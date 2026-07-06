from .base_formula_recognizer import BaseFormulaRecognizer

from ...data_models import FormulaData


class VLMFormulaRecognizer(BaseFormulaRecognizer):
    """
    Recognize mathematical formulas using a multimodal LLM.

    The model extracts:
    - Formula text
    - LaTeX representation
    - Short explanation
    """

    def __init__(self, vlm_service):

        self.vlm_service = vlm_service


    def recognize(self, image_path):
        """
        Recognize a mathematical formula from an image.

        Parameters
        ----------
        image : str | Path
            Path to the cropped formula image.

        Returns
        -------
        FormulaData
            Structured representation of the recognized formula.
        """

        prompt = """
        Analyze the mathematical formula in the provided image. 
        
        Return **only one valid JSON object**. 
        
        Do NOT: 
        - add Markdown 
        - use ```json code fences 
        - include headings 
        - include explanations outside the JSON 
        - include any text before or after the JSON 
        
        The response must begin with `{` and end with `}`. 
        
        Tasks: 
        1. Extract the entire formula exactly as shown, preserving all variables, function names, operators, subscripts, superscripts, equality signs, and mathematical symbols. Represent it as a plain mathematical expression, not LaTeX. Do not use LaTeX commands such as \frac, \sqrt, \sin, \cos, \left, \right, or \text. Instead, use standard mathematical notation such as /, sqrt(), sin(), cos(), ^, *, and _.
        2. Generate the equivalent **valid LaTeX** expression. 
        3. Provide a concise 2–4 sentence explanation. 
        4. Preserve all mathematical notation and symbols. 
        5. If any symbol is unclear, make the best reasonable interpretation. 
        
        JSON schema: 
        { 
            "formula": "<plain mathematical expression without LaTeX commands>", 
            "latex": "<equivalent valid LaTeX expression>", 
            "explanation": "<2-4 sentence explanation>" 
        }
        """

        response = self.vlm_service.invoke(
            image_path=image_path, 
            prompt=prompt
        )

        result = self.extract_json(response)

        return FormulaData(
            formula=result.get("formula", "").strip(),
            latex=result.get("latex", "").strip(),
            explanation=result.get("explanation", "").strip()
        )