from pathlib import Path
from datetime import datetime

ROOT = Path("/Volumes/NO NAME/GIDEON/v1.0.0/Notes").resolve()

class NotesTool:

    name = "notes"

    async def create_note(self, title: str, content: str, category: str = "Capture"):
        # categories: capture, build log, knowledge note, experiment, decision log, project

        folder = ROOT / category

        folder.mkdir(parents=True, exist_ok=True)
        date_str = datetime.now().strftime("%Y-%m-%d")

        filename = f"{date_str}_{title}.md"

        path = folder / filename

        path.write_text(content)

        return str(path)
    

    async def read_note(self, category: str, title: str):
        path = ROOT / category / f"{title}.md"

        return path.read_text()


    async def search_notes(self, query: str):
        results = []

        for file in ROOT.rglob("*.md"):
            text = file.read_text()

            if query.lower() in text.lower():
                results.append(str(file))

        return results