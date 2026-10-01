import os
from pathlib import Path


def safe_remove(path):

    try:

        path = Path(path)

        if path.exists():

            if path.is_file():

                path.unlink()

            elif path.is_dir():

                import shutil

                shutil.rmtree(path)

    except Exception as e:

        print(
            f"[Cleanup Error] {e}"
        )
