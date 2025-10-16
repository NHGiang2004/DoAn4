from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class PageHoiBai:
    def __init__(self, driver):
        self.driver = driver
        self.card_click = (By.CSS_SELECTOR, "p.card-text.text-grey-600")
        self.select_khoi = (By.XPATH, "//select[@aria-label='Chọn khối lớp']")
        self.select_mon = (By.XPATH, "//select[@aria-label='Chọn môn']")
        self.input_cauhoi = (By.XPATH, "//div[@role='textbox']")
        self.button_gui = (By.XPATH, "//button[contains(text(), 'Tạo câu hỏi')]")
        self.message_alert = (By.CSS_SELECTOR, "div.alert.alert-danger, div.alert.alert-success")
        self.toast_message = (By.XPATH, "//div[contains(@class,'toast-body')]")

    def open_hoibai_page(self):
        self.driver.get("https://olm.vn/hoi-dap")
        self.driver.maximize_window()
        time.sleep(2)

    def gui_cau_hoi(self, khoi, mon, cauhoi):
        # Click để mở form hỏi bài
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.card_click)
        ).click()

        # Chờ textarea xuất hiện
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.input_cauhoi)
        )

        # Chọn khối
        if khoi and khoi != "Tất cả":
            self.driver.find_element(*self.select_khoi).send_keys(khoi)

        # Chọn môn
        if mon and mon != "Tất cả":
            self.driver.find_element(*self.select_mon).send_keys(mon)

        # Nhập câu hỏi
        cauhoi_field = self.driver.find_element(*self.input_cauhoi)
        cauhoi_field.clear()
        if cauhoi:
            cauhoi_field.send_keys(cauhoi)

        # Nhấn Gửi
        self.driver.find_element(*self.button_gui).click()

        # Chờ thông báo hiện
        time.sleep(2)
        msg = ""
        try:
            msg = self.driver.find_element(*self.message_alert).text
        except:
            try:
                msg = self.driver.find_element(*self.toast_message).text
            except:
                pass

        return msg.strip()
