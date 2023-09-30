from converter import ConvertPDF2text
from reformatter import Formatter2
from translater import Translater2
from tqdm import tqdm
import sys
import time
import os
import shutil
import argparse

PROCESSING_INDEX_FILE = "result/processing_index.txt"
PROCESSING_TRANSLATE_FILE = "result/processing_translate.txt"
RESULT_FILE = "result/result.txt"


def main():
    args = sys.argv

    if not args:
        return

    # コマンドライン引数の解析
    parser = argparse.ArgumentParser()  # インスタンス作成
    parser.add_argument("--input_path", type=str, help="入力ファイル名")  # 引数定義
    parser.add_argument(
        "--output_path",
        default="result/extraction.txt",
        type=str,
        help="出力ファイル名(default:extraction.txt)",
    )  # 引数定義
    parser.add_argument(
        "-b",
        "--border",
        type=int,
        metavar="n",
        default=1,
        help="段組みの切れ目  0の場合、用紙幅の半分(default:%(default)s)",
    )  # 引数定義
    parser.add_argument(
        "-f",
        "--footer",
        type=int,
        metavar="n",
        default=30,
        help="フッター位置(default:%(default)s)",
    )  # 引数定義
    parser.add_argument(
        "-t",
        "--top",
        type=int,
        metavar="n",
        default=1000,
        help="ヘッダー位置(default:%(default)s)",
    )  # 引数定義
    parser.add_argument(
        "-s",
        "--s_page",
        type=int,
        metavar="n",
        default=1,
        help="開始ページ(default:%(default)s)",
    )  # 引数定義
    parser.add_argument(
        "-e",
        "--e_page",
        type=int,
        metavar="n",
        default=0,
        help="終了ページ(0:最終)(default:%(default)s)",
    )  # 引数定義
    parser.add_argument(
        "--chapter_pattern",
        type=str,
        default="^\d\.(\d\.)*\s?[A-z]+",
        help="chapterの番号フォーマット",
    )  # 引数定義

    args = parser.parse_args(args[1:])  # 引数の解析
    print(args)  # 引数の参照
    input_path = args.input_path
    start_page = args.s_page
    last_page = args.e_page
    output_path = args.output_path
    border = args.border
    footer = args.footer
    header = args.top
    chapter_pattern = args.chapter_pattern

    converter = ConvertPDF2text(
        input_path=input_path,
        output_path=output_path,
        border=border,
        footer=footer,
        header=header,
        start_page=start_page,
        last_page=last_page,
    )
    formatter = Formatter2(chapter_pattern)
    translater = Translater2()

    processing_index = 0
    # 前回の実行で失敗している箇所を取得
    if os.path.isfile(PROCESSING_INDEX_FILE):
        f = open(PROCESSING_INDEX_FILE, "r")
        processing_index = int(f.read())
        f.close()

    text = converter.convert_pdf_to_text()
    chapters = formatter.format(text)

    # chatGPTを使って和訳
    for i, sentence in enumerate(tqdm(chapters)):
        if i < processing_index:
            continue

        # 進捗をtxtファイルに上書き
        with open(PROCESSING_INDEX_FILE, "w") as file:
            file.write(str(i))

        jp_sentence = translater.translate(sentence)
        result = sentence + "\n" + jp_sentence + "\n\n"

        # 結果をtxtファイルに追記
        with open(PROCESSING_TRANSLATE_FILE, "a") as file:
            file.write(result)

        time.sleep(25)

    # 結果ファイルをコピーによって作成
    shutil.copyfile(PROCESSING_TRANSLATE_FILE, RESULT_FILE)

    # 正常終了したらprocessing系のファイルを削除する
    if os.path.isfile(PROCESSING_INDEX_FILE):
        os.remove(PROCESSING_INDEX_FILE)
    if os.path.isfile(PROCESSING_TRANSLATE_FILE):
        os.remove(PROCESSING_TRANSLATE_FILE)


main()
