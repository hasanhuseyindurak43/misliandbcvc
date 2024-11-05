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
    def go_on_mobile(self, tc="12071695146", parola="196835", kad=None, ksoyad=None, kiban=None, kcmiktar=None):
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
            driver = webdriver.Remote(command_executor="http://78.186.180.175:4444/wd/hub", options=chrome_options)

            driver.maximize_window()
            driver.get(
                "https://esube.burgan.com.tr/burgandijital/login-flow?culture=tr-TR")

            wait = WebDriverWait(driver, 10)

            tcgiris = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Username"]')))
            tcgiris.send_keys(tc)

            time.sleep(0.7)

            parolagiris = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Password"]')))
            parolagiris.send_keys(parola)

            time.sleep(0.7)
            girisyap = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="LoginButton"]')))
            girisyap.click()

            go_transfer = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="MoneyTransfer"]')))
            go_transfer.click()

            time.sleep(1)

            go_transfer_fast = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="FastButton"]')))
            go_transfer_fast.click()

            time.sleep(1)

            hesapsecim = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="AccountChoosing"]')))
            hesapsecim.click()

            # "options show-option" class'ına sahip elementi seçin
            options_element = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="externalMoneyTransferForm_sourceIBAN"]/div/div[2]')))

            # "BrgScroolbar" class'ına sahip alt elementi seçin
            brg_scrollbar_element = options_element.find_element(By.XPATH,
                                                                 '//*[@id="externalMoneyTransferForm_sourceIBAN"]/div/div[2]/div')

            # "iBox" class'ına sahip alt elementleri seçin
            iBox_elements = brg_scrollbar_element.find_elements(By.CLASS_NAME, 'iBox')

            # Her bir iBox elementi için işlem yapın
            for iBox_element in iBox_elements:
                # "RPan" class'ına ait altındaki "span" elementini seçin
                rpan_span_element = iBox_element.find_element(By.CLASS_NAME, 'RPan').find_element(By.TAG_NAME, 'span')

                # "span" elementinin metnini alın
                span_text = rpan_span_element.text

                balance = span_text.replace(',', '.')
                balance = balance.split(' ')
                balance = balance[0]
                balance = float(balance)

                if balance > 0.00:
                    # İstenilen şartı sağlayan elemente tıklamadan önce tıklanabilirliğini kontrol et
                    iBox_element.click()

                time.sleep(1)

                iban = kiban.split('TR')
                iban = iban[1]
                ibans = driver.find_element(By.XPATH, '//*[@id="externalMoneyTransferForm_targetIBAN"]')
                ibans.send_keys(iban)

                time.sleep(3)

                isimsoyisim = f"{kad} {ksoyad}"
                ad = driver.find_element(By.XPATH, '//*[@id="externalMoneyTransferForm_targetFullName"]')
                ad.send_keys(isimsoyisim)

                time.sleep(1)

                kcmiktar = int(kcmiktar)
                tutar = driver.find_element(By.XPATH, '//*[@id="externalMoneyTransferForm_amount"]')
                tutar.send_keys(kcmiktar)

                time.sleep(1)

                # select elementini tanımla
                select_element = driver.find_element(By.ID, "externalMoneyTransferForm_transferReason")

                # Select sınıfını kullanarak select elementini bir nesneye atayın
                select = Select(select_element)

                # Seçeneği option value'suna göre seç
                select.select_by_value("7")

                time.sleep(3)

                aciklama = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="externalMoneyTransferForm_explanation"]')))
                aciklama.send_keys(
                    f"{kad} {ksoyad} Has Mobile da bulunan cüzdanınızdan {kcmiktar} TL gönderim sağlanmıstır.")

                time.sleep(1)

                kaydet = driver.find_element(By.XPATH,
                                             '/html/body/app-root/internet-banking-dashboard/div[1]/div/div/div/money-transfer-dashboard/external-transfer-start/div/div[1]/div/form/div[3]/section/div/label/i')
                kaydet.click()
                yaz = driver.find_element(By.XPATH,
                                          '//*[@id="externalMoneyTransferForm_registeredTransferName"]')
                yaz.send_keys(isimsoyisim)

                time.sleep(1)

                devam = driver.find_element(By.XPATH, '//*[@id="EftHavaleContinue"]/span')
                devam.click()

                time.sleep(1)

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                onay = wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="EftHavaleConfirmation"]')))
                onay.click()

                time.sleep(10)

                driver.quit()

                hub_process.terminate()
                node_process.terminate()

                return True

        except Exception as e:
            driver.quit()

            hub_process.terminate()
            node_process.terminate()

            return e