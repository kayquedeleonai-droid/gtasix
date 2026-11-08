"""Anima imagens em clipes de vídeo no Runware (image-to-video) em modo assíncrono.

Uso: RUNWARE_KEY_FILE=<arquivo> python3 tools/runware_video.py jobs.json pasta_saida
jobs.json: lista de {"name","image" (caminho local),"prompt","duration": 5}
Modelo padrão: Seedance 1.0 Pro Fast (bytedance:2@2), 720p vertical (~US$ 0,07 por clipe de 5s).
"""
import base64, json, os, sys, time, uuid, urllib.request

API = "https://api.runware.ai/v1"
MODEL = "bytedance:2@2"


def key():
    return os.environ.get("RUNWARE_API_KEY") or open(os.environ["RUNWARE_KEY_FILE"]).read().strip()


def call(tasks):
    req = urllib.request.Request(API, data=json.dumps(tasks).encode(), headers={
        "Authorization": f"Bearer {key()}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def main(jobs_file, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    pending, total = {}, 0.0
    for j in json.load(open(jobs_file)):
        img = base64.b64encode(open(j["image"], "rb").read()).decode()
        tid = str(uuid.uuid4())
        resp = call([{"taskType": "videoInference", "taskUUID": tid, "model": j.get("model", MODEL),
                      "positivePrompt": j["prompt"], "duration": j.get("duration", 5),
                      "width": 704, "height": 1248, "inputs": {"frameImages": [f"data:image/png;base64,{img}"]},
                      "outputFormat": "MP4", "deliveryMethod": "async", "includeCost": True}])
        if resp.get("errors"):
            print("ERRO", j["name"], resp["errors"]); continue
        pending[tid] = j["name"]
        print("enviado:", j["name"])
    deadline = time.time() + 900
    while pending and time.time() < deadline:
        time.sleep(8)
        for tid, name in list(pending.items()):
            resp = call([{"taskType": "getResponse", "taskUUID": tid}])
            for e in resp.get("errors", []):
                print("ERRO", name, e.get("message")); pending.pop(tid, None)
            for d in resp.get("data", []):
                if d.get("videoURL"):
                    path = os.path.join(out_dir, name + ".mp4")
                    print("url:", d["videoURL"].split("/")[2])
                    try:
                        urllib.request.urlretrieve(d["videoURL"], path)
                        print("pronto:", path)
                    except Exception as ex:
                        print("FALHOU DOWNLOAD", name, d["videoURL"], ex)
                        open(os.path.join(out_dir, name + ".url"), "w").write(d["videoURL"])
                    total += d.get("cost") or 0
                    pending.pop(tid, None)
    for n in pending.values():
        print("SEM RESPOSTA:", n)
    print(f"custo total: US$ {total:.3f}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
