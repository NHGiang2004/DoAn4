# pages/page_DangNhap.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PageDangNhap:
    def __init__(self, driver):
        self.driver = driver
        # nút đăng nhập trên trang chủ
        self.btn_login_home = (By.CSS_SELECTOR, "a[title='Đăng nhập OLM']")
        # ô nhập username/email
        self.input_username = (By.XPATH, "//input[@name='username' and @placeholder='Tên đăng nhập hoặc email']")
        # ô nhập password
        self.input_password = (By.XPATH, "//input[@name='password' and @placeholder='Mật khẩu']")
        # nút submit
        self.btn_login = (By.XPATH, "(//button[contains(text(),'Đăng nhập')])[1]")
        # vùng thông báo lỗi/thành công
        self.alert_area = (By.CSS_SELECTOR, "div[class='alert alert-danger mb-2']")

    def open_login_page(self):
        # mở trang đăng nhập từ trang chủ
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.btn_login_home)
        ).click()

    def login(self, username, password):
        # nhập username
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.input_username)
        ).clear()
        self.driver.find_element(*self.input_username).send_keys(username or "")

        # nhập password
        self.driver.find_element(*self.input_password).clear()
        self.driver.find_element(*self.input_password).send_keys(password or "")

        # click login
        self.driver.find_element(*self.btn_login).click()

    def get_message(self, timeout=10):
        try:
            msg = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.alert_area)
            )
            return msg.text.strip()
        except:
            return self.driver.find_element(By.TAG_NAME, "body").text
