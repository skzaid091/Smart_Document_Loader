import gdown
import zipfile
from pathlib import Path

from .config import CONFIG


# Google Drive file ID for the pretrained DocLayout-YOLO model.
LAYOUT_MODEL_FILE_ID = "1jWADlbEukps--JX4Qves-qWW-cuc4OPz"
PADDLE_OCR_FILE_ID = "1bo0Avx9EUP_QQYOS6bQKS2-KtrsfLkOq"


def download_layout_model():
    """
    Download the DocLayout-YOLO model if it is not already
    available in the local models directory.
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


def download_paddle_ocr_models():
    """
    Download PaddleOCR models from Google Drive and extract them
    into the local models directory if they are not already present.
    """

    models_dir = Path(
        CONFIG["ocr"]["ocr_models_base_path"]
    )
    models_dir.mkdir(parents=True, exist_ok=True)

    paddle_dir = models_dir / "paddle_ocr"

    # Skip if already extracted
    if paddle_dir.exists():
        print(f"PaddleOCR models already exist: {paddle_dir}")
        return

    zip_path = models_dir / "paddle_ocr.zip"

    print("Downloading PaddleOCR models...")

    url = f"https://drive.google.com/uc?id={PADDLE_OCR_FILE_ID}"

    gdown.download(
        url=url,
        output=str(zip_path),
        quiet=False
    )

    if not zip_path.exists():
        raise RuntimeError(
            "Failed to download PaddleOCR models."
        )

    print("Extracting PaddleOCR models...")

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(models_dir)

    zip_path.unlink()

    print("PaddleOCR models downloaded successfully.")



def download_prerequisites():
    """
    Download all models and resources required by the
    document processing pipeline.
    """

    download_layout_model()
    download_paddle_ocr_models()


if __name__ == "__main__":
    download_prerequisites()