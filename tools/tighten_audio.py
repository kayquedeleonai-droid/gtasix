"""Encurta pausas longas da narração e acelera levemente, mantendo os tempos das palavras sincronizados.

Uso: python3 tools/tighten_audio.py narracao.mp3 timings_brutos.json narracao_ajustada.wav timings.json [tempo=1.15] [pausa_max=0.22]
"""
import json, subprocess, sys

src, tin, aout, tout = sys.argv[1:5]
tempo = float(sys.argv[5]) if len(sys.argv) > 5 else 1.15
gap_max = float(sys.argv[6]) if len(sys.argv) > 6 else 0.22
words = json.load(open(tin))["words"]
PAD_IN, PAD_OUT = 0.04, 0.10

# agrupa palavras em trechos de fala contínua
segs = []
for w in words:
    if segs and w["start"] - segs[-1]["end"] <= 0.30:
        segs[-1]["end"] = w["end"]; segs[-1]["words"].append(w)
    else:
        segs.append({"start": w["start"], "end": w["end"], "words": [w]})

pieces, new_words, cursor = [], [], 0.0
for i, s in enumerate(segs):
    a = max(0.0, s["start"] - PAD_IN)
    b = s["end"] + PAD_OUT
    if i + 1 < len(segs):
        b = min(b, segs[i + 1]["start"] - PAD_IN)
    pieces.append((a, b))
    for w in s["words"]:
        new_words.append({"text": w["text"], "start": (cursor + w["start"] - a) / tempo, "end": (cursor + w["end"] - a) / tempo})
    cursor += (b - a)
    if i + 1 < len(segs):
        gap = min(segs[i + 1]["start"] - s["end"], gap_max)
        pieces.append(("silence", gap))
        cursor += gap

parts, labels = [], []
for k, p in enumerate(pieces):
    if p[0] == "silence":
        parts.append(f"anullsrc=r=44100:cl=mono,atrim=duration={p[1]:.3f}[p{k}]")
    else:
        parts.append(f"[0:a]atrim={p[0]:.3f}:{p[1]:.3f},asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=mono[p{k}]")
    labels.append(f"[p{k}]")
fc = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(labels)}:v=0:a=1,atempo={tempo}[out]"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-filter_complex", fc, "-map", "[out]", aout], check=True)
dur = cursor / tempo
json.dump({"duration": round(dur, 3), "words": new_words}, open(tout, "w"), ensure_ascii=False, indent=0)
print(f"ok: {dur:.1f}s (antes {words[-1]['end']:.1f}s)")
