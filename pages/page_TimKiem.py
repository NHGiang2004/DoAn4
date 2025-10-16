# pages/page_TimKiem.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PageTimKiem:
    def __init__(self, driver):
        self.driver = driver
        # ô tìm kiếm (theo placeholder)
        self.search_box = (By.CSS_SELECTOR, "input[placeholder='Tìm kiếm bài học, bài tập, mã lớp, mã khóa học...']")
        # vùng chứa kết quả tổng (theo ảnh bạn gửi)
        self.result_area = (By.CSS_SELECTOR, "div.d-flex.flex-row.row")
        # fallback: item con trong vùng kết quả
        self.result_item = (By.CSS_SELECTOR, "div.d-flex.flex-row.row > div")
        # những chuỗi có thể biểu thị "không có kết quả" (so sánh lower-case trên body)
        self.no_result_texts = ["không tìm thấy", "không có kết quả", "không tìm thấy kết quả"]

    def nhap_tu_khoa(self, keyword):
        # chờ ô tìm kiếm có thể click và nhập
        search = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.search_box))
        search.clear()
        search.send_keys(keyword)
        search.send_keys(Keys.ENTER)
        # nhiều site chuyển trang khi tìm kiếm => đợi url chứa ?q= (nếu có)
        try:
            WebDriverWait(self.driver, 7).until(lambda d: "?q=" in d.current_url)
        except:
            # nếu không đổi URL thì vẫn tiếp tục (một số trường hợp là AJAX)
            pass

    def lay_ket_qua(self, timeout=15):
        wait = WebDriverWait(self.driver, timeout)

        def predicate(driver):
            # 1) kiểm tra body có chứa chuỗi "không tìm thấy" (bỏ qua hoa thường)
            try:
                body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
            except:
                body_text = ""
            for no_text in self.no_result_texts:
                if no_text in body_text:
                    return body_text  # trả về toàn bộ body để debug / hoặc trả về dòng liên quan

            # 2) kiểm tra vùng kết quả (result_area) có tồn tại và có text không rỗng
            elems = driver.find_elements(*self.result_area)
            if elems:
                txt = elems[0].text.strip()
                if txt:
                    return txt

            # 3) thử lấy các item con nếu có
            items = driver.find_elements(*self.result_item)
            if items:
                combined = "\n".join([it.text for it in items if it.text.strip()])
                if combined:
                    return combined

            # chưa thấy gì -> tiếp tục chờ
            return False

        try:
            result = wait.until(predicate)
            return result
        except Exception:
            # nếu hết timeout vẫn không tìm được gì, trả về toàn bộ body để debug (không raise nữa)
            try:
                return self.driver.find_element(By.TAG_NAME, "body").text
            except:
                return ""
