import pytest
from selenium import webdriver
from pages.page_HoiBai import PageHoiBai
from utils.data_utils import load_excel_data
from utils.excel_write_hoiBai import write_test_hoiBai
from datetime import datetime

# Đường dẫn file
excel_file = "Data/OLM_HoiBai.xlsx"
output_file = r"D:\Documents\Excel Files\TestHoiBai_OLM.xlsx"

# Mã chạy (RUN_ID)
RUN_ID = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@pytest.mark.parametrize(
    "khoi, mon, cauhoi, expected",
    [(row["Khoi"], row["Mon"], row["CauHoi"], row["Expected"]) for row in load_excel_data(excel_file)]
)
def test_hoi_bai(khoi, mon, cauhoi, expected):
    driver = webdriver.Chrome()
    try:
        driver.maximize_window()
        page = PageHoiBai(driver)
        page.open_hoibai_page()

        actual = page.gui_cau_hoi(khoi, mon, cauhoi)
        passed = expected.lower() in actual.lower()
        status = "PASS" if passed else "FAIL"

        # Ghi kết quả ra Excel
        write_test_hoiBai(output_file, RUN_ID, khoi, mon, cauhoi, expected, actual, status)

        # Kiểm tra kết quả
        assert passed, f"Expected '{expected}', but got '{actual}'"

    finally:
        driver.quit()
