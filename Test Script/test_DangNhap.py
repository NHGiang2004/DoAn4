# Test Script/test_DangNhap.py
import pytest
from selenium import webdriver
from pages.page_DangNhap import PageDangNhap
from utils.data_utils import load_csv_data
from datetime import datetime
from utils.excel_write_dangNhap import write_test_dangNhap

csv_file = "Data/OLM_DangNhap.csv"
excel_file = r"D:\Documents\Excel Files\TestDangNhapOLM.xlsx"
RUN_ID = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@pytest.mark.parametrize("username,password,expected", [
    (row["username"], row["password"], row["expected"]) for row in load_csv_data(csv_file)
])
def test_dangnhap(username, password, expected):
    driver = webdriver.Chrome()
    try:
        driver.maximize_window()
        driver.get("https://olm.vn/")

        page = PageDangNhap(driver)
        page.open_login_page()
        page.login(username, password)
        actual = page.get_message()

        passed = expected.lower() in actual.lower()
        status = "PASS" if passed else "FAIL"

        write_test_dangNhap(excel_file, RUN_ID, username, password, expected, actual, status)

        assert passed, f"Expected '{expected}', but got '{actual}'"

    finally:
        driver.quit()
