import nbformat as nbf
import os
import tempfile
from pathlib import Path


class CodeGenerator():
    def __init__(self,download_path,scraper_name,code_template):
        self.download_path=download_path
        self.scraper_name=scraper_name
        self.code_template=code_template

    def make_notebook(self):
        nb = nbf.v4.new_notebook()
        nb['cells'] = [nbf.v4.new_code_cell(self.code_template)]
        tmp = tempfile.NamedTemporaryFile
        fn=f"{self.scraper_name}.ipynb"
        with open(tmp.fn, 'w') as f:
            nbf.write(nb, f)# where `stuff` is, y'know... stuff to write (a string)
            tmp_directory = os.path.dirname(f)
        return tmp_directory
