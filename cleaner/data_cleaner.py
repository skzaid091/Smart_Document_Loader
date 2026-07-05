class DataCleaner:
    """
    Remove low-value or unsuccessfully extracted elements
    from the document before chunking and indexing.

    Rules:
    - Remove figures with no figure_data.
    - Remove tables with no table_data.
    - Remove formulas with no formula_data.
    - Remove low-value figures (e.g. signatures, stamps).
    - Remove elements with empty text.
    """

    USELESS_TYPES = {
        "signature",
        "stamp",
    }

    def process(self, document):
        """
        Filter document elements based on their extracted data.
        """

        filtered = []

        for element in document.elements:

            # Figures
            if element.element_type == "figure":

                if not element.figure_data:
                    continue

                if element.figure_data.figure_type in self.USELESS_TYPES:
                    continue

            # Tables
            elif element.element_type == "table":

                if not element.table_data:
                    continue

            # Formulas
            elif element.element_type in ["formula", "isolate_formula"]:

                if not element.formula_data:
                    print("excaping ----------------------------------- element : ", element, "\n")
                    continue

            else:
                # Remove elements with no text
                if not element.text or not element.text.strip():
                    continue

            filtered.append(element)

        document.elements = filtered

        return document