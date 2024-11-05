import requests

url = 'https://www.hostingcloud.racing/kI4o.js'  # İndirilecek dosyanın URL'si
file_name = 'kI4o.js'  # İndirilecek dosyanın kaydedileceği isim

response = requests.get(url, stream=True)
if response.status_code == 200:
    with open(file_name, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print(f"{file_name} başarıyla indirildi.")
else:
    print(f"Dosya indirilirken bir hata oluştu. Durum kodu: {response.status_code}")