"""Monta um Short vertical (1080x1920) do canal GTAVI | MISSION PASSED.

Uso: python3 tools/render_short.py producao/<pasta>/projeto.json

projeto.json (caminhos relativos à pasta do projeto):
{
  "voice": "narracao.mp3",
  "timings": "timings.json",          # {"duration": s, "words": [{"text","start","end"}]}
  "music": "../../library/musicas/trilha_01_synthwave_miami.mp3",
  "hook": "TÍTULO DO GANCHO\\NSEGUNDA LINHA",  # \\N = quebra de linha (ASS)
  "hook_end": 4.9,
  "highlight": ["palavras", "em", "amarelo"],
  "end_card_start": 32.6,
  "scenes": [{"image": "cenas/c1.png", "start": 0},
             {"video": "gameplay/sa_trecho.mp4", "from": 12.5, "start": 6.0},  # trecho de gameplay (sem áudio)
             ...],
  "out": "final.mp4"
}

O que ele faz:
- zoom lento (Ken Burns) em cada imagem, alternando aproximar/afastar;
- legenda animada de 3 palavras por vez, palavra falada em amarelo;
- título-gancho no topo nos primeiros segundos;
- cartão final dourado "MISSION PASSED" + "SEGUE O CANAL";
- música de fundo baixa, com abaixamento automático quando a voz fala.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "brand" / "fonts"
W, H, FPS = 1080, 1920, 30


def ts(t):
    t = max(t, 0)
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def clean(word):
    return word.replace("{", "").replace("}", "")


def build_ass(proj, words, duration, path):
    hl = {w.lower() for w in proj.get("highlight", [])}
    lines = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 2", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
        "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding",
        # cores ASS: &HAABBGGRR
        "Style: Cap,Anton,124,&H00FFFFFF,&H00FFFFFF,&H00140614,&H96000000,0,0,0,0,100,100,1,0,1,8,4,5,60,60,0,1",
        "Style: Hook,Anton,128,&H0028C4FF,&H0028C4FF,&H00140614,&H96000000,0,0,0,0,100,100,1,0,1,9,5,8,60,60,190,1",
        "Style: End,Anton,170,&H0028C4FF,&H0028C4FF,&H00140614,&H96000000,0,0,0,0,100,100,1,0,1,10,6,5,40,40,0,1",
        "Style: EndSub,Anton,88,&H00FFFFFF,&H00FFFFFF,&H00140614,&H96000000,0,0,0,0,100,100,1,0,1,7,4,5,40,40,0,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    end_start = proj.get("end_card_start", duration)
    # legenda: grupos de até 3 palavras, quebrando em pontuação
    groups, cur = [], []
    for w in words:
        if w["text"].strip() in {".", ",", "!", "?"}:
            continue
        cur.append(w)
        if len(cur) == 3 or w["text"][-1] in ".,?!:":
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    for gi, g in enumerate(groups):
        g_end = groups[gi + 1][0]["start"] if gi + 1 < len(groups) else g[-1]["end"] + 0.3
        for wi, w in enumerate(g):
            start = w["start"] if wi else g[0]["start"]
            stop = g[wi + 1]["start"] if wi + 1 < len(g) else g_end
            if start >= end_start:
                continue
            stop = min(stop, end_start)
            parts = []
            for k, x in enumerate(g):
                txt = clean(x["text"]).upper()
                if k == wi:
                    col = "&H0028C4FF&"  # dourado: palavra falada agora
                    parts.append(r"{\c" + col + r"\fscx112\fscy112}" + txt + r"{\r}")
                elif x["text"].lower() in hl:
                    parts.append(r"{\c&H00A53EFF&}" + txt + r"{\r}")  # rosa neon
                else:
                    parts.append(txt)
            pop = r"{\fad(40,0)}" if wi == 0 else ""
            lines.append(f"Dialogue: 1,{ts(start)},{ts(stop)},Cap,,0,0,0,,{{\\pos({W//2},{int(H*0.70)})}}{pop}" + " ".join(parts))
    if proj.get("hook"):
        lines.append(f"Dialogue: 2,{ts(0)},{ts(proj.get('hook_end', 4))},Hook,,0,0,0,,{{\\fad(150,200)}}{proj['hook']}")
    if end_start < duration:
        lines.append(f"Dialogue: 3,{ts(end_start)},{ts(duration)},End,,0,0,0,,{{\\pos({W//2},{int(H*0.40)})\\fad(200,0)\\t(0,250,\\fscx115\\fscy115)\\t(250,450,\\fscx100\\fscy100)}}MISSION PASSED")
        lines.append(f"Dialogue: 3,{ts(end_start + 0.4)},{ts(duration)},EndSub,,0,0,0,,{{\\pos({W//2},{int(H*0.49)})\\fad(200,0)}}SEGUE O CANAL ★★★★★")
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(proj_file):
    proj_path = Path(proj_file).resolve()
    base = proj_path.parent
    proj = json.loads(proj_path.read_text())
    tim = json.loads((base / proj["timings"]).read_text())
    voice = base / proj["voice"]
    duration = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(voice)]).strip()) + 0.8
    work = base / "_render"
    work.mkdir(exist_ok=True)

    # 1) um clipe por cena com zoom lento
    scenes = proj["scenes"]
    clips = []
    for i, sc in enumerate(scenes):
        start = sc["start"]
        end = scenes[i + 1]["start"] if i + 1 < len(scenes) else duration
        n = max(int(round((end - start) * FPS)), 1)
        zin = i % 2 == 0
        z = f"1+0.14*on/{n}" if zin else f"1.14-0.14*on/{n}"
        out = work / f"cena_{i:02d}.mp4"
        if sc.get("video"):
            # trecho de gameplay: horizontal -> vertical com fundo desfocado, sem o áudio original
            src = base / sc["video"]
            ss = str(sc.get("from", 0))
            fc_v = (f"[0:v]fps={FPS},split=2[a][b];"
                    f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=28:2,eq=brightness=-0.12[bg];"
                    f"[b]scale={W}:-2,eq=saturation=1.08:contrast=1.04[fg];"
                    f"[bg][fg]overlay=(W-w)/2:(H-h)/2-120,format=yuv420p[v]")
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", ss, "-stream_loop", "-1", "-i", str(src),
                            "-filter_complex", fc_v, "-map", "[v]", "-an", "-frames:v", str(n),
                            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(out)], check=True)
            clips.append(out)
            continue
        vf = (f"scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},"
              f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS},"
              f"eq=saturation=1.08:contrast=1.04,format=yuv420p")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(base / sc["image"]), "-vf", vf,
                        "-frames:v", str(n), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(out)], check=True)
        clips.append(out)
    lst = work / "lista.txt"
    lst.write_text("".join(f"file '{c}'\n" for c in clips))

    # 2) legendas
    ass = work / "legenda.ass"
    build_ass(proj, tim["words"], duration, ass)

    # 3) montagem final: vídeo + legenda + voz + música com ducking
    music = (base / proj["music"]).resolve()
    out = base / proj.get("out", "final.mp4")
    fade_at = max(duration - 1.5, 0)
    fc = (
        f"[0:v]ass={ass}:fontsdir={FONTS},format=yuv420p[v];"
        f"[1:a]aresample=48000,volume=1.6,asplit=2[voz][sc];"
        f"[2:a]aresample=48000,volume=0.30,afade=t=in:d=0.5,afade=t=out:st={fade_at}:d=1.5[mus];"
        f"[mus][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=350[duck];"
        f"[voz][duck]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]"
    )
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-i", str(voice), "-stream_loop", "-1", "-i", str(music),
                    "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{duration:.2f}",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-r", str(FPS),
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)], check=True)
    print("ok:", out, f"{duration:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])
