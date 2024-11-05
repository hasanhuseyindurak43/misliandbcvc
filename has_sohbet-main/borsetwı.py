from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import shutil
import os

global yon
yon = ''

global al
al = ''

global sat
yon = ''

class FirefoxAutomation:
    def __init__(self):
        self.profile_path = None
        self.driver = None

    def create_firefox_profile(self):
        # Create a temporary Firefox profile
        self.profile_path = os.path.join(os.getcwd(), "temp_firefox_profile")
        os.makedirs(self.profile_path, exist_ok=True)

        firefox_options = Options()
        firefox_options.add_argument(f"-profile")
        firefox_options.add_argument(self.profile_path)

        # Set up GeckoDriver service
        service = Service('/usr/local/bin/geckodriver')  # Ensure this path matches where you installed GeckoDriver

        # Initialize the Firefox browser with the specified options
        self.driver = webdriver.Firefox(service=service, options=firefox_options)

        # Maximize the window
        self.driver.maximize_window()

    def open_website_and_login(self):
        try:
            # Open the website
            self.driver.get('https://www.lbank.com/login')

            time.sleep(10)

            # Wait for the username field to be visible and send keys
            username_send_keys = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="__next"]/section/main/div[2]/div[1]/form/div[1]/div/input'))
            )
            username_send_keys.send_keys('barronsoftwares92@gmail.com')

            # Wait for the password field to be visible and send keys
            username_password_send_keys = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="__next"]/section/main/div[2]/div[1]/form/div[2]/div[1]/input'))
            )
            username_password_send_keys.send_keys('1968Hramoysulu2008')

            # Wait for the login button to be clickable and click it
            login_click = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/section/main/div[2]/div[1]/form/button'))
            )
            login_click.click()

            time.sleep(60)

            self.go_to_ded()

        except Exception as e:
            print(f"An error occurred: {e}")
            self.cleanup()
        finally:
            # Clean up: delete cookies, close driver, and remove profile
            self.cleanup()

    def go_to_ded(self):

        global yon

        global al

        global sat

        try:
            self.driver.get('https://www.lbank.com/tr/trade/ded_usdt')

            time.sleep(10)

            # Sayfayı adım adım 100 piksel aşağı kaydır
            current_position = 0  # Başlangıç pozisyonu
            while current_position < self.driver.execute_script("return document.body.scrollHeight"):
                self.driver.execute_script(f"window.scrollTo(0, {current_position});")
                current_position += 100  # Her seferinde 100 piksel artır
                time.sleep(0.1)  # Kaydırmalar arasında kısa bir bekleme süresi ekle

            ded_balance = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '/html/body/div/section/main/div[1]/div[1]/div[3]/div[3]/span[1]'))
            )
            ded_balances = ded_balance.text

            ded_balances = float(ded_balances)

            satis_tetikleme_fiyat_bir = ded_balances * 1.10
            satis_tetikleme_fiyat_iki = ded_balances * 0.90
            satisa_koyulacak_fiyat = ded_balances * 1.05

            alis_tetikleme_fiyat_bir = ded_balances * 0.89
            alis_tetikleme_fiyat_iki = ded_balances * 0.80
            alisa_koyulacak_fiyat = ded_balances * 0.85

            print("|" + "-" * 60 + "|")

            st1_string = f"| Satış tetiklenecek birinci şart : {satis_tetikleme_fiyat_bir:.7f} USDT"
            st1_length = len(st1_string)
            total_length = 61
            spaces = total_length - st1_length

            print(st1_string + " " * spaces + "|")

            st2_string = f"| Satış tetiklenecek ikinci şart : {satis_tetikleme_fiyat_iki:.7f} USDT"
            st2_length = len(st2_string)
            total_length = 61
            spaces = total_length - st2_length

            print(st2_string + " " * spaces + "|")

            sk_string = f"| Satışa koyulacak fiyat : {satisa_koyulacak_fiyat:.7f} USDT"
            sk_length = len(sk_string)
            total_length = 61
            spaces = total_length - sk_length

            print(sk_string + " " * spaces + "|")

            print("|" + "-" * 60 + "|")

            al1_string = f"| Alış tetiklenecek birinci şart : {alis_tetikleme_fiyat_bir:.7f} USDT"
            al1_length = len(al1_string)
            total_length = 61
            spaces = total_length - al1_length

            print(al1_string + " " * spaces + "|")

            al2_string = f"| Alış tetiklenecek ikinci şart : {alis_tetikleme_fiyat_iki:.7f} USDT"
            al2_length = len(al2_string)
            total_length = 61
            spaces = total_length - al2_length

            print(al2_string + " " * spaces + "|")

            ak_string = f"| Alışa koyulacak fiyat : {alisa_koyulacak_fiyat:.7f} USDT"
            ak_length = len(ak_string)
            total_length = 61
            spaces = total_length - ak_length

            print(ak_string + " " * spaces + "|")

            print("|" + "-" * 60 + "|")

            while True:
                # Ded coin değerini sürekli kontrol et
                ded_balance = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '/html/body/div/section/main/div[1]/div[1]/div[3]/div[3]/span[1]'))
                )
                ded_balances = ded_balance.text

                print("|" + "-" * 60 + "|")

                ded_string = f"| Ded Coin To Usdt : {ded_balances} USDT"
                ded_length = len(ded_string)
                total_length = 61
                spaces = total_length - ded_length

                print(ded_string + " " * spaces + "|")

                print("|" + "-" * 60 + "|")

                ded_balances = float(ded_balances)

                # Satış tetikleme fiyatlarını float olarak güncelleyin
                satis_tetikleme_fiyat_bir = float(satis_tetikleme_fiyat_bir)
                satis_tetikleme_fiyat_iki = float(satis_tetikleme_fiyat_iki)
                satisa_koyulacak_fiyat = float(satisa_koyulacak_fiyat)

                sats = self.driver.find_element(By.XPATH,
                                               '/html/body/div[1]/section/main/div[1]/div[2]/div[3]/div/div[2]/ul/li[2]/div/div[2]/span')

                # Elementi görünür yap (görünüm alanına kaydır)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", sats)


                sat = sats.text

                als = self.driver.find_element(By.XPATH,
                                                '/html/body/div[1]/section/main/div[1]/div[2]/div[3]/div/div[2]/ul/li[1]/div/div[2]/span')

                # Elementi görünür yap (görünüm alanına kaydır)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", als)

                al = als.text

                sat_string = f"| Sat : {float(sat):.8f} USDT"
                sat_length = len(sat_string)
                total_length = 61
                spaces = total_length - sat_length
                print(sat_string + " " * spaces + "|")

                al_string = f"| Al : {float(al):.8f} USDT"
                al_length = len(al_string)
                total_length = 61
                spaces = total_length - al_length
                print(al_string + " " * spaces + "|")

                if satis_tetikleme_fiyat_iki < ded_balances < satis_tetikleme_fiyat_bir and float(sat) > 0.10:

                    print("Satış Tetiklendi...")

                    time.sleep(1)

                    # İlk olarak, satis_giris elementini bulun
                    satis_giris = self.driver.find_element(By.XPATH,
                                                           '/html/body/div/section/main/div[1]/div[2]/div[3]/div/div[2]/div/div[2]/div[1]/div/input')

                    # Elementi görünür yap (görünüm alanına kaydır)
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", satis_giris)

                    # Kısa bir bekleme süresi ekleyin
                    satis_giris = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.XPATH,
                                                                                    '/html/body/div/section/main/div[1]/div[2]/div[3]/div/div[2]/div/div[2]/div[1]/div/input')))
                    # Mevcut değeri temizlemek için BACKSPACE tuşlarını kullanın
                    satis_giris.send_keys(Keys.CONTROL + "a")
                    satis_giris.send_keys(Keys.BACKSPACE)

                    # Yeni değeri girin
                    satis_giris.send_keys(f"{satisa_koyulacak_fiyat:.7f}")

                    time.sleep(3)

                    # Slider öğesini bul
                    slider_rail = self.driver.find_element(By.XPATH, '/html/body/div/section/main/div[1]/div[2]/div[3]/div/div[2]/div/div[2]/div[3]/div/div/div')

                    slider = slider_rail.find_element(By.XPATH, '/html/body/div/section/main/div[1]/div[2]/div[3]/div/div[2]/div/div[2]/div[3]/div/div/div/div[4]')

                    # Slider öğesini görünür hale getirmek için sayfayı kaydır
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", slider)

                    # Slider'ın genişliğini ve konumunu alın
                    slider_width = slider.size['width']

                    # Slider'ın başlangıç pozisyonunu alın
                    slider_location = slider.location['x']

                    # Tarayıcı genişliğini al
                    window_width = self.driver.execute_script("return window.innerWidth")

                    # Slider'ı tam olarak sonuna kadar sürüklemek için gereken offset miktarını hesapla
                    offset = window_width - slider_location - slider_width

                    # Slider'ı sağa doğru sürükle
                    actions = ActionChains(self.driver)
                    actions.click_and_hold(slider).move_by_offset(offset, 0).release().perform()

                    time.sleep(5)

                    sat_islem = self.driver.find_element(By.XPATH, '/html/body/div/section/main/div[1]/div[2]/div[3]/div/div[2]/div/div[2]/button')
                    sat_islem.click()

                    onayla = self.driver.find_element(By.XPATH, '/html/body/div/section/main/div[1]/div[2]/div[3]/div/div[3]/div/div/div[2]/div/div[2]/div[3]/button[2]')
                    onayla.click()

                    # Satış tetikleme fiyatlarını ve satışa koyulacak fiyatı güncelleyin
                    satis_tetikleme_fiyat_bir *= 1.10
                    satis_tetikleme_fiyat_iki *= 0.90
                    satisa_koyulacak_fiyat *= 1.05

                    print(f"Satış tetiklenecek birinci şart : {satis_tetikleme_fiyat_bir:.7f}")
                    print(f"Satış tetiklenecek ikinci şart : {satis_tetikleme_fiyat_iki:.7f}")
                    print(f"Satışa koyulacak fiyat : {satisa_koyulacak_fiyat:.7f} ")

                    time.sleep(15)

                if alis_tetikleme_fiyat_iki < ded_balances < alis_tetikleme_fiyat_bir and float(al) > 0.10:
                    print("Alış Tetiklendi...")

                    time.sleep(1)

                    # İlk olarak, satis_giris elementini bulun
                    alis_giris = self.driver.find_element(By.XPATH,
                                                           '/html/body/div/section/main/div[1]/div[2]/div[3]/div/div[2]/div/div[1]/div[1]/div/input')

                    # Elementi görünür yap (görünüm alanına kaydır)
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", alis_giris)

                    # Kısa bir bekleme süresi ekleyin
                    alis_giris = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.XPATH,
                                                                                                  '/html/body/div/section/main/div[1]/div[2]/div[3]/div/div[2]/div/div[1]/div[1]/div/input')))
                    # Mevcut değeri temizlemek için BACKSPACE tuşlarını kullanın
                    alis_giris.send_keys(Keys.CONTROL + "a")
                    alis_giris.send_keys(Keys.BACKSPACE)

                    # Yeni değeri girin
                    alis_giris.send_keys(f"{satisa_koyulacak_fiyat:.7f}")

                    time.sleep(3)

                    # Slider öğesini bul
                    slider_rail = self.driver.find_element(By.XPATH,
                                                           '/html/body/div/section/main/div[1]/div[2]/div[3]/div/div[2]/div/div[1]/div[3]/div/div[1]/div')

                    slider = slider_rail.find_element(By.XPATH,
                                                      '/html/body/div/section/main/div[1]/div[2]/div[3]/div/div[2]/div/div[1]/div[3]/div/div[1]/div/div[4]')

                    # Slider öğesini görünür hale getirmek için sayfayı kaydır
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", slider)

                    # Slider'ın genişliğini ve konumunu alın
                    slider_width = slider.size['width']

                    # Slider'ın başlangıç pozisyonunu alın
                    slider_location = slider.location['x']

                    # Tarayıcı genişliğini al
                    window_width = self.driver.execute_script("return window.innerWidth")

                    # Slider'ı tam olarak sonuna kadar sürüklemek için gereken offset miktarını hesapla
                    offset = window_width - slider_location - slider_width

                    # Slider'ı sağa doğru sürükle
                    actions = ActionChains(self.driver)
                    actions.click_and_hold(slider).move_by_offset(offset, 0).release().perform()

                    time.sleep(5)

                    al_islem = self.driver.find_element(By.XPATH,
                                                         '/html/body/div[1]/section/main/div[1]/div[2]/div[3]/div/div[2]/div/div[1]/button')
                    al_islem.click()

                    onayla = self.driver.find_element(By.XPATH,
                                                      '/html/body/div/section/main/div[1]/div[2]/div[3]/div/div[3]/div/div/div[2]/div/div[2]/div[3]/button[2]')
                    onayla.click()

                    # Satış tetikleme fiyatlarını ve satışa koyulacak fiyatı güncelleyin
                    alis_tetikleme_fiyat_bir *= 0.89
                    alis_tetikleme_fiyat_iki *= 0.80
                    alisa_koyulacak_fiyat *= 0.85

                    print(f"Satış tetiklenecek birinci şart : {alis_tetikleme_fiyat_bir:.7f}")
                    print(f"Satış tetiklenecek ikinci şart : {alis_tetikleme_fiyat_iki:.7f}")
                    print(f"Satışa koyulacak fiyat : {alisa_koyulacak_fiyat:.7f} ")

                    time.sleep(15)

        except Exception as e:
            print(f"An error occurred: {e}")
            self.cleanup()
        finally:
            # Clean up: delete cookies, close driver, and remove profile
            self.cleanup()

    def cleanup(self):
        if self.driver:
            self.driver.delete_all_cookies()  # Clear cookies
            self.driver.quit()  # Close the browser

        # Remove the temporary Firefox profile
        if self.profile_path and os.path.exists(self.profile_path):
            shutil.rmtree(self.profile_path)


if __name__ == "__main__":
    while True:
        automation = FirefoxAutomation()
        automation.create_firefox_profile()
        automation.open_website_and_login()
