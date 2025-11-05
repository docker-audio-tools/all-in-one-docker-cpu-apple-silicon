#!/usr/bin/env python3
"""
Genera un archivo MIDI con marcadores de secciones desde un JSON.
Uso:
    python generate_midi_from_json.py japonesa.json

El archivo MIDI contendrá:
- Markers de texto para cada sección
- Tempo (BPM) del JSON
- Opcionalmente notas MIDI en cada cambio de sección
"""

import sys
import json
from pathlib import Path
from midiutil import MIDIFile

def main(json_path, add_notes=True):
    json_path = Path(json_path)

    if not json_path.exists():
        print(f"❌ Error: No se encuentra el archivo {json_path}")
        sys.exit(1)

    output_path = json_path.with_suffix('.mid')

    # 1) Leer JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    segments = data.get("segments", [])
    if not segments:
        print("⚠️ El JSON no contiene 'segments'. Nada que hacer.")
        return

    bpm = data.get("bpm", 120)

    # 2) Crear archivo MIDI
    # 1 track, con tempo
    midi = MIDIFile(1)
    track = 0
    channel = 0
    time = 0

    midi.addTempo(track, time, bpm)

    # 3) Agregar marcadores de texto para cada sección
    print(f"\n🎵 Generando MIDI con {len(segments)} marcadores:")

    # Mapeo de labels a notas MIDI (opcional)
    label_to_note = {
        "start": 60,   # C4
        "intro": 62,   # D4
        "verse": 64,   # E4
        "chorus": 67,  # G4
        "bridge": 69,  # A4
        "inst": 71,    # B4
        "outro": 72,   # C5
        "end": 60      # C4
    }

    for i, seg in enumerate(segments):
        label = seg.get("label", f"seg_{i+1}")
        start_time = float(seg['start'])
        end_time = float(seg['end'])
        duration = end_time - start_time

        # Agregar marcador de texto
        midi.addText(track, start_time, label)

        # Agregar nota MIDI al inicio de cada sección (opcional)
        if add_notes:
            note = label_to_note.get(label, 60)  # Default C4
            velocity = 100
            midi.addNote(track, channel, note, start_time, duration, velocity)

        print(f"   {i+1:2d}. {start_time:7.2f}s → {end_time:7.2f}s ({duration:6.2f}s) : {label}")

    # 4) Guardar archivo MIDI
    with open(output_path, "wb") as f:
        midi.writeFile(f)

    print(f"\n✅ Archivo MIDI generado: {output_path}")
    print(f"   BPM: {bpm}")
    print(f"   Marcadores: {len(segments)}")
    if add_notes:
        print(f"   Notas MIDI: Sí (una por sección)")
    print(f"\n💡 Importa este archivo MIDI en tu DAW para ver los marcadores de secciones.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python generate_midi_from_json.py <archivo.json>")
        print("\nEjemplo:")
        print("  python generate_midi_from_json.py japonesa.json")
        print("\nOpciones:")
        print("  --no-notes : No generar notas MIDI, solo marcadores de texto")
        sys.exit(1)

    json_file = sys.argv[1]
    add_notes = "--no-notes" not in sys.argv

    main(json_file, add_notes)
