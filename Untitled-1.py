"""
Lokale Transkription mit faster-whisper.
Voraussetzungen:
    1) ffmpeg installiert (System)
    2) pip install faster-whisper

Aufruf:  python transkribieren.py
Die Audiodatei muss im selben Ordner liegen (oder Pfad unten anpassen).
Alles laeuft lokal; nur das Modell wird beim ersten Lauf einmalig geladen.
"""

from pathlib import Path
from faster_whisper import WhisperModel

# --- Einstellungen -----------------------------------------------------------
AUDIO_DATEI = "Jonas.m4a"      # Pfad zur Aufnahme
SPRACHE     = "de"             # Deutsch
MODELL      = "large-v3"       # beste Qualitaet fuer Deutsch
                               # zu langsam? -> "medium" oder "small"
COMPUTE     = "int8"           # CPU-freundlich; bei GPU: "float16"
# -----------------------------------------------------------------------------

audio = Path(AUDIO_DATEI)
basis = audio.with_suffix("")  # Name ohne Endung, fuer die Ausgabedateien

print(f"Lade Modell '{MODELL}' (erster Lauf laedt es einmalig herunter) ...")
model = WhisperModel(MODELL, device="cpu", compute_type=COMPUTE)

print("Transkribiere ... (das kann bei ~49 Min ein paar Minuten dauern)")
segmente, info = model.transcribe(str(audio), language=SPRACHE, vad_filter=True)

# Zwei Ausgaben: reiner Fliesstext + Version mit Zeitstempeln (gut fuer Zitate)
txt_pfad = basis.with_name(basis.name + "_transkript.txt")
ts_pfad  = basis.with_name(basis.name + "_transkript_zeitstempel.txt")

def hms(sekunden: float) -> str:
    s = int(sekunden)
    return f"{s // 3600:02d}:{(s % 3600) // 60:02d}:{s % 60:02d}"

with txt_pfad.open("w", encoding="utf-8") as f_txt, \
     ts_pfad.open("w", encoding="utf-8") as f_ts:
    for seg in segmente:
        text = seg.text.strip()
        f_txt.write(text + " ")
        f_ts.write(f"[{hms(seg.start)} - {hms(seg.end)}] {text}\n")
        print(f"[{hms(seg.start)}] {text}")  # Live-Fortschritt im Terminal

print("\nFertig.")
print(f"  Fliesstext:   {txt_pfad}")
print(f"  Zeitstempel:  {ts_pfad}")