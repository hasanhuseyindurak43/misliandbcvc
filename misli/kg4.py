from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta

class Application():
    def __init__(self):
        self.tcno, self.password, self.misli, self.ms, self.sistem, self.oynama, self.match_count = self.get_match_count()
        self.driver = self.start_browser()
        self.accept_cookies()
        self.scroll_to_bottom()
        self.html = self.get_html_source()
        self.maclar = self.parse_html()
        self.driver.quit()
        print("-" * 100)
        print("Seçilen Maçlar:", self.maclar)
        print("-" * 100)
        self.results = self.play_matches()
        self.print_combined_results()

    def get_match_count(self):
        # Kullanıcıdan TC kimlik numarası, şifre ve maç sayısını sormak
        tcno = input("Tc Kimlik Numarası Giriniz   : ")
        print("-" * 65)
        password = input("Parolanızı Giriniz           : ")
        print("-" * 65)
        misli = input("Misli Tutarı Giriniz         : ")
        print("-" * 65)
        print("Ms 1 derseniz : 5 maçı sistem1, sistem2, sistem3, sistem4, sistem5 şeklinde oynayabilirsiniz")
        print("Ms 2 derseniz : 5 maçı sistem2, sistem3, sistem4, sistem5 şeklinde oynayabilirsiniz")
        print("Ms 3 derseniz : 5 maçı sistem3, sistem4, sistem5 şeklinde oynayabilirsiniz")
        ms = input("Ms Giriniz : ")
        print("-" * 65)
        sistem = input("Sistem Olsun Mu? (Evet/Hayır): ")
        print("-" * 65)
        oynama = input("Maçlar Kaydedildikten Sonra Oynansın Mı? (Evet/Hayır): ")
        print("-" * 65)
        match_count = int(input("Kaç maç çekmek istiyorsunuz?: "))  # Ensure this is an integer
        print("-" * 65)
        return tcno, password, misli, ms, sistem, oynama, match_count

    def start_browser(self):
        # Tarayıcıyı başlatın
        driver = webdriver.Chrome()
        # Tarayıcı penceresini maksimum boyuta ayarlayın
        driver.maximize_window()
        url = "https://www.misli.com"
        # Belirtilen URL'ye gidin
        driver.get(f'{url}/iddaa/futbol')
        return driver

    def accept_cookies(self):
        try:
            # "onetrust-accept-btn-handler" id'sine sahip butonun görünmesini bekleyin ve tıklayın
            accept_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            accept_button.click()
            print("Çerezleri kabul ettim.")
        except Exception as e:
            print(f"Çerezleri kabul ederken bir hata oluştu: {e}")

    def scroll_to_bottom(self):
        # Sayfanın tamamen yüklenmesi için bekleyin
        time.sleep(5)  # Gerekirse bu süreyi ayarlayın
        # Sayfanın en altına kadar 100 piksel kademelerle kaydırma işlemi
        scroll_pause_time = 0.1  # Her kaydırma adımında bekleme süresi
        # Belirli bir sınır belirlemeksizin sayfanın sonuna kadar kaydırma
        for _ in range(100):  # Yeterli sayıda döngü
            self.driver.execute_script("window.scrollBy(0, 100);")
            time.sleep(scroll_pause_time)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            current_scroll_position = self.driver.execute_script("return window.pageYOffset + window.innerHeight")
            if current_scroll_position >= new_height:
                break

    def get_html_source(self):
        # Sayfanın HTML kaynağını alın
        return self.driver.page_source

    def parse_html(self):
        # BeautifulSoup ile HTML kaynağını parse edin
        soup = BeautifulSoup(self.html, 'html.parser')
        # 'bultenpre-futbol' id'sine sahip div'i bulun
        bultenpre_futbol_div = soup.find('div', id='bultenpre-futbol')
        maclar = []

        # Şu anki saati al
        now = datetime.now()

        # İki saat sonrasını hesapla
        two_hours_later = now + timedelta(hours=2)


        if bultenpre_futbol_div:
            # 'bulletinRowWrapperPre' classına sahip div'leri bulun
            bulletin_row_wrappers = bultenpre_futbol_div.find_all('div', class_='bulletinRowWrapperPre')
            url = "https://www.misli.com"

            for wrapper in bulletin_row_wrappers:
                # 'bulletinItemInside' classına sahip div'leri bulun
                bulletin_item_insides = wrapper.find_all('div', class_='bulletinItemInside')

                for item_inside in bulletin_item_insides:
                    # 'bulletinItemRow' classına sahip elementleri bulun
                    bulletin_item_rows = item_inside.find_all('div', class_='bulletinItemRow')

                    for item_row in bulletin_item_rows:
                        # 'bulletinTeamName bulletinHomeTeam' classına sahip span'ları bulun
                        # XPath ile metni alın
                        
                        
                        saat = item_row.find('span', class_='bulletinDate txtBlack000')
                        
                        if saat is not None:
                        
                            saattwo = saat.get_text(strip=True)
                            
                            team = item_row.find('span', class_='bulletinTeamName bulletinHomeTeam')
                            
                            ms = item_row.find('span', class_='bulletinInfo MBS infoMblNone')
                            
                            # HTML'deki saat bilgisini datetime nesnesine çevir
                            time_obj = datetime.strptime(saattwo, '%H:%M')
                            # Günün aynı saatine ayarla
                            time_obj = now.replace(hour=time_obj.hour, minute=time_obj.minute, second=0, microsecond=0)
                            # İki saat sonrasının üstündeki saatleri listeye ekle
                            if time_obj > two_hours_later:
                            
                                if team is not None:
                                    
                                    if ms is not None:
                                    
                                        saat = saat.text
                                        
                                        text = team.text
                                        
                                        ms = ms.text
                                        
                                        # Metni '-' karakterinden böl
                                        team_parts = text.split('-')
                                        
                                        if len(team_parts) == 2:
                                            home_team, away_team = team_parts
                                        else:
                                            # Handle cases with more than one '-'
                                            home_team = team_parts[0].strip()
                                            away_team = ' - '.join(part.strip() for part in team_parts[1:])

                                        
                                        home_team = home_team.strip()
                                        away_team = away_team.strip()

                                        # 'bulletinOddsWrapper' classına sahip div'leri bulun
                                        odds_wrappers = item_row.find_all('div', class_='bulletinOddsWrapper')

                                        for odds_wrapper in odds_wrappers:
                                            # 'eventDetailMobile' classına sahip 'a' etiketini bulun
                                            event_detail_link = odds_wrapper.find('a', class_='eventDetailMobile')
                                            if event_detail_link:
                                                href = event_detail_link.get('href')

                                                # 'oddsCount fs-14 fw-600' classına sahip 'span' etiketini bulun
                                                odds_count_span = event_detail_link.find('span', class_='oddsCount fs-14 fw-600')
                                                if odds_count_span:
                                                    odds_count_text = odds_count_span.text.replace('+', '').strip()
                                                    odds_count = int(odds_count_text)

                                                    # Oranların +260 ve +300 arasında olup olmadığını kontrol edin
                                                    if 42 <= odds_count <= 400 and ms == self.ms :
                                                        match_info = {
                                                            "saat": saat,
                                                            "home_team": home_team,
                                                            "away_team": away_team,
                                                            "ms": ms,
                                                            "href": f"{url}{href}",
                                                            "odds_count": odds_count
                                                        }
                                                        maclar.append(match_info)
                                                        print(f"Clock: {saat}")
                                                        print(f"Home Team: {home_team}")
                                                        print(f"Away Team: {away_team}")
                                                        print(f"Ms : {ms}")
                                                        print(f"Event Detail Link: {url}{href}")
                                                        print(f"Odds Count: {odds_count}")
                                                        print("-----")
                                                        # İstenilen maç sayısına ulaşıldıysa döngüyü sonlandırın
                                                        if len(maclar) >= self.match_count:
                                                            return maclar
        else:
            print('Div with id "bultenpre-futbol" not found.')
        return maclar

    def play_matches(self):
        results = []
        for match in self.maclar:
            # Yeni bir tarayıcı başlat
            self.driver = self.start_browser()

            # Yeni sekme aç
            self.driver.execute_script("window.open('');")
            # Yeni sekmeye geç
            self.driver.switch_to.window(self.driver.window_handles[-1])
            # Href'i aç
            self.driver.get(match["href"])

            try:
                # Çerezleri kabul et
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "onetrust-consent-sdk"))
                )
                cookie_div = self.driver.find_element(By.ID, "onetrust-consent-sdk")
                button_group = cookie_div.find_element(By.ID, "onetrust-button-group-parent")
                accept_button = button_group.find_element(By.ID, "onetrust-accept-btn-handler")
                accept_button.click()

                # Sayfanın yüklenmesini bekle
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "marketTabItem")))

                first_half_results = []

                # 'marketTabItem' classına sahip div'i bulun
                market_tabs = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'marketTabItem goller')]")

                for tab in market_tabs:
                    # 'marketItem' classına sahip div'in içindeki 'marketName' classına sahip p'yi bulun
                    market_items = tab.find_elements(By.CLASS_NAME, "detail-markets-wrapper")

                    for item in market_items:
                        market_title = item.find_element(By.CLASS_NAME, "market-name")

                        # Tam eşleşme için metni kontrol et
                        if market_title.text.strip() == "Karşılıklı Gol":

                            # 'marketOddWrapper' classına sahip div'in içindeki 'marketOdds' classına sahip div'leri bulun
                            odds_containers = item.find_elements(By.CLASS_NAME, "market-odd-wrapper")

                            for container in odds_containers:
                                odds_wrappers = container.find_elements(By.CLASS_NAME, "marketOdds")
                                
                                for wrapper in odds_wrappers:
                                    odd_items = wrapper.find_elements(By.CLASS_NAME, "oddItem")

                                    for odd_item in odd_items:
                                        try:
                                            odd_inside = odd_item.find_element(By.CLASS_NAME, "oddInside")
                                            odd_name_span = odd_inside.find_element(By.CLASS_NAME, "oddName")
                                            odd_value_span = odd_inside.find_element(By.CLASS_NAME, "oddValue")
                                            
                                            super_odd_wrappers = odd_value_span.find_elements(By.CLASS_NAME, "superOddWrapper")

                                            if super_odd_wrappers:  # Eğer superOddWrapper sınıfına sahip div bulunmuşsa
                                                # superOddWrapper bulunduysa, içinde superOdd sınıfına sahip span'ı bul
                                                super_odd_wrapper = super_odd_wrappers[0]
                                                super_odd_spans = super_odd_wrapper.find_elements(By.CLASS_NAME, "superOdd")
                                                
                                                if super_odd_spans:  # Eğer superOdd sınıfına sahip span bulunmuşsa
                                                    super_odd_span = super_odd_spans[0]
                                                    # Span içindeki değeri (metni) al
                                                    odd_value_text = super_odd_span.text.replace(",", ".").strip()
                                                    odd_value = float(odd_value_text)
                                            else:
                                                odd_value_text = odd_value_span.text.replace(",", ".").strip()
                                                odd_value = float(odd_value_text)

                                            odd_name = odd_name_span.text

                                            first_half_results.append({
                                                "home_team": match["home_team"],
                                                "away_team": match["away_team"],
                                                "odd_name": odd_name,
                                                "href": match["href"],
                                                "odd_value": odd_value
                                            })
                                        except Exception as e:
                                            print(f"An error occurred: {e}")

                results.append({
                    "home_team": match["home_team"],
                    "away_team": match["away_team"],
                    "first_half_results": first_half_results,
                })

            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                self.driver.quit()

        return results

    def print_combined_results(self):
        def combine(matches, current_combination, all_combinations):
            if len(current_combination) == len(matches):
                all_combinations.append(list(current_combination))
                return

            next_match_index = len(current_combination)
            next_match = matches[next_match_index]

            for result in next_match['first_half_results']:
                current_combination.append(result)
                combine(matches, current_combination, all_combinations)
                current_combination.pop()

        combined_results = []
        combine(self.results, [], combined_results)

        def perform_login(driver):
            # Çerezleri kabul et
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "onetrust-consent-sdk"))
            )
            cookie_div = driver.find_element(By.ID, "onetrust-consent-sdk")
            button_group = cookie_div.find_element(By.ID, "onetrust-button-group-parent")
            accept_button = button_group.find_element(By.ID, "onetrust-accept-btn-handler")
            accept_button.click()

            time.sleep(5)

            girisyap = driver.find_element(By.XPATH,
                                           '//*[@id="misli-app"]/header/div/div[1]/div/div/div/div/div[3]/div/button/span')
            girisyap.click()

            time.sleep(5)

            tcno = driver.find_element(By.XPATH, '//*[@id="username"]')
            tcno.send_keys(self.tcno)

            time.sleep(5)

            ps = driver.find_element(By.XPATH, '//*[@id="password"]')
            ps.send_keys(self.password)

            time.sleep(5)

            giristikla = driver.find_element(By.XPATH,
                                             '//*[@id="m-login"]/div/div[2]/div/div[3]/form/div[6]/div/button')
            giristikla.click()

        try:
            for i, combination in enumerate(combined_results, 1):
                # Her sekme için yeni bir tarayıcı başlatma ve giriş yapma
                time.sleep(5)
                driver = self.start_browser()
                perform_login(driver)

                combination_str = " - ".join([
                    f"{result['home_team']} - {result['away_team']} : {result['odd_name']} ({result['odd_value']})"
                    for result in combination
                ])

                print("-" * 100)
                print(f"{i} -) {combination_str} Oynanıyor....")
                print("-" * 100)

                for result in combination:
                    # Her bir maç için href bilgisini alıp Selenium ile tıklama işlemini yapacağız
                    href = result['href']
                    odd_name = result['odd_name']

                    # Tarayıcıda yeni sekme açma ve ilgili href'e gitme
                    driver.execute_script(f"window.open('{href}', '_blank');")
                    # Son açılan sekme üzerinde işlem yapabilmek için pencereyi geçiş yapalım
                    driver.switch_to.window(driver.window_handles[-1])

                    time.sleep(5)
                    
                    if odd_name == "Var":
                        var_tikla = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div[3]/div[4]/div[1]/div[2]/div[2]/div[2]/div/div[1]/span')
                        var_tikla.click()
                    elif odd_name == "Yok":
                        yok_tikla = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div[3]/div[4]/div[1]/div[2]/div[2]/div[2]/div/div[2]/span')
                        yok_tikla.click()

                    time.sleep(5)

                    try:
                        kapat = driver.find_element(By.XPATH, '//*[@id="newAmount"]/div/div[2]/div/div[1]/img')

                        kapat.click()
                    except Exception as e:
                        continue

                    # İşlemler arasında biraz bekleme süresi ekleyebilirsiniz
                    time.sleep(2)  # Örnek olarak 2 saniye bekleme

                sistem_li_texts = []
                mac_sayi = 0

                if self.sistem == "Evet":

                    # headerSlipWrapper betslip-show slipPre divin içindeki headerSlipMain clasa sahip dive erişin
                    header_slip_main = driver.find_element(By.CSS_SELECTOR,
                                                           "div.headerSlipWrapper.betslip-show.slipPre .headerSlipMain")

                    # slipBottom classa sahip dive erişin
                    slip_bottom = header_slip_main.find_element(By.CSS_SELECTOR, ".slipBottom")

                    # sMatchesSystemLogic classa sahip divin içindeki sMatchesSystemUl classa sahip ul öğesini bulun
                    matches_system_ul = slip_bottom.find_element(By.CSS_SELECTOR,
                                                                 "div.sMatchesSystemLogic .sMatchesSystemUl")

                    # ul içindeki tüm li öğelerini bulun ve her birine tek tek tıklayın
                    li_elements = matches_system_ul.find_elements(By.TAG_NAME, "li")
                    for li in li_elements:
                        li.click()

                        sistem = li.text

                        # sMathcesCouponAmount classa sahip divin içindeki sMathcesFold classa sahip divi bulun
                        s_matches_fold_div = driver.find_element(By.CSS_SELECTOR,
                                                                 "div.sMathcesCouponAmount .sMathcesFold")

                        # sMathcesFold classa sahip divin içindeki form-group classa sahip divi bulun
                        form_group_div = s_matches_fold_div.find_element(By.CSS_SELECTOR, ".form-group")

                        # form-group classa sahip divin içindeki sMathcesFoldInput classa sahip input'u bulun
                        input_element = form_group_div.find_element(By.CSS_SELECTOR, ".sMathcesFoldInput")

                        input_element.clear()

                        # input alanına 71 sayısını gönderin
                        input_element.send_keys(f"{self.misli}")

                        makskazanc = driver.find_element(By.XPATH,
                                                         '//*[@id="misli-app"]/header/div/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div[6]/div[3]/span[2]').text

                        sistem_tutar = driver.find_element(By.XPATH,
                                                           '//*[@id="misli-app"]/header/div/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div[6]/div[1]/span[2]').text

                        sistem_oran = driver.find_element(By.XPATH,
                                                          '//*[@id="misli-app"]/header/div/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div[6]/div[2]/span[2]').text

                        sistem_li_texts.append((sistem, makskazanc, sistem_oran, sistem_tutar))

                        time.sleep(1)  # Her tıklamadan sonra kısa bir süre bekleyin

                elif self.sistem == "Hayır":
                    mac_sayi += 1
                    # sMathcesCouponAmount classa sahip divin içindeki sMathcesFold classa sahip divi bulun
                    s_matches_fold_div = driver.find_element(By.CSS_SELECTOR,
                                                             "div.sMathcesCouponAmount .sMathcesFold")

                    # sMathcesFold classa sahip divin içindeki form-group classa sahip divi bulun
                    form_group_div = s_matches_fold_div.find_element(By.CSS_SELECTOR, ".form-group")

                    # form-group classa sahip divin içindeki sMathcesFoldInput classa sahip input'u bulun
                    input_element = form_group_div.find_element(By.CSS_SELECTOR, ".sMathcesFoldInput")

                    input_element.clear()

                    # input alanına 71 sayısını gönderin
                    input_element.send_keys(f"{self.misli}")

                    makskazanc = driver.find_element(By.XPATH,
                                                     '//*[@id="misli-app"]/header/div/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div[6]/div[3]/span[2]').text

                    mac_tutar = driver.find_element(By.XPATH,
                                                    '//*[@id="misli-app"]/header/div/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div[6]/div[1]/span[2]').text

                    mac_oran = driver.find_element(By.XPATH,
                                                   '//*[@id="misli-app"]/header/div/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div[6]/div[2]/span[2]').text

                    sistem_li_texts.append((mac_sayi, makskazanc, mac_oran, mac_tutar))

                    time.sleep(1)  # Her tıklamadan sonra kısa bir süre bekleyin

                time.sleep(2)

                # sMathcesCouponAmount classa sahip divin içindeki sMathcesFold classa sahip divi bulun
                s_matches_fold_div = driver.find_element(By.CSS_SELECTOR, "div.sMathcesCouponAmount .sMathcesFold")

                # sMathcesFold classa sahip divin içindeki form-group classa sahip divi bulun
                form_group_div = s_matches_fold_div.find_element(By.CSS_SELECTOR, ".form-group")

                # form-group classa sahip divin içindeki sMathcesFoldInput classa sahip input'u bulun
                input_element = form_group_div.find_element(By.CSS_SELECTOR, ".sMathcesFoldInput")

                input_element.clear()

                # input alanına 71 sayısını gönderin
                input_element.send_keys(f"{self.misli}")

                time.sleep(2)

                # XPath ile belirtilen elemente tıklayın
                # element = driver.find_element(By.XPATH, '//*[@id="misli-app"]/header/div/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div[6]/div[5]/button[2]/img')
                # element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/header/div/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div[6]/div[5]/button[2]/img')
                element = driver.find_element(By.CSS_SELECTOR, 'button.slipBtn:nth-child(2)')
                
                element.click()

                time.sleep(2)

                # v--modal-box v--modal classa sahip divin içindeki m-body classına sahip dive erişin
                modal_body = driver.find_element(By.CSS_SELECTOR, "div.v--modal-box.v--modal .m-body")

                # m-body classına sahip divin içindeki form-group classa sahip dive erişin
                form_group = modal_body.find_element(By.CSS_SELECTOR, ".form-group")

                # form-group classına sahip divin içindeki pristine untouched classa sahip input'u bulun
                input_element = form_group.find_element(By.CSS_SELECTOR, "input.pristine.untouched")

                input_element.clear()

                # input alanına "Deneme-Kupon" metnini gönderin
                input_element.send_keys(f"Deneme-Kupon-{i}")

                kaydet = driver.find_element(By.XPATH, '//*[@id="SaveCoupon"]/div/div[2]/div/div[3]/form/div[2]/button[2]')
                kaydet.click()

                time.sleep(5)

                kapat = driver.find_element(By.XPATH, '//*[@id="SaveCoupon"]/div/div[2]/div/div[2]/div/div/button[1]')
                kapat.click()

                if self.oynama == "Evet":
                    oynatikla = driver.find_element(By.XPATH, '//*[@id="misli-app"]/header/div/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div[6]/div[5]/button[3]')
                    oynatikla.click()

                elif self.oynama == "Hayır":
                    pass

                time.sleep(10)

                combination_str = " - ".join([
                    f"{result['home_team']} - {result['away_team']} : {result['odd_name']} ({result['odd_value']})"
                    for result in combination
                ])

                print("-" * 100)
                print(f"{i} -) {combination_str} Oynandı...")
                print("-" * 100)
                if self.sistem == "Evet":
                    for sistem, makskazanc, sistem_oran, sistem_tutar in sistem_li_texts:
                        print(
                            f"Sistem: {sistem} / Maksimum Kazanç: {makskazanc} / Sistem Oran : {sistem_oran} / Sistem Tutar : {sistem_tutar}")
                elif self.sistem == "Hayır":
                    for mac_sayi, makskazanc, mac_oran, mac_tutar in sistem_li_texts:
                        print(
                            f"Maç: {mac_sayi} / Maksimum Kazanç: {makskazanc} / Maç Oran : {mac_oran} / Maç Tutar : {mac_tutar}")
                print("-" * 100)

            # Tüm işlemler bittiğinde tarayıcıyı kapatma
            driver.quit()

        except Exception as e:
            print(f"Hata oluştu: {str(e)}")
            driver.quit()


if __name__ == '__main__':
    app = Application()
