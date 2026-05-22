import re
from pathlib import Path

DEFAULT_REQUIRED_FILES = {
    Path("resources/configuration/experiment_config.json"): "experiment",
    Path("resources/configuration/sets_sequences_config.json"): "sets",
    Path("resources/configuration/modules_config.json"): "modules",
    Path("resources/configuration/blocks_config.json"): "blocks"
}

# TODO: Please update to Enums
PROMPT_TYPES = {
    "text", 
    "image", 
    "survey"
}

RESPONSE_TYPES = {
    "text", 
    "audio"
}

CONTENT_TYPES = {
    "text", 
    "image"
}

TEMPLATES = { 
    "web_content_embed",
    "web_link",
    "content_viewer",
    "session_code_display",
    "session_code_entry",
    "prompter",
    "voicebot",
    "chatbot"
}

ASSET_PREFIX = "/session/assets/"