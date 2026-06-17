"""Start language labeler from KazNLP project root."""

import socket
import sys

import uvicorn


def find_free_port(start: int = 8000, attempts: int = 20) -> int:
    for port in range(start, start + attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise SystemExit(f"No free port in range {start}-{start + attempts - 1}")


if __name__ == "__main__":
    preferred = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    port = find_free_port(preferred)

    if port != preferred:
        print(f"Port {preferred} is busy (old server still running?).")
        print(f"Using port {port} instead.")

    url = f"http://127.0.0.1:{port}"
    print(f"KazNLP Language Labeler - open {url} in your browser")
    print("Press Ctrl+C here to stop the server.")

    uvicorn.run(
        "main:app",
        app_dir="labeling_service",
        host="127.0.0.1",
        port=port,
        reload=True,
    )
