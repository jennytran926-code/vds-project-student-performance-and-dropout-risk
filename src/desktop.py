"""Run the dashboard in a native desktop window (used for the .exe build)."""

from __future__ import annotations

import socket
import threading
import time

from app import TITLE, create_app

HOST = "127.0.0.1"


def _free_port() -> int:
    with socket.socket() as s:
        s.bind((HOST, 0))
        return s.getsockname()[1]


def _wait_for_server(port: int, timeout: float = 15.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with socket.create_connection((HOST, port), timeout=0.5):
                return
        except OSError:
            time.sleep(0.1)


def main() -> None:
    import webview  # imported lazily so the browser mode works without pywebview

    app = create_app()
    port = _free_port()
    server = threading.Thread(
        target=app.run, kwargs={"host": HOST, "port": port, "debug": False}, daemon=True
    )
    server.start()
    _wait_for_server(port)

    webview.create_window(TITLE, f"http://{HOST}:{port}", width=1440, height=920, min_size=(1000, 700))
    webview.start()  # blocks until the window is closed; the daemon server thread dies with it


if __name__ == "__main__":
    main()
