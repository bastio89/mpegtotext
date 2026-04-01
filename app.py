import os
import tempfile
import subprocess
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

_model = None

def get_model():
    global _model
    if _model is None:
        import whisper
        _model = whisper.load_model("base")
    return _model


HTML = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MPEG zu Text</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: #0f0f0f;
    color: #e0e0e0;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 20px;
  }
  h1 { font-size: 1.8rem; font-weight: 600; margin-bottom: 8px; color: #fff; }
  .subtitle { color: #888; font-size: 0.9rem; margin-bottom: 40px; }
  .card {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 16px;
    padding: 32px;
    width: 100%;
    max-width: 680px;
  }
  .drop-zone {
    border: 2px dashed #3a3a3a;
    border-radius: 12px;
    padding: 48px 24px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
  }
  .drop-zone:hover, .drop-zone.dragover {
    border-color: #6366f1;
    background: rgba(99,102,241,0.05);
  }
  .drop-zone .icon { font-size: 2.5rem; margin-bottom: 12px; }
  .drop-zone p { color: #999; font-size: 0.9rem; }
  .drop-zone strong { color: #ccc; }
  #fileInput { display: none; }
  .file-info {
    display: none;
    margin-top: 16px;
    padding: 12px 16px;
    background: #252525;
    border-radius: 8px;
    font-size: 0.85rem;
    color: #aaa;
  }
  .file-info span { color: #e0e0e0; font-weight: 500; }
  .btn {
    display: block;
    width: 100%;
    margin-top: 20px;
    padding: 14px;
    background: #6366f1;
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
  }
  .btn:hover:not(:disabled) { background: #4f46e5; }
  .btn:disabled { background: #2a2a2a; color: #555; cursor: not-allowed; }
  .status {
    display: none;
    margin-top: 20px;
    padding: 14px 16px;
    border-radius: 10px;
    font-size: 0.85rem;
  }
  .status.loading { background: #1e2030; border: 1px solid #3a3d5c; color: #8b8fd8; }
  .status.error   { background: #200; border: 1px solid #500; color: #f88; }
  .progress-bar {
    height: 4px;
    background: #2a2a2a;
    border-radius: 2px;
    margin-top: 10px;
    overflow: hidden;
  }
  .progress-fill {
    height: 100%;
    background: #6366f1;
    border-radius: 2px;
    animation: indeterminate 1.5s infinite;
    width: 40%;
  }
  @keyframes indeterminate {
    0%   { margin-left: -40%; }
    100% { margin-left: 100%; }
  }
  .result-box {
    display: none;
    margin-top: 24px;
  }
  .result-box label {
    display: block;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #666;
    margin-bottom: 8px;
  }
  textarea {
    width: 100%;
    min-height: 200px;
    background: #111;
    border: 1px solid #2a2a2a;
    border-radius: 10px;
    color: #e0e0e0;
    font-size: 0.9rem;
    line-height: 1.6;
    padding: 16px;
    resize: vertical;
    font-family: inherit;
  }
  .actions {
    display: flex;
    gap: 10px;
    margin-top: 12px;
  }
  .btn-sm {
    padding: 8px 18px;
    background: #252525;
    border: 1px solid #3a3a3a;
    color: #ccc;
    border-radius: 8px;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s;
  }
  .btn-sm:hover { background: #303030; color: #fff; }
  .model-select {
    margin-top: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.85rem;
    color: #888;
  }
  select {
    background: #252525;
    border: 1px solid #3a3a3a;
    color: #ccc;
    padding: 6px 10px;
    border-radius: 6px;
    font-size: 0.85rem;
  }
</style>
</head>
<body>
<h1>MPEG zu Text</h1>
<p class="subtitle">Lokale Transkription mit Whisper</p>
<div class="card">
  <div class="drop-zone" id="dropZone" onclick="document.getElementById('fileInput').click()">
    <div class="icon">🎬</div>
    <strong>Datei auswählen oder hierher ziehen</strong>
    <p style="margin-top:6px">MP4, MPEG, MOV, MKV, AVI, MP3, WAV, M4A</p>
  </div>
  <input type="file" id="fileInput" accept="video/*,audio/*,.mpeg,.mpg,.mkv">
  <div class="file-info" id="fileInfo">Datei: <span id="fileName"></span></div>
  <div class="model-select">
    <span>Modell:</span>
    <select id="modelSelect">
      <option value="tiny">tiny (schnellste)</option>
      <option value="base" selected>base (empfohlen)</option>
      <option value="small">small (genauer)</option>
      <option value="medium">medium (langsam)</option>
    </select>
    <span id="modelHint" style="color:#555; font-size:0.8rem"></span>
  </div>
  <button class="btn" id="transcribeBtn" disabled onclick="transcribe()">Transkribieren</button>
  <div class="status" id="status">
    <span id="statusText">Verarbeitung läuft...</span>
    <div class="progress-bar"><div class="progress-fill"></div></div>
  </div>
  <div class="result-box" id="resultBox">
    <label>Transkription</label>
    <textarea id="resultText" readonly></textarea>
    <div class="actions">
      <button class="btn-sm" onclick="copyText()">Kopieren</button>
      <button class="btn-sm" onclick="saveText()">Als .txt speichern</button>
    </div>
  </div>
</div>

<script>
let selectedFile = null;

const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');

dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('dragover'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', e => {
  e.preventDefault();
  dropZone.classList.remove('dragover');
  if (e.dataTransfer.files[0]) setFile(e.dataTransfer.files[0]);
});
fileInput.addEventListener('change', () => { if (fileInput.files[0]) setFile(fileInput.files[0]); });

function setFile(file) {
  selectedFile = file;
  document.getElementById('fileName').textContent = file.name + ' (' + (file.size / 1024 / 1024).toFixed(1) + ' MB)';
  document.getElementById('fileInfo').style.display = 'block';
  document.getElementById('transcribeBtn').disabled = false;
  document.getElementById('resultBox').style.display = 'none';
  document.getElementById('status').style.display = 'none';
}

async function transcribe() {
  if (!selectedFile) return;
  const model = document.getElementById('modelSelect').value;
  const btn = document.getElementById('transcribeBtn');
  const status = document.getElementById('status');
  const statusText = document.getElementById('statusText');

  btn.disabled = true;
  status.className = 'status loading';
  status.style.display = 'block';
  statusText.textContent = 'Datei wird hochgeladen und verarbeitet...';
  document.getElementById('resultBox').style.display = 'none';

  const formData = new FormData();
  formData.append('file', selectedFile);
  formData.append('model', model);

  try {
    const res = await fetch('/transcribe', { method: 'POST', body: formData });
    const data = await res.json();
    if (data.error) throw new Error(data.error);

    document.getElementById('resultText').value = data.text;
    document.getElementById('resultBox').style.display = 'block';
    status.style.display = 'none';
  } catch (err) {
    status.className = 'status error';
    statusText.textContent = 'Fehler: ' + err.message;
  } finally {
    btn.disabled = false;
  }
}

function copyText() {
  navigator.clipboard.writeText(document.getElementById('resultText').value);
}

function saveText() {
  const text = document.getElementById('resultText').value;
  const name = (selectedFile?.name || 'transkription').replace(/[.][^.]+$/, '') + '.txt';
  const blob = new Blob([text], { type: 'text/plain' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = name;
  a.click();
}
</script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...), model: str = "base"):
    if not WHISPER_AVAILABLE:
        return JSONResponse({"error": "whisper ist nicht installiert. Bitte 'run.sh' ausführen."})

    allowed_models = {"tiny", "base", "small", "medium", "large"}
    if model not in allowed_models:
        model = "base"

    suffix = Path(file.filename).suffix or ".mp4"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        global _model
        import whisper
        if _model is None or getattr(_model, "_model_name", None) != model:
            _model = whisper.load_model(model)
            _model._model_name = model

        result = _model.transcribe(tmp_path)
        return {"text": result["text"].strip()}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    finally:
        os.unlink(tmp_path)


if __name__ == "__main__":
    print("Starte MPEG-zu-Text Tool...")
    print("Browser öffnen: http://localhost:8765")
    uvicorn.run(app, host="127.0.0.1", port=8765)
