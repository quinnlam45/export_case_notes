import unittest
import io
from tempfile import NamedTemporaryFile
from openpyxl import Workbook
from report_builder import *

class ReportBuilderTest(unittest.TestCase):

    test_file_bytes = io.BytesIO()

    with NamedTemporaryFile(suffix='.xlsx') as tmp:

        #create temp test workbook
        wb = Workbook()
        ws = wb.active
        ws["A1"] = "Test"

        tmp.seek(0)
        stream = tmp.read()
        test_file_bytes.write(stream)
    
    def test_read_file_obj_to_bytes(self):
        pass
