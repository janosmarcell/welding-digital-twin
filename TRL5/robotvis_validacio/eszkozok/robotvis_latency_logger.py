"""Minimális késleltetés-naplózó a RobotVis-be illesztéshez (T5-08).

Használat a RobotVis Python-oldalán (a hívási pontokat a szerző illeszti a saját kódjába):
    from robotvis_latency_logger import LatencyLog
    log = LatencyLog("robotvis_latency.csv", run_id="futas1")
    ...adatcsomag megérkezésekor/feldolgozásakor:   log.on_receive(seq)
    ...a kirajzolás (frissítés) után:                log.on_display(seq)
    ...a futás végén:                                log.close()
Mindkét időbélyeg ugyanazon a monotonikus órán készül (time.perf_counter), ezért különbségük megbízható.
"""
import csv, threading, time


class LatencyLog:
    def __init__(self, path, run_id):
        self._f = open(path, "a", newline="", encoding="utf-8")
        self._w = csv.writer(self._f)
        if self._f.tell() == 0:
            self._w.writerow(["run_id", "seq", "t_recv_ms", "t_display_ms"])
        self._run = run_id
        self._recv = {}
        self._lock = threading.Lock()

    @staticmethod
    def _now_ms():
        return time.perf_counter() * 1000.0

    def on_receive(self, seq):
        with self._lock:
            self._recv[seq] = self._now_ms()

    def on_display(self, seq):
        t = self._now_ms()
        with self._lock:
            r = self._recv.pop(seq, None)
            if r is not None:
                self._w.writerow([self._run, seq, f"{r:.3f}", f"{t:.3f}"])

    def close(self):
        with self._lock:
            self._f.close()
