import os
from dataclasses import dataclass

@dataclass
class Settings:
    workspace_root: str = os.getenv("WORKSPACE_ROOT", "")
    log_level: str = os.getenv("LOG_LEVEL","INFO")

settings = Settings()