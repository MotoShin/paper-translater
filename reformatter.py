from dataclasses import dataclass
import re
import nltk

@dataclass
class Formatter():
    def reformat(self, text: str) -> str:
        text_shaped = text

        # 論文中のアブストと参考文献の章の文字列を取得
        abst_str = re.findall(r'abstract', text, re.IGNORECASE)[0]
        ref_str = re.findall(r'references', text, re.IGNORECASE)[-1]

        # アブスト以前と参考文献以降は使用しないので削除する
        text_shaped = text_shaped[text_shaped.find(abst_str):text_shaped.find(ref_str)]

        text_shaped = re.sub("([a-z])(\n)+", r'\1 ', text_shaped)
        text_shaped = re.sub("(\n)+([a-z])", r'\2 ', text_shaped)
        text_shaped = re.sub(" \[(\d+, )*\d+\]", '', text_shaped)

        return text_shaped

    def sentence_split(self, text: str) -> list:
        return nltk.sent_tokenize(text)
