import pytest
from selenium import webdriver
from pages.page_QuenMK import PageQuenMK
from utils.data_utils import load_excel_data
from utils.excel_write_quenMK import write_test_quenMK
from datetime import datetime

excel_file = "Data/OLM_QuenMK.xlsx"
output_file = r"D:\Documents\Excel Files\TestQuenMK_OLM.xlsx"
RUN_ID = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@pytest.mark.parametrize(
    "mail,expected",
    [(row["Mail"], row["Expected"]) for row in load_excel_data(excel_file)]
)
def test_quen_mat_khau(mail, expected):
    driver = webdriver.Chrome()
    try:
        driver.maximize_window()
        page = PageQuenMK(driver)
        page.open_quen_mk_page()

        # Nếu mail trống hoặc None, xử lý trước để tránh lỗi send_keys
        actual = page.nhap_email(mail if mail else "")

        passed = expected.lower() in actual.lower()
        status = "PASS" if passed else "FAIL"

        write_test_quenMK(output_file, RUN_ID, mail, expected, actual, status)
        assert passed, f"Expected '{expected}', but got '{actual}'"

    finally:
        driver.quit()
