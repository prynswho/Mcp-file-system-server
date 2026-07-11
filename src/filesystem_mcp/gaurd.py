import os
from .errors import PathNotAllowed
from .config import settings




def resolve_safe_path(path:str) -> str:
    #path should be extension of the WORKSPACE_ROOT if not then throw error
    full = os.path.normpath(os.path.join(settings.workspace_root, path))
    if not full.startswith(settings.workspace_root):
        raise PathNotAllowed(f"Path {path} is not a safe path under workspace root {settings.workspace_root}")
    return full
