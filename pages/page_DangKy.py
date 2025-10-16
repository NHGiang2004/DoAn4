from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PageDangKy:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://olm.vn/"

        self.register_link = (By.CSS_SELECTOR, "a[title='Đăng ký tài khoản OLM']")
        self.hoten_input = (By.NAME, "name")
        self.tendn_input = (By.NAME, "username")
        self.sdt_input = (By.XPATH, "//input[@placeholder='Số điện thoại']")
        self.email_input = (By.NAME, "email")
        self.password_input = (By.NAME, "password")

        # sửa lại selector nút submit
        self.submit_button = (By.XPATH, "//button[contains(text(),'Đăng ký')]")

        self.popup_skip = (By.XPATH, "//button[contains(text(),'Để sau')]")

    def open_register_page(self):
        self.driver.find_element(*self.register_link).click()
        # xử lý popup nếu có
        try:
            WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(self.popup_skip)
            ).click()
        except:
            pass

    def register(self, hoten, tendn, sdt, email, matkhau):
        # điền form
        if hoten:
            self.driver.find_element(*self.hoten_input).send_keys(hoten)
        if tendn:
            self.driver.find_element(*self.tendn_input).send_keys(tendn)
        if sdt:
            self.driver.find_element(*self.sdt_input).send_keys(sdt)
        if email:
            self.driver.find_element(*self.email_input).send_keys(email)
        if matkhau:
            self.driver.find_element(*self.password_input).send_keys(matkhau)

        # chờ nút xuất hiện rồi click
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.submit_button)
        ).click()

    def get_messages(self, timeout=5):
        """
        Gom tất cả thông báo lỗi/thành công (nếu có) từ DOM.
        """
        driver = self.driver
        messages = []

        alert_selectors = [
            "div.response-register.alert-danger",
            "div.alert-danger",
            "span.text-danger",
            ".invalid-feedback",
            ".box-error-tel"
        ]

        # duyệt tất cả selector lỗi
        for sel in alert_selectors:
            try:
                elems = WebDriverWait(driver, timeout).until(
                    lambda d: d.find_elements(By.CSS_SELECTOR, sel)
                )
                for e in elems:
                    txt = e.text.strip()
                    if txt and txt not in messages:
                        messages.append(txt)
            except:
                continue

        # nếu không có gì, fallback lấy body text
        if not messages:
            try:
                body_text = driver.find_element(By.TAG_NAME, "body").text
                if body_text:
                    messages.append(body_text.strip())
            except:
                pass

        return " || ".join(messages)

