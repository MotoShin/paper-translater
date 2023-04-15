from converter import Converter
from reformatter import Formatter
from translater import Translater
from tqdm import tqdm
import sys
import time

def main():
    args = sys.argv
    if (len(args) <= 1):
        target_pdf_file = "sample.pdf"
    else:
        target_pdf_file = args[1]

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
    result = ""
    for sentence in tqdm(sentencies):
        jp_sentence = translater.translate(sentence)
        result += sentence + "\n" + jp_sentence + "\n\n"
        time.sleep(25)

    # 結果をtxtファイルに出力
    with open('result/result.txt', 'w') as file:
        file.write(result)

main()
