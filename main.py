from converter import Converter
from reformatter import Formatter
from translater import Translater
from tqdm import tqdm

def main():
    # 使用するクラスのインスタンス生成
    converter = Converter(target_pdf_file="attention_is_all_you_need.pdf")
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

    # 結果をtxtファイルに出力
    with open('result/result.txt', 'w') as file:
        file.write(result)

main()
