from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

class go_to_tranfertion():
    def go_on_mobile(self, iban="24 0012 5020 0783 2682 5003 55", tc=None, parola=None, yatirilanlimit=None):
        try:
            # Selenium Hub'ı başlatmak için kullanılacak komut
            hub_command = "java -jar selenium-server-standalone.jar -role hub"

            # Selenium Hub'ı başlat
            import subprocess
            hub_process = subprocess.Popen(hub_command, shell=True)

            # Selenium Node'ları başlatmak için kullanılacak komut
            node_command = "java -jar selenium-server-standalone.jar -role node -hub http://localhost:4444/grid/register -browser browserName=chrome"

            # Selenium Node'ları başlat (örnek olarak bir Chrome tarayıcı eklenmiştir)
            node_process = subprocess.Popen(node_command, shell=True)

            chrome_options = Options()

            # webdriver.Remote kullanarak tarayıcıyı başlatın
            driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub", options=chrome_options)

            # driver = webdriver.Firefox()

            def scroll_down(driver, pixels):
                # JavaScript'i kullanarak sayfayı belirli bir miktarda aşağıya kaydırma
                driver.execute_script("window.scrollBy(0, arguments[0]);", pixels)

            driver.maximize_window()
            driver.get("https://sube.garantibbva.com.tr/isube/login/login/passwordentrypersonalforgetme")

            wait = WebDriverWait(driver, 10)

            tcgiris = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="custno"]')))
            tcgiris.send_keys(tc)
            time.sleep(0.7)

            parolagiris = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
            parolagiris.send_keys(parola)

            time.sleep(0.7)
            girisyap = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="formSubmit"]')))
            girisyap.click()

            time.sleep(1)
            paratransfer = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="primary3"]')))
            paratransfer.click()

            time.sleep(0.7)
            ibantransfer = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="primaryLi3"]/ul/li[3]/a')))
            ibantransfer.click()

            time.sleep(1)
            hesapseç = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="fakeSelectselector1"]')))
            hesapseç.click()

            # İlgili elementleri bul
            customDropDown = driver.find_element(By.CLASS_NAME, 'customDropDown')
            accountSelection = customDropDown.find_element(By.ID, 'accountSelection')
            selectorContId = accountSelection.find_element(By.ID, 'selectorContId')
            formFieldOuter = selectorContId.find_element(By.CLASS_NAME, 'formFieldOuter')
            selectorFormFieldSurroundId = formFieldOuter.find_element(By.ID, 'selectorFormFieldSurroundId')
            gtCustomContainer = selectorFormFieldSurroundId.find_element(By.CLASS_NAME, 'gtCustomContainer')
            gTautoSuggestions = gtCustomContainer.find_element(By.CLASS_NAME, 'gTautoSuggestions')
            ul = gTautoSuggestions.find_element(By.TAG_NAME, 'ul')
            li = ul.find_element(By.CSS_SELECTOR, 'li.group.odd')
            ul = li.find_element(By.TAG_NAME, 'ul')
            oddLiElements = ul.find_elements(By.TAG_NAME, 'li')

            # Li elementlerini dolaş
            for liElement in oddLiElements:
                # D1 classına sahip spanı bul
                d1Span = liElement.find_element(By.CLASS_NAME, 'd1')
                # C2 classına sahip spanı bul
                c2Span = d1Span.find_element(By.CLASS_NAME, 'c2')
                # Sp3 classına sahip spanı bul
                sp3Span = c2Span.find_element(By.CLASS_NAME, 'sp3')
                # Elementin içeriğini ekrana yazdır
                span = sp3Span.text

                balance = span.replace(',', '.')
                balance = balance.split(' ')
                balance = balance[0]
                balance = float(balance)
                if balance > float(str(yatirilanlimit)):
                    liElement.click()
                    break

            scroll_down(driver, 100)

            time.sleep(1)
            ibans = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="iban"]')))
            ibans.send_keys(iban)

            scroll_down(driver, 100)

            tutar = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="tutarContainer"]/div/div/div/div[1]/input[4]')))
            tutar.click()

            time.sleep(1)
            adsoyad = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="aliciAdSoyad"]')))
            adsoyad.send_keys("Hasan Hüseyin Durak")

            scroll_down(driver, 100)

            yatirilanlimit = yatirilanlimit.replace(".", ",")

            time.sleep(0.7)
            tutar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="tutarContainer"]/div/div/div/div[1]/input[4]')))
            tutar.send_keys(yatirilanlimit)

            scroll_down(driver, 100)

            time.sleep(0.7)
            aciklama = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="textfieldAciklama"]')))
            aciklama.send_keys(f"Has Mobile {yatirilanlimit} Ödemesi")

            time.sleep(1)
            gonder = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="submitButton"]')))
            gonder.click()

            scroll_down(driver, 100)

            time.sleep(1)
            onay = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="submitButton"]')))
            onay.click()

            hub_process.terminate()
            node_process.terminate()

            driver.quit()
            return True

        except Exception as e:
            driver.quit()
            hub_process.terminate()
            node_process.terminate()

            return False