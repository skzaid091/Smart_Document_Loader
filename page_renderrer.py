import pymupdf


class PageRenderer:
    """
    Renders PDF pages into high-resolution images.

    Each rendered page is stored inside the document workspace and the
    corresponding page metadata is updated with the rendered image path
    and dimensions.
    """

    def __init__(self, workspace, dpi=300, base_dpi=72):
        """
        Initialize the page renderer.

        Parameters
        ----------
        workspace : Workspace
            Workspace used for storing rendered page images.

        dpi : int, default=300
            Rendering resolution.

        base_dpi : int, default=72
            Native PDF resolution used for scaling.
        """

        self.workspace = workspace

        self.dpi = dpi
        self.base_dpi = base_dpi


    def render(self, document):
        """
        Render all pages of a PDF document.

        Documents containing previous processing errors are returned
        unchanged.

        Parameters
        ----------
        document : Document

        Returns
        -------
        Document
        """

        if document.error:
            return document

        try:
            return self._render_pdf(document)

        except Exception as e:
            document.error = f"Page rendering failed: {e}"

            return document


    def _render_pdf(self, document):
        """
        Render each PDF page as a PNG image.

        Updates every PageContent object with:

        - image_path
        - rendered_width
        - rendered_height
        """

        zoom = self.dpi / self.base_dpi

        matrix = pymupdf.Matrix(zoom, zoom)

        with pymupdf.open(document.file_path) as pdf:

            for page in pdf:

                page_number = page.number + 1

                image_path = self.workspace.page_path(
                    document.document_id,
                    page_number
                )

                # Render the page at the requested resolution.
                pixmap = page.get_pixmap(matrix=matrix)

                pixmap.save(image_path)

                page_obj = document.pages[page.number]

                # Store rendering metadata for downstream processing.
                page_obj.image_path = image_path
                page_obj.rendered_width = pixmap.width
                page_obj.rendered_height = pixmap.height

        return document