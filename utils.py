import os
import shutil


def safe_remove(
    path
):

    try:

        if not os.path.exists(
            path
        ):
            return

        if os.path.isdir(
            path
        ):

            shutil.rmtree(
                path,
                ignore_errors=True
            )

        else:

            os.remove(
                path
            )

    except Exception as error:

        print(
            "Cleanup error:",
            error
        )
