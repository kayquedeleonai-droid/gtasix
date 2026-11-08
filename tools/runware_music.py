"""Gera músicas no Runware (MiniMax Music) em modo assíncrono e baixa os MP3.

Uso:
  RUNWARE_KEY_FILE=/caminho/da/chave python3 tools/runware_music.py jobs.json pasta_saida
jobs.json: lista de {"name": "...", "prompt": "...", "lyrics": "...opcional..."}
Sem "lyrics" a faixa é instrumental. Com "lyrics" só de tags ([Intro], [Inst]...)
o modelo costuma gerar uma faixa mais longa, ainda sem voz.
A chave NUNCA fica no repositório: vem de RUNWARE_API_KEY ou RUNWARE_KEY_FILE.
"""
import json, os, sys, time, uuid, urllib.request

API = "https://api.runware.ai/v1"


def key():
    if os.environ.get("RUNWARE_API_KEY"):
        return os.environ["RUNWARE_API_KEY"]
    return open(os.environ["RUNWARE_KEY_FILE"]).read().strip()


def call(tasks):
    req = urllib.request.Request(API, data=json.dumps(tasks).encode(), headers={
        "Authorization": f"Bearer {key()}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def main(jobs_file, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    jobs = json.load(open(jobs_file))
    pending = {}
    for j in jobs:
        tid = str(uuid.uuid4())
        task = {"taskType": "audioInference", "taskUUID": tid, "model": j.get("model", "minimax:music@2.6"),
                "positivePrompt": j["prompt"], "deliveryMethod": "async", "outputFormat": "MP3",
                "includeCost": True}
        task["settings"] = {"lyrics": j["lyrics"]} if j.get("lyrics") else {"instrumental": True}
        resp = call([task])
        if resp.get("errors"):
            print("ERRO ao enviar", j["name"], resp["errors"]); continue
        pending[tid] = j["name"]
        print("enviado:", j["name"])
    total = 0.0
    deadline = time.time() + 900
    while pending and time.time() < deadline:
        time.sleep(10)
        for tid, name in list(pending.items()):
            resp = call([{"taskType": "getResponse", "taskUUID": tid}])
            for e in resp.get("errors", []):
                print("ERRO", name, e.get("message")); pending.pop(tid, None)
            for d in resp.get("data", []):
                url = d.get("audioURL")
                if url:
                    path = os.path.join(out_dir, name + ".mp3")
                    urllib.request.urlretrieve(url, path)
                    total += d.get("cost", 0) or 0
                    print("pronto:", path, "custo:", d.get("cost"))
                    pending.pop(tid, None)
    for name in pending.values():
        print("SEM RESPOSTA (verificar depois):", name)
    print(f"custo total: US$ {total:.2f}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
