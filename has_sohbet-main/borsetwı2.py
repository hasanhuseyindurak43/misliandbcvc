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

global coin_list
coin_list = []

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

    def go_to_list(self):
        
        global coin_list

        try:
            self.driver.get('https://www.lbank.com/tr/trade/ded_usdt')

            time.sleep(10)

            # components_tableMain__tTqwC sınıfına sahip div'i bulun
            div_element = self.driver.find_element(By.CLASS_NAME, 'components_tableMain__tTqwC')

            # div içindeki notranslate false tableListItem sınıfına sahip tüm li elemanlarını bulun
            li_elements = div_element.find_elements(By.CSS_SELECTOR, 'li.notranslate.false.tableListItem')

            # Her bir li elemanının içindeki istenen css selector'e sahip elementin text'ini al
            for li in li_elements:
                try:
                    # İstenen css selector'e sahip elementin text'ini alın
                    c1 = li.find_element(By.CSS_SELECTOR, 'div.components_symbol__xlZ3i > i:nth-child(1)').text
                    c2 = li.find_element(By.CSS_SELECTOR, 'div.components_symbol__xlZ3i > i:nth-child(3)').text
                    price_change = li.find_element(By.CSS_SELECTOR, 'div.components_priceChange__9B1hP > div:nth-child(1)').text

                    # Metinleri bir liste olarak coin_list'e ekle
                    coin_list.append([c1, c2, price_change])

                except Exception as e:
                    # Eleman bulunamazsa veya başka bir hata oluşursa hata mesajını yazdırın
                    print(f"Hata: {e}")

            # coin_list'in içeriğini numaralandırarak yazdırın
            print("Coin Listesi:")
            for index, coin in enumerate(coin_list):
                print(f"{index}: {coin}")
            
            # Kullanıcıdan bir giriş alın (örn. "LUNA")
            user_input = input("Aramak istediğiniz coin'i girin (örn. 'LUNA'): ").strip()

            # Kullanıcıdan arama yapmaya devam etmek isteyip istemediğini sor
            while True:
                # Kullanıcıdan bir giriş alın (örn. "LUNA")
                user_input = input("Aramak istediğiniz coin'i girin (örn. 'LUNA'): ").strip()

                # Kullanıcı girdisine göre filtreleme yapın
                filtered_coins = [coin for coin in coin_list if user_input.upper() in coin[0].upper()]

                # Filtrelenmiş sonuçları yazdırın
                if filtered_coins:
                    print("Filtrelenmiş Coin Listesi:")
                    for index, coin in enumerate(filtered_coins):
                        print(f"{index}: {coin}")
                else:
                    print(f"'{user_input}' ile eşleşen coin bulunamadı.")

                # Kullanıcıya tekrar arama yapmak isteyip istemediğini sor
                continue_search = input("Tekrar arama yapmak ister misiniz? (E/H): ").strip().lower()
                if continue_search != 'e':
                    print("Çıkılıyor...")
                    break
                    self.cleanup()


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
    automation = FirefoxAutomation()
    automation.create_firefox_profile()
    automation.go_to_list()
