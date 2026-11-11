#!/usr/bin/env bash
# Install everything main.py needs: system fonts/tools, Python packages, Chromium.
set -euo pipefail

echo "== system packages"
sudo apt-get update -qq
sudo apt-get install -y --no-install-recommends \
  ffmpeg tesseract-ocr \
  fonts-liberation fonts-dejavu fonts-croscore fonts-noto-core

echo "== python packages"
python3 -m pip install --upgrade pip
python3 -m pip install -r "$(dirname "$0")/requirements.txt"

echo "== chromium for playwright"
python3 -m playwright install --with-deps chromium

echo "== smoke test (captures one captcha and prints the readings)"
python3 "$(dirname "$0")/main.py" --check
