import pytest
from selenium import webdriver
from pages.page_TimKiem import PageTimKiem
from utils.excel_write_timKiem import write_test_result
from utils.data_utils import load_csv_data
from datetime import datetime

csv_file = "Data/OLM_TimKiem.csv"   # file input test data
excel_file = "D:\Documents\Excel Files\TestTimKiemOLM.xlsx" # file output báo cáo
RUN_ID = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@pytest.mark.parametrize(
    "keyword,expected",
    [(row["keys"], row["expected"]) for row in load_csv_data(csv_file)]
)

def test_tim_kiem(keyword, expected):
    driver = webdriver.Chrome()
    try:
        driver.maximize_window()
        driver.get("https://olm.vn/")

        page = PageTimKiem(driver)
        page.nhap_tu_khoa(keyword)
        result_text = page.lay_ket_qua()

        results = result_text.splitlines()
        passed = any(expected.lower() in r.lower() for r in results)
        status = "PASS" if passed else "FAIL"

        write_test_result(excel_file, RUN_ID, keyword, expected, result_text, status)

        assert passed, f"Expected '{expected}' not found in results: {results}"
    finally:
        driver.quit()
