import base64
import mimetypes
from pathlib import Path


def encode_image(image_path: str | Path) -> str:
    """
    Encode an image as a Base64 string.

    Parameters
    ----------
    image_path : str | Path
        Path to the input image.

    Returns
    -------
    str
        Base64-encoded image.
    """

    image_path = Path(image_path)

    with image_path.open("rb") as file:

        return base64.b64encode(
            file.read()
        ).decode("utf-8")


def get_url(image_path: str | Path) -> str:
    """
    Convert an image into a Base64 data URL.

    The MIME type is inferred from the file extension. If it cannot be
    determined, ``image/jpeg`` is used as the default.

    Parameters
    ----------
    image_path : str | Path
        Path to the input image.

    Returns
    -------
    str
        Base64 data URL suitable for vision-language model APIs.
    """

    image_path = Path(image_path)

    mime_type, _ = mimetypes.guess_type(image_path)

    if mime_type is None:
        mime_type = "image/jpeg"

    return (
        f"data:{mime_type};base64,"
        f"{encode_image(image_path)}"
    )