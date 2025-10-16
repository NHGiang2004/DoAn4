from selenium.webdriver.common.by import By
import time

class PageQuenMK:
    def __init__(self, driver):
        self.driver = driver
        self.link_quen_mk = (By.XPATH, "(//a[contains(text(),'Quên mật khẩu')])[1]")
        self.input_email = (By.CSS_SELECTOR, "input[name='data'][type='email']")
        self.button_submit = (By.CSS_SELECTOR, "button.btn.olm-btn-primary")
        self.message = (By.XPATH, "(//div[@class='alert alert-danger mb-2'])[1]")
        self.toast_message = (By.XPATH, "//*[contains(text(),'Hãy điền đầy đủ thông tin chưa dấu')]")

    def open_quen_mk_page(self):
        self.driver.get("https://olm.vn/")
        self.driver.find_element(By.CSS_SELECTOR, "a[title='Đăng nhập OLM']").click()
        time.sleep(1)
        self.driver.find_element(*self.link_quen_mk).click()
        time.sleep(2)

    def nhap_email(self, email):
        email_field = self.driver.find_element(*self.input_email)
        email_field.clear()
        if email:
            email_field.send_keys(email)

        self.driver.find_element(*self.button_submit).click()
        time.sleep(1)

        # Kiểm tra lỗi HTML5 validation
        validation_msg = email_field.get_attribute("validationMessage")
        if validation_msg:
            return validation_msg

        # Nếu không có validation message thì kiểm tra các thông báo khác
        try:
            msg = self.driver.find_element(*self.message).text
        except:
            try:
                msg = self.driver.find_element(*self.toast_message).text
            except:
                msg = ""

        return msg
