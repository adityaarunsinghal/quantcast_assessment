import io
import sys
import unittest
from most_active_cookie import most_active_cookie

class test_most_active_cookie(unittest.TestCase):

    def test_multi_line_output(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput  
        test = most_active_cookie()
        test.read_file("test_cookie_log_1.csv")
        test.printMostActive("2018-12-08")
        sys.stdout = sys.__stdout__ 
        expected = """SAZuXPGUrfbcn5UA\n4sMM2LxV07bPJzwf\nfbcn5UAVanZf6UtG\n"""
        self.assertEqual(expected, capturedOutput.getvalue(), "Multi Value Output Test Failed")

    def test_single_line_output(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput  
        test = most_active_cookie()
        test.read_file("test_cookie_log_1.csv")
        test.printMostActive("2018-12-09")
        sys.stdout = sys.__stdout__ 
        expected = """AtY0laUfhglK3lC7\n"""
        self.assertEqual(expected, capturedOutput.getvalue(), "Single Value Output Test Failed")

    def test_date_nonexistent(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput  
        test = most_active_cookie()
        test.read_file("test_cookie_log_1.csv")
        test.printMostActive("2018-11-09")
        sys.stdout = sys.__stdout__ 
        expected = """No Values for Requested Date\n"""
        self.assertEqual(expected, capturedOutput.getvalue(), "Non-existent Date Request Test Failed")
    
    def test_null_filepath(self):
        test = most_active_cookie()
        self.assertRaises(FileNotFoundError, test.read_file, "")

    def test_invalid_date_format(self):
        test = most_active_cookie()
        test.read_file("test_cookie_log_1.csv")
        self.assertRaises(ValueError, test.printMostActive, "")
    
    def test_wrong_header(self):
        test = most_active_cookie()
        self.assertRaises(AssertionError, test.read_file, "test_cookie_log_2.csv")
    
    def test_bad_rows(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput  
        test = most_active_cookie()
        with self.assertLogs() as logs:
            test.read_file("test_cookie_log_3.csv")
        self.assertEqual(len(logs.records), 4)
        test.printMostActive("2017-01-07")
        sys.stdout = sys.__stdout__ 
        expected = """4sMM2LxV07bPJzwf\n"""
        self.assertEqual(expected, capturedOutput.getvalue(), "Bag rows Test Failed")

if __name__ == '__main__':
    unittest.main()
    