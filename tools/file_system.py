import os


WORKSPACE_ROOT = os.path.abspath(
    os.getenv("WORKSPACE_ROOT", "/agent/workspace"))

def resolve_safe_path(path:str) -> str:
    #path should be extension of the WORKSPACE_ROOT if not then throw error
    full = os.path.normpath(os.path.join(WORKSPACE_ROOT, path))
    if not full.startswith(WORKSPACE_ROOT):
        raise ValueError(f"Path {path} is not a safe path under workspace root {WORKSPACE_ROOT}")
    return full

def create_folder(path:str) -> dict:
    safe_path = resolve_safe_path(path)
    os.makedirs(safe_path, exist_ok=True)
    return {"success": True, "path": safe_path}

def write_file(path:str, content:str) -> dict:
    safe_path = resolve_safe_path(path)
    with open(safe_path, 'w') as f:
        f.write(content)
    return {"success": True, "path": safe_path}

def read_file(path:str) -> dict:
    safe_path = resolve_safe_path(path)
    if not os.path.exists(safe_path):
        return {"success": False, "error": "File does not exist", "path": safe_path}
    with open(safe_path, 'r') as f:
        content = f.read()
    return {"success": True, "path": safe_path, "content": content}

def delete_file(path:str) -> dict:
    safe_path = resolve_safe_path(path)
    if not os.path.exists(safe_path):
        return {"success": False, "error": "File does not exist", "path": safe_path}
    os.remove(safe_path)
    return {"success": True, "path": safe_path}

def list_files(path:str = ".") -> dict:
    safe_path = resolve_safe_path(path)
    if not os.path.exists(safe_path):
        return {"success": False, "error": "Directory does not exist", "path": safe_path}
    items = []
    for item in os.listdir(safe_path):
        item_path = os.path.join(safe_path, item)
        items.append({
            "name": item,
            "type":"directory" if os.path.isdir(item_path) else "file",
            "size": os.path.getsize(item_path) if os.path.isfile(item_path) else None
        })
    return {"success": True, "path": safe_path, "items": items}
    
def edit_file(path:str, content:str) -> dict:
    safe_path = resolve_safe_path(path)
    if not os.path.exists(safe_path):
        return {"success": False, "error": "File does not exist", "path": safe_path}
    with open(safe_path, 'a') as f:
        f.write(content)
    return {"success": True, "path": safe_path}

def edit_replace_file(path:str,new_content:str,old_content:str) -> dict:
    safe_path = resolve_safe_path(path)
    if not os.path.exists(safe_path):
        return {"status":"error","message":"file does not exist"}
    with open(safe_path,"r",encoding="utf-8") as f:
        content = f.read()
    if old_content not in content:
        return {"status":"error","message":"old content to be replaced not found in file"}
    
    updated_content = content.replace(old_content,new_content) 
    with open(safe_path,"w",encoding="utf-8") as f:
        f.write(updated_content)
    return {"status":"success","path":safe_path}
