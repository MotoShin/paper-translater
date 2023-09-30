# paper-translater
pdfの英語論文をテキスト化した上で機械翻訳をかまして日本語化します。
（日本語論文 to 英語論文にも対応しました。）
OpenAIのAPIの都合上、文字列を分割する必要があり実行時間との兼ね合いから章（チャプター）毎の分割としています。

## How to use
[OpenAI](https://platform.openai.com/)にてAPI Keyの発行を行ってください。（本スクリプトはchatGPTを使用して和訳を行なっています）
API Keyを発行したらターミナルにて下記のコマンドを実行してください。
```
$ export OPENAI_API_KEY="[発行したAPI Key]"
```
`target_document` 直下に和訳したい論文のpdfを配置して下記のコマンドを実行してください。
```
$ python main.py --input_path [配置したpdfファイル名] --chapter_pattern [chapter番号の正規表現]
```
プログラムが完了すると `result/result.txt` に英語の文章と日本語の文章が交互に出力されています。

### 計算機（サーバ）での使用方法
計算機（サーバ）にsshして下記のコマンドを実行
```
$ uid=$(id -u `whoami`)
$ sudo docker build -t paper-translater --build-arg useruid=$uid .
$ sudo docker run -it paper-translater:latest /bin/bash
```
コンテナ入った後に下記のコマンドを実行して準備完了
TODO: 権限変更しないといけないのはイケてないのであとで修正予定
```
$ cd ../
$ sudo chown -R docker:docker paper-translater/
$ cd paper-translater/
```

## Example
`target_document/sample.pdf` に [NeurIPS 2020 Style Files](https://nips.cc/Conferences/2020/PaperInformation/StyleFiles) のページにあるpdfが配置してあります。
下記のコマンドを実行して出力されたファイルが `result/sample_result.txt` になっています。
```
$ python main.py --input_path target_document/sample.pdf --chapter_pattern  "^\d(\.\d)*\s?[A-z]+"
```

### 二段組論文の場合
`-b 0` というオプションを使用すれば二段組論文にも対応可能。
```
python main.py --input_path target_document/sample_two_column.pdf -b 0 --chapter_pattern  "^\d(\.\d)*\s?[A-z]+"
```

## 正規表現の例
正規表現については下記のサイトなどを使用して自分で利用したい論文のチャプター番号のフォーマットに合わせてください。
https://weblabo.oscasierra.net/tools/regex/

| チャプター番号のパターン | 正規表現 |
| --- | --- |
| 1 xxx <br> 1.1 xxx <br> 1.1.1 xxx | `^\d(\.\d)*\s?[A-z]+` |
| 1. xxx <br> 1.1. xxx <br> 1.1.1. xxx | `^\d\.(\d\.)*\s?[A-z]+` |

# 参考
- https://github.com/juu7g/Python-PDF2text/blob/main/README.md
