# 🎬 MPEG zu Text – Lokale KI-Transkription

> Sprache in Text verwandeln – vollständig lokal, ohne Cloud, ohne Datenschutzrisiko.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Whisper](https://img.shields.io/badge/OpenAI-Whisper-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-teal)
![Lizenz](https://img.shields.io/badge/Lizenz-MIT-lightgrey)

---

## Was ist das?

**MPEG zu Text** ist eine schlanke, browserbasierte Desktop-Anwendung, die Audio- und Videodateien automatisch in Text transkribiert – vollständig **offline** und **ohne Datenweitergabe an Dritte**. Die KI läuft direkt auf dem eigenen Rechner.

---

## Features

- **Lokale KI** – OpenAI Whisper läuft komplett auf Ihrem Gerät. Keine Cloud, keine API-Kosten.
- **Datenschutzkonform** – Audiodaten verlassen niemals Ihren Computer. DSGVO-ready by design.
- **Breite Formatunterstützung** – MP4, MPEG, MOV, MKV, AVI, MP3, WAV, M4A
- **Modellauswahl** – Von `tiny` (blitzschnell) bis `medium` (höchste Genauigkeit), je nach Bedarf
- **Moderne Web-UI** – Drag & Drop, Fortschrittsanzeige, direkt im Browser
- **Kopieren & Exportieren** – Transkription mit einem Klick kopieren oder als `.txt` speichern
- **Einfaches Setup** – Ein einziger Befehl startet alles

---

## Voraussetzungen

- macOS (getestet), Linux möglich
- Python 3.9 oder neuer
- [Homebrew](https://brew.sh) (für automatische `ffmpeg`-Installation)

---

## Schnellstart

```bash
# Repository klonen
git clone https://github.com/bastio89/mpegtotext.git
cd mpegtotext

# Starten (Setup läuft automatisch)
chmod +x run.sh
./run.sh
```

Der Browser öffnet sich automatisch unter `http://localhost:8765`.

---

## So funktioniert es

1. **Datei auswählen** – per Klick oder Drag & Drop
2. **Modell wählen** – je nach gewünschter Geschwindigkeit/Genauigkeit
3. **„Transkribieren" klicken** – die KI arbeitet lokal
4. **Text kopieren oder speichern** – fertig

---

## Modellübersicht

| Modell   | Geschwindigkeit | Genauigkeit | Empfohlen für |
|----------|----------------|-------------|---------------|
| `tiny`   | ⚡⚡⚡⚡         | ★★☆☆        | Kurze Clips, schnelle Drafts |
| `base`   | ⚡⚡⚡          | ★★★☆        | Allgemeiner Einsatz (Standard) |
| `small`  | ⚡⚡            | ★★★★        | Meetings, Interviews |
| `medium` | ⚡              | ★★★★★       | Maximale Präzision |

---

## Technologie-Stack

| Komponente | Technologie |
|-----------|-------------|
| KI-Transkription | [OpenAI Whisper](https://github.com/openai/whisper) |
| Backend | [FastAPI](https://fastapi.tiangolo.com) + [Uvicorn](https://www.uvicorn.org) |
| Audio-Extraktion | [ffmpeg](https://ffmpeg.org) |
| Frontend | Vanilla HTML/CSS/JS (keine Abhängigkeiten) |

---

## Lizenz

MIT – frei verwendbar, anpassbar, erweiterbar.

---

## Über das Projekt

Dieses Tool entstand aus dem praktischen Bedarf, Gesprächsprotokolle, Interviews und Meeting-Aufzeichnungen schnell und datenschutzkonform zu verschriftlichen – ohne Abhängigkeit von externen Diensten wie Otter.ai oder Whisper-API-Clouds.

---

*Entwickelt mit ❤️ und lokaler KI.*
