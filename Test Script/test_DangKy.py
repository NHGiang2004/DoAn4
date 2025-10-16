import pytest
from selenium import webdriver
from pages.page_DangKy import PageDangKy
from utils.data_utils import load_csv_data
from datetime import datetime
from utils.excel_write_dangKy import write_test_dangKy

csv_file = "Data/OLM_DangKy.csv"
excel_file = r"D:\Documents\Excel Files\TestDangKyOLM.xlsx"
RUN_ID = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@pytest.mark.parametrize(
    "hoten,tendn,sdt,email,matkhau,expected",
    [
        (row["HovaTen"], row["TenDN"], row["SDT"], row["Email"], row["MatKhau"], row["Expected"])
        for row in load_csv_data(csv_file)
    ]
)
def test_dangky(hoten, tendn, sdt, email, matkhau, expected):
    driver = webdriver.Chrome()
    try:
        driver.maximize_window()
        driver.get("https://olm.vn/")

        page = PageDangKy(driver)
        page.open_register_page()
        page.register(hoten, tendn, sdt, email, matkhau)

        actual = page.get_messages()
        passed = expected.lower() in actual.lower()
        status = "PASS" if passed else "FAIL"

        write_test_dangKy(excel_file, RUN_ID, hoten, tendn, sdt, email, matkhau, expected, actual, status)

        assert passed, f"Expected '{expected}', but got '{actual}'"

    finally:
        driver.quit()
