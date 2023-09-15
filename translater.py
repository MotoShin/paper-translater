from dataclasses import dataclass
import os
import openai
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
) 


@dataclass
class Translater():
    def __post_init__(self):
        self.token = os.environ["OPENAI_API_KEY"]

    def translate(self, text: str) -> str:
        return self._post("和訳して\n" + text)

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(5))
    def _post(self, text: str) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": text},
            ],
        )

        return response.choices[0]["message"]["content"].strip()

@dataclass
class Translater2():
    def __post_init__(self):
        self.token = os.environ["OPENAI_API_KEY"]

    def translate(self, text: str) -> str:
        return self._post("下記の文章を英文はそのままで日本語は英訳してください\n" + text)

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(5))
    def _post(self, text: str) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": text},
            ],
        )

        return response.choices[0]["message"]["content"].strip()
