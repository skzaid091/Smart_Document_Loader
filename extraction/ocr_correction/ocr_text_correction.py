import re
import json

class TextLLMCorrector:

    def __init__(self, llm_service):

        self.llm_service = llm_service
    

    def extract_json(self, response):

        if not response:
            raise ValueError("Empty response received.")

        response = response.strip()

        try:
            return json.loads(response)

        except Exception:
            pass

        # JSON Array
        match = re.search(r"\[.*\]", response, re.DOTALL)

        if match:
            return json.loads(match.group())

        # JSON Object
        match = re.search(r"\{.*\}", response, re.DOTALL)

        if match:
            return json.loads(match.group())

        raise ValueError(f"No JSON found:\n{response}")
    

    def correct_text(self, elements):
        """
        Improve OCR-derived text using an LLM.

        OCR engines occasionally introduce spelling
        mistakes such as:

            ResNet5O -> ResNet50
            mode1    -> model

        Elements are processed in a single batch
        to reduce API calls and cost.

        Only OCR-generated text should be sent
        through this correction stage.
        """

        # Build a lightweight payload that can be
        # mapped back to the original elements after
        # correction.
        payload = []

        for idx, element in enumerate(elements):
            payload.append({"id": idx, "text": element.text})

        prompt = f"""Correct only obvious OCR spelling mistakes.

        Rules:

        - Do not paraphrase.
        - Do not summarize.
        - Do not rewrite sentences.
        - Do not change numbers.
        - Do not change units.
        - Do not change dates.
        - Do not change names.
        - Do not change technical terms unless the OCR error is obvious.
        - Preserve the original wording and formatting whenever possible.

        Return ONLY valid JSON.
        Do not wrap the JSON in markdown.
        Do not add explanations, notes, or comments.

        - If you are uncertain whether a value is an OCR mistake, leave it unchanged.

        Input:

        {json.dumps(payload, indent=2)}
        """

        response = self.llm_service.invoke(
            prompt=prompt,
            temperature=0
        )

        corrected = self.extract_json(response)
        # corrected = json.loads(response)

        # Replace OCR text with the corrected
        # version returned by the model.
        for item in corrected:

            element = elements[item["id"]]
            element.text = item["text"]