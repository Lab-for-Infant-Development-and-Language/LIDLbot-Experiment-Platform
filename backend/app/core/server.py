import sys

from werkzeug.serving import make_server

from app import create_app
from app.core.browser import open_browser
from app.core.logging import Logger


def run_server():
    Logger.info("Starting LIDLbot...")

    try:
        app = create_app()
    except Exception:
        Logger.fail("LIDLbot failed to start.")
        sys.exit(1)
    
    Logger.info("Initializing...")
    Logger.newline()

    server = make_server("127.0.0.1", 0, app)
    port = server.socket.getsockname()[1]
    url = f"http://127.0.0.1:{port}"

    Logger.info(f"Server running on {url}.")

    open_browser(f"{url}/session/page/0/0")

    try:
        server.serve_forever()
    finally:
        server.shutdown()
        Logger.info("LIDLbot terminated.")