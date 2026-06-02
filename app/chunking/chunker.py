import ast


def chunk_python_file(file_data):
    chunks = []

    try:
        tree = ast.parse(file_data["content"])

        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):

                chunk = {
                    "path": file_data["path"],
                    "type": "function",
                    "name": node.name,
                    "line": node.lineno,
                    "content": ast.get_source_segment(
                        file_data["content"],
                        node
                    )
                }

                chunks.append(chunk)

            elif isinstance(node, ast.ClassDef):

                chunk = {
                    "path": file_data["path"],
                    "type": "class",
                    "name": node.name,
                    "line": node.lineno,
                    "content": ast.get_source_segment(
                        file_data["content"],
                        node
                    )
                }

                chunks.append(chunk)

    except Exception:
        pass

    return chunks