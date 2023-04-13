from dataclasses import dataclass
import os
import openai


@dataclass
class Translater():
    def __post_init__(self):
        self.token = os.environ["OPENAI_API_KEY"]

    def translate(self, text: str) -> str:
        return self._post("和訳して\n" + text)

    def _post(self, text: str) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": text},
            ],
        )

        return response.choices[0]["message"]["content"].strip()
