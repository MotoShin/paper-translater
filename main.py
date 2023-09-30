from converter import ConvertPDF2text
from reformatter import Formatter2
from translater import Translater2
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

    converter = ConvertPDF2text(args[1:])
    formatter = Formatter2()
    translater = Translater2()

    processing_index = 0
    # 前回の実行で失敗している箇所を取得
    if(os.path.isfile(PROCESSING_INDEX_FILE)):
        f = open(PROCESSING_INDEX_FILE, 'r')
        processing_index = int(f.read())
        f.close()

    text = converter.convert_pdf_to_text()
    chapters = formatter.format(text)

    # chatGPTを使って和訳
    for i, sentence in enumerate(tqdm(chapters)):
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
