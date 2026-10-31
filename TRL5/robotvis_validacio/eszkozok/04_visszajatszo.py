#!/usr/bin/env python3
"""
04_visszajatszo.py - valós cellás CSV-k visszajátszása a RobotVis-nek, robot és áramforrás nélkül (T5-08).

A RobotVis két forrásból kap adatot:
  1. a RobotComm-tól TCP-n (127.0.0.1:9999) a pozíciót: "X, Y, Z, Rx, Ry, Rz;"
  2. az áramforrás webes felületéről Seleniummal a TorchSignal, feszültség, áram, huzalsebesség értékét.
     A RobotVis-ben van beépített helyi tesztoldal-mód (open_local_test_site): ekkor a http://127.0.0.1:8000/
     címet olvassa. Ez a program ezt az oldalt is kiszolgálja.

Ez a program a RobotComm helyére ül (a RobotComm-ot NEM kell elindítani), és a megadott CSV-k sorait az
eredeti időzítéssel küldi. Minden küldést naplóz (kuldesi_naplo.csv), hogy a RobotVis saját CSV-jével
összevetve mérhető legyen a késés, az adatvesztés és a megállás (05_visszajatszas_kiertekelo.py).

Csak a Python standard könyvtárát használja. Futtatható a RobotVis mellé csomagolt Pythonnal is:
    RobotVis\\addons\\pythonscript\\windows-64\\python.exe 04_visszajatszo.py --csv a.csv b.csv c.csv

Menete:
    1. A RobotVis Main.tscn fájljában a WeldUnitConnectorBrowser csomópont alá:  open_local_test_site = true
       (lásd README; a módosítás előtt a fájlról másolat készül).
    2. Ez a program elindul, és várja a RobotVis csatlakozását.
    3. A RobotVis elindul; magától csatlakozik a 9999-es portra. A kezelő bekapcsolja a böngésző-kapcsolatot.
    4. Futásonként: a kezelő beírja a Log File Prefix mezőbe a futás nevét, bekapcsolja a Recording-ot,
       majd itt Entert nyom. A futás végén kikapcsolja a Recording-ot.
"""
import argparse, csv, json, os, socket, sys, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

STATE = {"seq": 0, "torch": 0, "voltage": 0.0, "current": 0.0, "wfs": 0.0}
LOCK = threading.Lock()

PAGE = """<!doctype html><html><head><meta charset="utf-8"><title>Visszajátszó – áramforrás-teszt</title>
<style>body{font-family:sans-serif} .rowElement{display:flex;gap:12px} .Value{min-width:120px}</style></head>
<body><h3>T5-08 visszajátszó – helyi teszt-oldal (nem valós áramforrás)</h3>
<div id="tablecontainer_output">%ROWS%</div>
<script>
async function tick(){
  try{
    const r = await fetch('/state', {cache:'no-store'}); const s = await r.json();
    const rows = document.getElementsByClassName('rowElement');
    rows[4].querySelector('.Value').title = 'TorchSignal ' + s.torch + '\\nseq ' + s.seq;
    rows[4].querySelector('.Value').textContent = String(s.torch);
    rows[35].querySelector('.Value').textContent = s.voltage.toFixed(2) + ' V';
    rows[36].querySelector('.Value').textContent = s.current.toFixed(1) + ' A';
    rows[37].querySelector('.Value').textContent = s.wfs.toFixed(2) + ' m/min';
  }catch(e){}
  setTimeout(tick, 10);
}
tick();
</script></body></html>"""


def make_page():
    rows = []
    for i in range(40):
        # a .Value és a magyar nyelvű .érték osztály is szerepel, mert a RobotVis a Windows nyelve szerint választ
        rows.append(f'<div class="rowElement"><span>sor {i}</span><div class="Value érték" title="x 0\n">0</div></div>')
    return PAGE.replace("%ROWS%", "".join(rows)).encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    page = None

    def do_GET(self):
        if self.path.startswith("/state"):
            with LOCK:
                body = json.dumps(STATE).encode()
            ctype = "application/json"
        else:
            body = Handler.page
            ctype = "text/html; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass


def load_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    t0 = int(rows[0]["SysTimeMsecs"])
    out = []
    for i, r in enumerate(rows):
        out.append(dict(i=i, t=int(r["SysTimeMsecs"]) - t0,
                        pos=tuple(float(r[k]) for k in ("X", "Y", "Z", "Rx", "Ry", "Rz")),
                        torch=int(r["TorchSignal"]), voltage=float(r["Voltage"]),
                        current=float(r["Current"]), wfs=float(r["WireFeedSpeed"])))
    return out


def now_ms():
    return time.time() * 1000.0  # ugyanaz a rendszeróra, mint a RobotVis get_system_time_msecs()


IVJEL = False  # --ivjel: a TorchSignal 7. mezőként a pozícióüzenetben is megy (mint a javított RobotComm-nál)


def run_one(conn, run_id, rows, speed, log):
    last_pos, last_pow, last_arc = None, None, None
    start = now_ms()
    seq = 0
    for r in rows:
        target = start + r["t"] / speed
        while True:
            d = target - now_ms()
            if d <= 0:
                break
            time.sleep(min(d / 1000.0, 0.002))
        pw = (r["torch"], r["voltage"], r["current"], r["wfs"])
        if pw != last_pow:
            with LOCK:
                STATE.update(seq=r["i"], torch=r["torch"], voltage=r["voltage"], current=r["current"], wfs=r["wfs"])
            log.writerow([run_id, "aramforras", r["i"], f"{now_ms():.1f}", r["torch"], r["voltage"], r["current"], r["wfs"]])
            last_pow = pw
        if r["pos"] != last_pos or (IVJEL and r["torch"] != last_arc):
            if IVJEL:
                msg = "{0}, {1}, {2}, {3}, {4}, {5}, {6};".format(*r["pos"], r["torch"])
                last_arc = r["torch"]
            else:
                msg = "{0}, {1}, {2}, {3}, {4}, {5};".format(*r["pos"])
            try:
                conn.sendall(msg.encode("ascii"))
            except OSError as e:
                print(f"  A kapcsolat megszakadt: {e}")
                return False
            log.writerow([run_id, "pozicio", r["i"], f"{now_ms():.1f}", *r["pos"]])
            last_pos = r["pos"]
            seq += 1
    print(f"  {run_id}: {len(rows)} sor, {seq} pozícióüzenet elküldve, {(now_ms() - start) / 1000:.1f} s")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", nargs="+", required=True, help="a visszajátszandó valós CSV-k (futásonként egy)")
    ap.add_argument("--port", type=int, default=9999)
    ap.add_argument("--http-port", type=int, default=8000)
    ap.add_argument("--speed", type=float, default=1.0, help="1.0 = eredeti időzítés")
    ap.add_argument("--out", default="visszajatszas_naplo")
    ap.add_argument("--ivjel", action="store_true", help="a TorchSignal a pozícióüzenet 7. mezőjeként is megy (javított RobotComm szimulálása)")
    a = ap.parse_args()
    global IVJEL
    IVJEL = a.ivjel

    os.makedirs(a.out, exist_ok=True)
    Handler.page = make_page()
    httpd = ThreadingHTTPServer(("127.0.0.1", a.http_port), Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    print(f"Teszt-oldal: http://127.0.0.1:{a.http_port}/")

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", a.port))
    srv.listen(1)
    print(f"Várom a RobotVis csatlakozását a 127.0.0.1:{a.port} porton (a RobotComm ne fusson)...")
    conn, addr = srv.accept()
    conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    print(f"RobotVis csatlakozott: {addr}")

    logf = open(os.path.join(a.out, "kuldesi_naplo.csv"), "w", newline="", encoding="utf-8")
    log = csv.writer(logf)
    log.writerow(["futas", "fajta", "forras_sor", "t_kuldes_ms", "a", "b", "c", "d", "e", "f"])
    meta = dict(indulas_ms=now_ms(), csv=[os.path.abspath(p) for p in a.csv], speed=a.speed, port=a.port, ivjel=a.ivjel)

    for k, path in enumerate(a.csv, 1):
        rows = load_csv(path)
        run_id = f"futas{k}"
        with LOCK:
            STATE.update(seq=0, torch=rows[0]["torch"], voltage=rows[0]["voltage"], current=rows[0]["current"], wfs=rows[0]["wfs"])
        input(f"\n[{run_id}] {os.path.basename(path)}: a RobotVis-ben Log File Prefix = {run_id}, Recording BE, majd Enter... ")
        ok = run_one(conn, run_id, rows, a.speed, log)
        logf.flush()
        print(f"  [{run_id}] kész. Kapcsold KI a Recording-ot.")
        if not ok:
            break
    meta["vege_ms"] = now_ms()
    json.dump(meta, open(os.path.join(a.out, "meta.json"), "w"), indent=1, ensure_ascii=False)
    logf.close()
    input("\nMinden futás kész. Enter a kilépéshez (előtte a RobotVis Recording legyen KI)... ")
    conn.close()
    httpd.shutdown()


if __name__ == "__main__":
    main()
