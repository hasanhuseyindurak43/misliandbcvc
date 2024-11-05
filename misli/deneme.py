import sys
import random
import requests
from bs4 import BeautifulSoup
from random import randint
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QTabWidget, QMessageBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile
from PyQt5.QtNetwork import QNetworkProxy
from PyQt5.QtCore import QUrl

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Proxy Tab Widget Example")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("URL girin...")
        self.proxy_count_input = QLineEdit(self)
        self.proxy_count_input.setPlaceholderText("Kullanılacak proxy sayısını girin...")
        self.tab_count_input = QLineEdit(self)
        self.tab_count_input.setPlaceholderText("Açılacak sekme sayısını girin...")

        self.submit_button = QPushButton("Başlat", self)
        self.submit_button.clicked.connect(self.start_process)

        self.layout.addWidget(self.url_input)
        self.layout.addWidget(self.proxy_count_input)
        self.layout.addWidget(self.tab_count_input)
        self.layout.addWidget(self.submit_button)

    def start_process(self):
        url = self.url_input.text()
        proxy_count = int(self.proxy_count_input.text())
        tab_count = int(self.tab_count_input.text())

        if not url or proxy_count <= 0 or tab_count <= 0:
            QMessageBox.warning(self, "Hata", "Lütfen geçerli bilgiler girin.")
            return

        self.tabs = TabWidget(url, proxy_count, tab_count)
        self.tabs.show()

class TabWidget(QTabWidget):
    def __init__(self, url, proxy_count, tab_count):
        super().__init__()

        self.url = url
        self.proxy_count = proxy_count
        self.tab_count = tab_count

        for i in range(tab_count):
            tab = QWidget()
            tab_layout = QVBoxLayout()
            tab.setLayout(tab_layout)

            proxy = self.get_proxy()
            if proxy is None:
                QMessageBox.warning(self, "Hata", "Proxy alınamadı!")
                return
            
            tab_layout.addWidget(QLabel(f"Tab {i + 1} - Kullanılan Proxy: {proxy}"))

            # Proxy ile web engine oluştur
            self.open_browser_with_proxy(tab_layout, self.url, proxy)

            self.addTab(tab, f"Tab {i + 1}")

    def get_proxy(self):
        try:
            url = 'https://www.sslproxies.org/'
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')

            div = soup.find('div', class_='table-responsive')
            tbody = div.find("tbody")
            proxies = tbody.find_all("tr")

            if not proxies:
                return None

            proxy = proxies[randint(0, len(proxies) - 1)]
            proxy_ip = proxy.find_all("td")[0].get_text()
            proxy_port = proxy.find_all("td")[1].get_text()

            return f"{proxy_ip}:{proxy_port}"
        except Exception as e:
            print(f"Proxy alma hatası: {e}")
            return None

    def open_browser_with_proxy(self, layout, url, proxy):
        # QWebEngineProfile ile proxy ayarlarını yap
        profile = QWebEngineProfile.defaultProfile()
        self.set_proxy(proxy)

        # Sayfa ve tarayıcı oluştur
        page = QWebEnginePage(profile)
        browser = QWebEngineView()
        browser.setPage(page)
        
        # URL'yi QUrl nesnesine dönüştür
        browser.setUrl(QUrl(url))

        layout.addWidget(browser)

    def set_proxy(self, proxy):
        # Proxy ayarlarını uygula
        ip, port = proxy.split(':')
        proxy_object = QNetworkProxy(QNetworkProxy.HttpProxy, ip, int(port))
        QNetworkProxy.setApplicationProxy(proxy_object)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

