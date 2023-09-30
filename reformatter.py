from dataclasses import dataclass
import re
import nltk
import argparse


@dataclass
class Formatter:
    def reformat(self, text: str) -> str:
        text_shaped = text

        # 論文中のアブストと参考文献の章の文字列を取得
        abst_str = re.findall(r"abstract", text, re.IGNORECASE)[0]
        ref_str = re.findall(r"references", text, re.IGNORECASE)[-1]

        # アブスト以前と参考文献以降は使用しないので削除する
        text_shaped = text_shaped[
            text_shaped.find(abst_str) : text_shaped.find(ref_str)
        ]

        text_shaped = re.sub("([a-z])(\n)+", r"\1 ", text_shaped)
        text_shaped = re.sub("(\n)+([a-z])", r"\2 ", text_shaped)
        text_shaped = re.sub(" \[(\d+, )*\d+\]", "", text_shaped)

        return text_shaped

    def sentence_split(self, text: str) -> list:
        return nltk.sent_tokenize(text)


@dataclass
class Formatter2:
    def __init__(self, argv: list):
        self.chapter_pattern = "^\d\.(\d\.)*\s?[A-z]+"

        # コマンドライン引数の解析
        parser = argparse.ArgumentParser()  # インスタンス作成
        parser.add_argument(
            "chapter_pattern",
            type=str,
            default=self.chapter_pattern,
            help="chapterの番号フォーマット",
        )

        args = parser.parse_args(argv)
        print(args)

        self.chapter_pattern = args.chapter_pattern

    def format(self, text: str):
        # 改行で文字列分割
        lines = text.split("\n")

        chapters = []
        chapter = ""
        chapter_pattern = self.chapter_pattern
        for line in lines:
            flag = re.search(chapter_pattern, line)
            if flag:
                chapters.append(chapter)
                chapter = ""
                flag = False
            chapter += line + "\n"
        chapters.append(chapter)

        # for i, chapter in enumerate(chapters):
        #     print("Chapter {}".format(i) + '\n' + chapter + '\n')
        return chapters
