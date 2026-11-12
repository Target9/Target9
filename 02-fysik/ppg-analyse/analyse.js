/* PPG-analyse: finder puls ud fra lysstyrken i en video af en fingerspids.
 * Virker både i browseren (window.PPG) og i Node (module.exports) til test.
 */
(function (root) {
  "use strict";

  const FS = 30; // analysefrekvens (Hz) efter resampling

  function mean(a) {
    let s = 0;
    for (const v of a) s += v;
    return a.length ? s / a.length : 0;
  }

  function std(a) {
    const m = mean(a);
    let s = 0;
    for (const v of a) s += (v - m) * (v - m);
    return a.length > 1 ? Math.sqrt(s / (a.length - 1)) : 0;
  }

  function median(a) {
    if (!a.length) return 0;
    const s = [...a].sort((x, y) => x - y);
    const k = Math.floor(s.length / 2);
    return s.length % 2 ? s[k] : (s[k - 1] + s[k]) / 2;
  }

  function percentile(a, p) {
    if (!a.length) return 0;
    const s = [...a].sort((x, y) => x - y);
    const idx = Math.min(s.length - 1, Math.max(0, Math.round((p / 100) * (s.length - 1))));
    return s[idx];
  }

  function movingAverage(a, win) {
    const out = new Array(a.length);
    const half = Math.floor(win / 2);
    let sum = 0;
    let lo = 0;
    let hi = -1;
    for (let i = 0; i < a.length; i++) {
      const L = Math.max(0, i - half);
      const H = Math.min(a.length - 1, i + half);
      while (hi < H) sum += a[++hi];
      while (lo < L) sum -= a[lo++];
      out[i] = sum / (hi - lo + 1);
    }
    return out;
  }

  /** Lineær resampling af ujævnt samplede målinger til fast frekvens. */
  function resample(samples, key) {
    const t0 = samples[0].t;
    const t1 = samples[samples.length - 1].t;
    const n = Math.floor((t1 - t0) * FS) + 1;
    const t = new Array(n);
    const v = new Array(n);
    let j = 0;
    for (let i = 0; i < n; i++) {
      const ti = t0 + i / FS;
      while (j < samples.length - 2 && samples[j + 1].t < ti) j++;
      const a = samples[j];
      const b = samples[j + 1] || a;
      const f = b.t > a.t ? (ti - a.t) / (b.t - a.t) : 0;
      t[i] = ti - t0;
      v[i] = a[key] + (b[key] - a[key]) * Math.min(1, Math.max(0, f));
    }
    return { t, v };
  }

  function channelStats(raw) {
    const trend = movingAverage(raw, Math.round(FS * 1.0));
    const detr = raw.map((x, i) => x - trend[i]);
    const smooth = movingAverage(detr, 3);
    const edge = Math.min(FS, Math.floor(smooth.length / 4));
    const core = smooth.slice(edge, smooth.length - edge);
    const dc = mean(raw);
    const ac = percentile(core, 95) - percentile(core, 5);
    return { dc, ac, acdc: dc > 0 ? (ac / dc) * 100 : 0, filtered: smooth, saturated: dc > 250 };
  }

  /** Finder hjerteslag: blod absorberer lys, så hvert slag giver et minimum i lysstyrken. */
  function detectBeats(filtered) {
    const s = filtered.map((x) => -x);
    const thr = 0.35 * std(s);
    const minDist = Math.round(FS * 0.33); // max ca. 180 slag/min
    const peaks = [];
    for (let i = 2; i < s.length - 2; i++) {
      if (s[i] > thr && s[i] >= s[i - 1] && s[i] >= s[i + 1] && s[i] >= s[i - 2] && s[i] >= s[i + 2]) {
        if (peaks.length && i - peaks[peaks.length - 1] < minDist) {
          if (s[i] > s[peaks[peaks.length - 1]]) peaks[peaks.length - 1] = i;
        } else {
          peaks.push(i);
        }
      }
    }
    return peaks;
  }

  /**
   * samples: [{t (s), r, g, b}] – middel-lysstyrke pr. billede (0–255).
   * channel: "auto" | "r" | "g" | "b"
   */
  function analyse(samples, channel) {
    if (!samples || samples.length < FS * 4) {
      return { error: "For kort optagelse – optag mindst 10 sekunder." };
    }
    const sorted = [...samples].sort((a, b) => a.t - b.t);
    const ch = {};
    let time = null;
    for (const key of ["r", "g", "b"]) {
      const { t, v } = resample(sorted, key);
      time = t;
      ch[key] = { raw: v, ...channelStats(v) };
    }
    let use = channel;
    if (!use || use === "auto") {
      use = ["r", "g", "b"]
        .filter((k) => ch[k].dc > 15 && !ch[k].saturated)
        .sort((a, b) => ch[b].acdc - ch[a].acdc)[0] || "g";
    }
    const beats = detectBeats(ch[use].filtered);
    const beatTimes = beats.map((i) => time[i]);
    const intervals = [];
    for (let i = 1; i < beatTimes.length; i++) intervals.push(beatTimes[i] - beatTimes[i - 1]);
    const medInt = median(intervals);
    const irregular = [];
    intervals.forEach((iv, i) => {
      if (medInt > 0 && Math.abs(iv - medInt) / medInt > 0.25) irregular.push(i + 1);
    });
    const regular = intervals.filter((iv) => medInt > 0 && Math.abs(iv - medInt) / medInt <= 0.25);
    const bpm = regular.length ? 60 / mean(regular) : 0;
    const cv = intervals.length > 1 ? (std(intervals) / mean(intervals)) * 100 : 0;
    let quality = "god";
    if (beats.length < 5 || bpm < 35 || bpm > 200) quality = "dårlig";
    else if (irregular.length > beats.length * 0.3 || ch[use].acdc < 0.05) quality = "usikker";
    return {
      fs: FS,
      duration: time[time.length - 1],
      time,
      channels: ch,
      used: use,
      beats,
      beatTimes,
      intervals,
      irregular,
      bpm,
      cv,
      quality,
    };
  }

  /** Syntetisk fingerspids-signal til demo/test (inkl. et ekstra-slag). */
  function demoSamples(bpm, seconds, extraBeatAt) {
    const out = [];
    const fps = 30;
    const period = 60 / bpm;
    const beats = [];
    for (let t = 0.3; t < seconds; t += period) beats.push(t);
    if (extraBeatAt) {
      beats.push(extraBeatAt);
      beats.sort((a, b) => a - b);
    }
    let seed = 7;
    const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647 - 0.5);
    for (let i = 0; i < seconds * fps; i++) {
      const t = i / fps;
      let p = 0;
      for (const bt of beats) {
        const d = t - bt;
        if (d > -0.3 && d < 0.8) p += Math.exp(-((d - 0.1) ** 2) / 0.006) + 0.35 * Math.exp(-((d - 0.35) ** 2) / 0.006);
      }
      const drift = 3 * Math.sin(t / 3);
      out.push({
        t,
        r: 235 + drift - 1.2 * p + rnd() * 0.4,
        g: 38 + drift * 0.3 - 0.9 * p + rnd() * 0.25,
        b: 6 - 0.05 * p + rnd() * 0.2,
      });
    }
    return out;
  }

  const api = { analyse, demoSamples, movingAverage, detectBeats, FS };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.PPG = api;
})(typeof window !== "undefined" ? window : globalThis);
