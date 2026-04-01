#!/bin/bash
set -e

echo "=== MPEG zu Text Setup ==="

# ffmpeg prüfen/installieren
if ! command -v ffmpeg &> /dev/null; then
  echo "Installiere ffmpeg..."
  if command -v brew &> /dev/null; then
    brew install ffmpeg
  else
    echo "Homebrew nicht gefunden. Bitte ffmpeg manuell installieren: https://ffmpeg.org"
    exit 1
  fi
else
  echo "ffmpeg: OK"
fi

# Python-Pakete installieren
echo "Installiere Python-Abhängigkeiten..."
pip3 install --quiet --break-system-packages openai-whisper uvicorn fastapi python-multipart 2>&1 | tail -5

echo ""
echo "Starte Server auf http://localhost:8765"
echo "Zum Beenden: Ctrl+C"
echo ""

# Browser öffnen (kurz warten bis Server bereit)
(sleep 2 && open "http://localhost:8765") &

python3 "$(dirname "$0")/app.py"
