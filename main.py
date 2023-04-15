from converter import Converter
from reformatter import Formatter
from translater import Translater
from tqdm import tqdm
import sys
import time
import os
import shutil

PROCESSING_INDEX_FILE = 'result/processing_index.txt'
PROCESSING_TRANSLATE_FILE = 'result/processing_translate.txt'
RESULT_FILE = 'result/result.txt'

def main():
    args = sys.argv
    if (len(args) <= 1):
        target_pdf_file = "sample.pdf"
    else:
        target_pdf_file = args[1]

    processing_index = 0
    # 前回の実行で失敗している箇所を取得
    if(os.path.isfile(PROCESSING_INDEX_FILE)):
        f = open(PROCESSING_INDEX_FILE, 'r')
        processing_index = int(f.read())
        f.close()

    # 使用するクラスのインスタンス生成
    converter = Converter(target_pdf_file=target_pdf_file)
    formatter = Formatter()
    translater = Translater()

    # pdfからテキスト情報を抽出
    text = converter.convert()
    converter.close()

    # テキスト情報を精査して、文章単位で分割する
    text_shaped = formatter.reformat(text)
    sentencies = formatter.sentence_split(text_shaped)

    # chatGPTを使って和訳
    for i, sentence in enumerate(tqdm(sentencies)):
        if i < processing_index:
            continue

        # 進捗をtxtファイルに上書き
        with open(PROCESSING_INDEX_FILE, 'w') as file:
            file.write(str(i))

        jp_sentence = translater.translate(sentence)
        result = sentence + "\n" + jp_sentence + "\n\n"

        # 結果をtxtファイルに追記
        with open(PROCESSING_TRANSLATE_FILE, 'a') as file:
            file.write(result)

        time.sleep(25)

    # 結果ファイルをコピーによって作成
    shutil.copyfile(PROCESSING_TRANSLATE_FILE, RESULT_FILE)

    # 正常終了したらprocessing系のファイルを削除する
    if(os.path.isfile(PROCESSING_INDEX_FILE)):
        os.remove(PROCESSING_INDEX_FILE)
    if(os.path.isfile(PROCESSING_TRANSLATE_FILE)):
        os.remove(PROCESSING_TRANSLATE_FILE)

main()
