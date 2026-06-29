from pathlib import Path

import gdown

from config import CONFIG


# Google Drive file ID for the trained DocLayout-YOLO model.
LAYOUT_MODEL_FILE_ID = "1jWADlbEukps--JX4Qves-qWW-cuc4OPz"


def download_layout_model():
    """
    Download the DocLayout-YOLO model if it is not already available.
    """

    model_dir = Path(
        CONFIG["layout_detection"]["layout_model_base_path"]
    )
    model_dir.mkdir(parents=True, exist_ok=True)

    model_path = Path(
        CONFIG["layout_detection"]["layout_model_path"]
    )

    # Skip downloading if the model already exists.
    if model_path.exists():
        print(f"Layout model already exists: {model_path}")
        return

    print("Downloading DocLayout-YOLO model...")

    url = f"https://drive.google.com/uc?id={LAYOUT_MODEL_FILE_ID}"

    gdown.download(
        url=url,
        output=str(model_path),
        quiet=False
    )

    if not model_path.exists():
        raise RuntimeError(
            "Failed to download the DocLayout-YOLO model."
        )


def download_prerequisites():
    """
    Download all required models and resources.
    """

    download_layout_model()


if __name__ == "__main__":
    download_prerequisites()