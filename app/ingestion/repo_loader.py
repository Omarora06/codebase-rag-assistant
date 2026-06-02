from pathlib import Path

def load_repository(repo_path):
    files = []

    for file_path in Path(repo_path).rglob("*.py"):
        try:
            content = file_path.read_text(
                encoding="utf-8"
            )

            files.append({
                "path": str(file_path),
                "content": content
            })

        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    return files