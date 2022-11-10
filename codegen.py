import nbformat as nbf
import os
from pathlib import Path


class CodeGenerator():
    def __init__(self,download_path,scraper_name,code_template):
        self.download_path=download_path
        self.scraper_name=scraper_name
        self.code_template=code_template

    def make_notebook(self):
        nb = nbf.v4.new_notebook()
        nb['cells'] = [nbf.v4.new_code_cell(self.code_template)]
        download_path=r"{}".format(self.download_path) +"\\"+self.scraper_name
        nbf.write(nb, f'{download_path)}-Scraper.ipynb')
