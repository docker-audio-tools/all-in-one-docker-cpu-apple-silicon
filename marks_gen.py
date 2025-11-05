#!/usr/bin/env python3
"""
Genera un archivo MIDI con locators (marcadores) a partir de un JSON de estructura musical.
Ejemplo de uso:
    python generar_midi.py japonesa.json
Salida:
    estructura.mid
"""

import json
import sys
from mido import MidiFile, MidiTrack, MetaMessage, bpm2tempo
from pathlib import Path


def generar_midi(json_path):
    # === Cargar JSON ===
    with open(json_path) as f:
        data = json.load(f)

    bpm = data.get("bpm", 120)
    segments = data.get("segments", [])
    if not segments:
        print("⚠️ No se encontraron segmentos en el JSON.")
        return

    # === Crear archivo MIDI ===
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage("set_tempo", tempo=bpm2tempo(bpm), time=0))

    ticks_per_beat = mid.ticks_per_beat  # 480 por defecto

    # === Agregar marcadores ===
    for seg in segments:
        start_sec = float(seg["start"])
        label = seg["label"]

        # Conversión de segundos → ticks (aproximado)
        start_tick = int(start_sec * ticks_per_beat * bpm / 60)
        track.append(MetaMessage("marker", text=label, time=start_tick))

    # === Guardar ===
    out_path = Path(json_path).with_suffix(".mid")
    mid.save(out_path)
    print(f"✅ MIDI generado: {out_path} (BPM={bpm}, {len(segments)} segmentos)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python generar_midi.py <archivo.json>")
        sys.exit(1)

    generar_midi(sys.argv[1])
