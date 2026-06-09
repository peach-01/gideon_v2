from pathlib import Path

ROOT = Path("/Volumes/NO NAME/GIDEON/v1.0.0").resolve()

# ------------ HELPERS ------------
def validate_path(path: Path):
    path = path.resolve()

    if ROOT not in path.parents and path != ROOT:
        raise PermissionError("Outside Sandbox")
    
    return path


def build_filename(project: str, discipline: str, doc_type: str, title: str, revision: str = "RevA", ext: str = "md"):
    safe_title = title.replace(" ", "_")

    return (f"{project}-{discipline}-{doc_type}-{safe_title}-{revision}.{ext}")


def project_path(project, discipline, doc_type):
    return (ROOT / "Projects" / project / discipline / doc_type)


# ------------- CORE --------------
class FileSystemTool:

    name = "filesystem"

    async def save_document(self, project, discipline, doc_type, title, content, revision="RevA", ext="md"):
        filename = build_filename(project, discipline, doc_type, title, revision, ext)
        folder = (ROOT / "Projects" / project / discipline / doc_type)

        folder.mkdir(parents=True, exist_ok=True)

        file = folder / filename

        file.write_text(content)

        return str(file)
    

    async def read_file(self, path: str):
        file = validate_path(path)

        return Path(file).read_text()


    async def write_file(self, path: str, content: str):
        file = validate_path(path)

        file.parent.mkdir(parents=True, exist_ok=True)

        file.write_text(content)
        
        return {"status": "success"}
    

    async def list_directory(self, path="."):
        folder = validate_path(path)

        return [x.name for x in folder.iterdir()]
    

    async def exists(self, path: str):
        return validate_path(path).exists()
    

    async def delete_file(self, path: str):
        validate_path(path).unlink()

        return {"status": "deleted"}