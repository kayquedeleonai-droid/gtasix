"""Gera imagens no Runware em modo assíncrono e baixa os arquivos.

Uso: RUNWARE_KEY_FILE=<arquivo> python3 tools/runware_image.py jobs.json pasta_saida
jobs.json: lista de {"name": "...", "prompt": "...", "width": 768, "height": 1344, "model": "..."}
"""
import base64, json, os, sys, time, uuid, urllib.request

API = "https://api.runware.ai/v1"
DEFAULT_MODEL = "runware:400@2"  # FLUX.2 [klein] 9B: rápido e muito barato


def key():
    return os.environ.get("RUNWARE_API_KEY") or open(os.environ["RUNWARE_KEY_FILE"]).read().strip()


def call(tasks):
    req = urllib.request.Request(API, data=json.dumps(tasks).encode(), headers={
        "Authorization": f"Bearer {key()}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)


def main(jobs_file, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    pending, total = {}, 0.0
    for j in json.load(open(jobs_file)):
        tid = str(uuid.uuid4())
        resp = call([{"taskType": "imageInference", "taskUUID": tid,
                      "model": j.get("model", DEFAULT_MODEL), "positivePrompt": j["prompt"],
                      "width": j.get("width", 768), "height": j.get("height", 1344),
                      "numberResults": 1, "outputFormat": "PNG", "outputType": "base64Data", "deliveryMethod": "async",
                      "includeCost": True}])
        if resp.get("errors"):
            print("ERRO", j["name"], resp["errors"]); continue
        pending[tid] = j["name"]
    deadline = time.time() + 600
    while pending and time.time() < deadline:
        time.sleep(4)
        for tid, name in list(pending.items()):
            resp = call([{"taskType": "getResponse", "taskUUID": tid}])
            for e in resp.get("errors", []):
                print("ERRO", name, e.get("message")); pending.pop(tid, None)
            for d in resp.get("data", []):
                if d.get("imageBase64Data"):
                    path = os.path.join(out_dir, name + ".png")
                    open(path, "wb").write(base64.b64decode(d["imageBase64Data"]))
                    total += d.get("cost") or 0
                    print("pronto:", path)
                    pending.pop(tid, None)
    for n in pending.values():
        print("SEM RESPOSTA:", n)
    print(f"custo total: US$ {total:.4f}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
