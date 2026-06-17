"""Запуск demo-сайта KazNLP (сайт + inference API на порту 8000)."""

from __future__ import annotations

import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PORT = 8000


def _port_open(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=0.8):
            return True
    except OSError:
        return False


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    setup = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "setup_demo_models.py")],
        cwd=ROOT,
    )
    if setup.returncode != 0:
        return setup.returncode

    if _port_open(HOST, PORT):
        print(f"\nПорт {PORT} уже занят.")
        print(f"Закройте другой процесс или откройте: http://{HOST}:{PORT}/\n")
        return 1

    print("\nЗапуск сервера…")
    print("  (импорт PyTorch может занять 20–40 сек — это нормально)\n")

    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "inference.app:app",
            "--host",
            HOST,
            "--port",
            str(PORT),
        ],
        cwd=ROOT,
    )

    url = f"http://{HOST}:{PORT}/"
    opened = False

    try:
        for _ in range(120):
            if proc.poll() is not None:
                print(f"\nСервер остановился (код {proc.returncode}).")
                print("Смотрите ошибку выше в логе uvicorn.\n")
                return proc.returncode or 1

            if _port_open(HOST, PORT):
                print(f"Сервер готов: {url}")
                print("Модели грузятся в фоне 1–3 мин — дождитесь исчезновения жёлтого баннера.\n")
                if not opened:
                    webbrowser.open(url)
                    opened = True
                return proc.wait()

            time.sleep(1)

        print("\nТаймаут: сервер не ответил за 2 минуты.")
        proc.terminate()
        return 1
    except KeyboardInterrupt:
        print("\nОстановка…")
        proc.terminate()
        proc.wait(timeout=10)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
