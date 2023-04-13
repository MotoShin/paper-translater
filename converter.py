from dataclasses import dataclass
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from io import StringIO


@dataclass
class Converter():
    target_pdf_file: str = "sample.pdf"
    
    def __post_init__(self) -> None:
        # 標準組込み関数open()でモード指定をbinaryでFileオブジェクトを取得
        self.fp = open("target_document/" + self.target_pdf_file, 'rb')
        # 出力先をPythonコンソールするためにIOストリームを取得
        self.outfp = StringIO()

        # 各種テキスト抽出に必要なPdfminer.sixのオブジェクトを取得する処理
        rmgr = PDFResourceManager() # PDFResourceManagerオブジェクトの取得
        lprms = LAParams() # LAParamsオブジェクトの取得
        self.device = TextConverter(rmgr, self.outfp, laparams=lprms) # TextConverterオブジェクトの取得
        self.iprtr = PDFPageInterpreter(rmgr, self.device) # PDFPageInterpreterオブジェクトの取得

    def convert(self) -> str:
        # PDFファイルから1ページずつ解析(テキスト抽出)処理する
        for page in PDFPage.get_pages(self.fp):
            self.iprtr.process_page(page)
        
        text = self.outfp.getvalue()  # Pythonコンソールへの出力内容を取得
        return text

    def close(self) -> None:
        self.outfp.close()  # I/Oストリームを閉じる
        self.device.close() # TextConverterオブジェクトの解放
        self.fp.close()     #  Fileストリームを閉じる
