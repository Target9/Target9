"""Reading the STIL 6-character captcha.

The gateway in front of UniLogin shows a 6 character code as an image *and*
reads it aloud. Neither channel alone is reliable, so this module fuses them:

* the audio is transcribed by faster-whisper (two models, two prompts) and
  voted on — it gets the *letters* right most of the time
* the image is tone-isolated (the glyphs are drawn in one flat grey tone that
  differs from both the background and the noise lines), split into glyphs with
  connected components, and each glyph is template-matched against rendered
  fonts, which resolves case and look-alikes (S/F, 2/Z, 8/B, D/O, U/V ...)

`read()` returns, for each of the six positions, the candidate characters ranked
by how well they match the picture. Callers can then try the top combination and
fall back to the next ones.
"""

from __future__ import annotations

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT_PATHS = (
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/croscore/Arimo-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/croscore/Arimo-Regular.ttf",
)
FONT_SIZES = (26, 30, 34, 38, 42, 46)
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

# Look-alikes, used when generating alternative spellings of a reading.
CONFUSABLE = {
    "0": "ODQo", "O": "0DQ", "D": "0O", "Q": "0O", "o": "0OD",
    "1": "ILl", "I": "1Ll", "L": "1I", "l": "1I",
    "2": "Zz", "Z": "2z", "z": "2Z",
    "5": "S", "S": "5F", "s": "5",
    "8": "B", "B": "8", "b": "8",
    "6": "G", "G": "6C", "9": "g", "g": "9", "q": "9",
    "U": "VY", "V": "UY", "u": "vy", "v": "uy",
    "F": "ET", "E": "F", "T": "7", "7": "T",
    "M": "WN", "N": "MH", "W": "M", "H": "N",
    "C": "G", "K": "X", "X": "K", "P": "R", "R": "P",
    "Y": "V", "y": "v", "c": "e", "e": "c", "n": "h", "h": "n",
    "m": "nm", "r": "n", "f": "t", "t": "f", "i": "j", "j": "i",
    "A": "4", "4": "A", "3": "8", "a": "9",
}

_GLYPH_SIZE = (26, 34)
_templates: dict[str, list[np.ndarray]] | None = None


def _render_templates() -> dict[str, list[np.ndarray]]:
    """Glyph masks for every character in every bundled font, normalised."""
    out: dict[str, list[np.ndarray]] = {}
    for path in FONT_PATHS:
        for size in FONT_SIZES:
            try:
                font = ImageFont.truetype(path, size)
            except Exception:
                continue
            for char in ALPHABET:
                canvas = Image.new("L", (90, 90), 0)
                ImageDraw.Draw(canvas).text((14, 8), char, fill=255, font=font)
                mask = np.array(canvas)
                ys, xs = np.nonzero(mask > 127)
                if len(ys) == 0:
                    continue
                crop = mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
                out.setdefault(char, []).append(
                    cv2.resize(crop.astype(np.float32) / 255.0, _GLYPH_SIZE,
                               interpolation=cv2.INTER_AREA))
    return out


def templates() -> dict[str, list[np.ndarray]]:
    global _templates
    if _templates is None:
        _templates = _render_templates()
    return _templates


def _normalise(patch: np.ndarray) -> np.ndarray | None:
    ys, xs = np.nonzero(patch > 0)
    if len(ys) == 0:
        return None
    crop = patch[ys.min():ys.max() + 1, xs.min():xs.max() + 1].astype(np.float32)
    # patches are 0..255 masks, templates are 0..1
    if crop.max() > 1.0:
        crop /= 255.0
    return cv2.resize(crop, _GLYPH_SIZE, interpolation=cv2.INTER_AREA)


def isolate_glyphs(image: np.ndarray, count: int = 6):
    """Split the captcha into `count` glyph patches.

    The glyphs are painted in one flat grey; picking the most common tone in the
    100..205 range and keeping a narrow band around it leaves the glyphs while
    dropping the background (near white) and the darker noise lines.
    """
    values, frequencies = np.unique(image, return_counts=True)
    tones = [(v, c) for v, c in zip(values, frequencies) if 100 <= v <= 205 and c >= 150]
    tones.sort(key=lambda item: -item[1])

    best = None
    for tone, _ in tones[:4]:
        for band in (5, 6, 8, 10):
            mask = ((image >= tone - band) & (image <= tone + band)).astype(np.uint8) * 255
            mask = cv2.medianBlur(mask, 3)
            count_components, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
            boxes = []
            for i in range(1, count_components):
                x, y, w, h, area = stats[i]
                if area >= 70 and 11 <= h <= 55 and 4 <= w <= 55:
                    boxes.append([x, y, w, h, area])
            if not boxes:
                continue
            boxes.sort()
            merged = _merge_boxes(boxes)
            merged = _fit_count(merged, count)
            if len(merged) != count:
                continue
            mass = sum(box[4] for box in merged)
            if best is None or mass > best[0]:
                best = (mass, merged, mask.copy())
    if best is None:
        return None, None

    _, boxes, mask = best
    patches = [mask[max(0, y - 1):y + h + 1, max(0, x - 1):x + w + 1]
               for x, y, w, h, _ in boxes]
    return patches, boxes


def _merge_boxes(boxes):
    """Join components that belong to the same glyph (broken strokes)."""
    merged = []
    for box in boxes:
        if merged and box[0] < merged[-1][0] + merged[-1][2] - 3:
            px, py, pw, ph, pa = merged[-1]
            x2 = max(px + pw, box[0] + box[2])
            y2 = max(py + ph, box[1] + box[3])
            merged[-1] = [min(px, box[0]), min(py, box[1]), x2 - min(px, box[0]),
                          y2 - min(py, box[1]), pa + box[4]]
        else:
            merged.append(list(box))
    return merged


def _fit_count(boxes, count):
    """Drop specks / split glued pairs so that exactly `count` boxes remain."""
    boxes = [list(b) for b in boxes]
    while len(boxes) > count:
        boxes.sort(key=lambda b: b[4])
        boxes.pop(0)
        boxes.sort()
    while len(boxes) < count:
        widest = max(range(len(boxes)), key=lambda i: boxes[i][2])
        x, y, w, h, area = boxes[widest]
        if w < 13:
            break
        mid = x + w // 2
        boxes[widest:widest + 1] = [[x, y, mid - x, h, area // 2],
                                    [mid, y, x + w - mid, h, area // 2]]
        boxes.sort()
    return boxes


def _candidates(audio_code: str | None, position: int) -> list[str]:
    if not audio_code or position >= len(audio_code):
        return list(ALPHABET)
    char = audio_code[position]
    found = {char, char.upper(), char.lower()}
    for variant in (char.upper(), char.lower()):
        for other in CONFUSABLE.get(variant, ""):
            found.update((other, other.upper(), other.lower()))
    return [c for c in found if c]


def _score(patch: np.ndarray, candidates: list[str]) -> list[tuple[str, float]]:
    normalised = _normalise(patch)
    table = templates()
    scored = []
    for char in candidates:
        pool = table.get(char)
        if not pool or normalised is None:
            scored.append((char, float("inf")))
            continue
        scored.append((char, min(float(np.mean((normalised - glyph) ** 2))
                                 for glyph in pool)))
    scored.sort(key=lambda item: item[1])
    return scored


def read(image_path: str, audio_readings: list[str], debug: bool = False):
    """Rank the characters for each of the six positions.

    `audio_readings` are the transcriptions of the spoken code; they restrict the
    candidate set per position. Returns the ranked lists, or None if the image
    could not be segmented.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return None
    patches, _ = isolate_glyphs(image)
    if not patches:
        return None
    ranked = []
    for position in range(6):
        candidates = set()
        for reading in audio_readings:
            candidates.update(_candidates(reading, position))
        if not candidates:
            candidates = set(ALPHABET)
        ranked.append(_score(patches[position], sorted(candidates)))
        if debug:
            print(f"  pos{position}: " + " ".join(f"{c}:{d:.0f}" for c, d in ranked[position][:6]))
    return ranked


def best_code(ranked) -> str:
    return "".join(position[0][0] if position else "?" for position in ranked)


def top_codes(ranked, limit: int = 12) -> list[str]:
    """Whole-code candidates, ranked by summed glyph distance (max 2 changes)."""
    options = [position[:3] for position in ranked]
    scored: list[tuple[str, float]] = []
    length = len(options)

    def walk(position, chosen, remaining, total):
        if position == length:
            scored.append(("".join(chosen), total))
            return
        for index, (char, distance) in enumerate(options[position]):
            if index > 0:
                if remaining == 0:
                    continue
                walk(position + 1, chosen + [char], remaining - 1, total + distance)
            else:
                walk(position + 1, chosen + [char], remaining, total + distance)

    walk(0, [], 2, 0.0)
    scored.sort(key=lambda item: item[1])
    seen, unique = set(), []
    for code, _ in scored:
        if code.upper() in seen:
            continue
        seen.add(code.upper())
        unique.append(code)
        if len(unique) >= limit:
            break
    return unique


def variants(code: str, limit: int = 40) -> list[str]:
    """Spellings of `code` that swap one or two look-alike glyphs."""
    out = [code]
    for index in range(len(code) - 1, -1, -1):
        for other in CONFUSABLE.get(code[index], ""):
            out.append(code[:index] + other + code[index + 1:])
    for i in range(len(code)):
        for j in range(i + 1, len(code)):
            for a in CONFUSABLE.get(code[i], ""):
                for b in CONFUSABLE.get(code[j], ""):
                    candidate = list(code)
                    candidate[i], candidate[j] = a, b
                    out.append("".join(candidate))
    seen, unique = set(), []
    for candidate in out:
        if candidate.upper() not in seen:
            seen.add(candidate.upper())
            unique.append(candidate)
    return unique[:limit]
