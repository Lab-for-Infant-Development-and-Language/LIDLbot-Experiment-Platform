import webbrowser

from app.core.logging import Logger


def open_browser(url):
    try:
        webbrowser.open_new(url)
        Logger.info(f"Opened browser at {url}.")
    except Exception:
        Logger.action(f"Failed to open browser automatically. Please navigate to: {url}.")