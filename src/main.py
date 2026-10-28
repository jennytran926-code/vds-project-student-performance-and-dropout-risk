"""Command-line entry point: `python src/main.py [--desktop] [--port PORT]`."""

from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Student dropout risk dashboard")
    parser.add_argument("--desktop", action="store_true", help="open in a native window instead of the browser")
    parser.add_argument("--port", type=int, default=8050, help="port for browser mode (default 8050)")
    parser.add_argument("--no-debug", action="store_true", help="disable Dash hot reload and dev tools")
    args = parser.parse_args()

    if args.desktop:
        from desktop import main as run_desktop

        run_desktop()
        return

    from app import create_app

    print(f"Dashboard running at http://127.0.0.1:{args.port}")
    create_app().run(host="127.0.0.1", port=args.port, debug=not args.no_debug)


if __name__ == "__main__":
    main()
