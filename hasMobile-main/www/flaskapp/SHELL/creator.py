import itertools

# Karakter kümesi
chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*+.,<>'

# Kombinasyonları dosyaya yaz
def generate_and_save(length, file):
    with open(file, 'a') as f:
        for combination in itertools.product(chars, repeat=length):
            f.write(''.join(combination) + '\n')

# Dosyaları temizle
with open('username.txt', 'w') as f:
    pass
with open('password.txt', 'w') as f:
    pass

# Uzunlukları belirle ve kombinasyonları oluştur
for length in range(1, 17):  # 1'den 16'ya kadar uzunluklar
    generate_and_save(length, 'username.txt')
    generate_and_save(length, 'password.txt')