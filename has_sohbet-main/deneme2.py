from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import shutil
import os

class Login:
    def __init__(self, driver_path, profile_dir):
        self.driver_path = driver_path
        self.profile_dir = profile_dir
        self.driver = None

    def setup_driver(self):
        # Profil için geçici bir klasör oluşturun
        if not os.path.exists(self.profile_dir):
            os.makedirs(self.profile_dir)

        # Chrome seçeneklerini ayarlayın
        chrome_options = Options()
        chrome_options.add_argument(f"user-data-dir={self.profile_dir}")

        # ChromeDriver servisini ayarlayın
        service = Service(executable_path=self.driver_path)

        # WebDriver'ı başlatın
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        # Tarayıcı penceresinin boyutunu ayarlayın
        self.driver.set_window_size(1000, 900)

    def login(self, url, username, password):
        if self.driver is None:
            raise RuntimeError("Driver not initialized. Call setup_driver() before login.")

        # URL'yi açın
        self.driver.get(url)
        
        time.sleep(10)
        
        # Giriş butonuna tıklayın
        giris_click = self.driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/header/div[1]/div[3]/button[1]')
        giris_click.click()
        
        # Bekleme süresi (giriş penceresinin açılması için)
        time.sleep(5)
        
        # Kullanıcı adı ve şifre alanlarını doldurun
        username_field = self.driver.find_element(By.XPATH, '//*[@id="root"]/div[6]/div/div/div/div/div/div[2]/form/div[1]/div[3]/div/label/input')
        username_field.send_keys(username)
        
        time.sleep(1)
        
        password_field = self.driver.find_element(By.XPATH, '//*[@id="root"]/div[6]/div/div/div/div/div/div[2]/form/div[1]/div[4]/div/label/input')
        password_field.send_keys(password)
        
        # Giriş butonuna tıklayın
        login_button = self.driver.find_element(By.XPATH, '//*[@id="root"]/div[6]/div/div/div/div/div/div[2]/form/div[1]/div[6]/div/button')
        login_button.click()
        
        # Sayfanın yüklenmesini bekleyin (giriş sonrası)
        time.sleep(1000)

    def cleanup(self):
        if self.driver:
            # Çerezleri temizleyin
            self.driver.delete_all_cookies()

            # Tarayıcıyı kapatın
            self.driver.quit()

            # Profil klasörünü kaldırın
            shutil.rmtree(self.profile_dir)

# Kullanım örneği
if __name__ == "__main__":
    profile_dir = '/tmp/chrome_profile'
    driver_path = '/usr/bin/chromedriver'

    login = Login(driver_path, profile_dir)
    login.setup_driver()
    login.login("https://www.galabet882.com/tr/games?openGames=300000091-fun&gameNames=Mines", "barron4335", "1968Hram")
    login.cleanup()
