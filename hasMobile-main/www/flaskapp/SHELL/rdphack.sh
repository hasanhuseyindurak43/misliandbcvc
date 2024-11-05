#!/bin/bash

max_length=16

generate_and_save() {
    length=$1
    chars=$2

    # Kombinasyonları oluşturup dosyalara yaz
    for combination in $(echo $chars | tr -d '{}'); do
        echo $combination >> username.txt
        echo $combination >> password.txt
    done
}

# Dosyaları temizle
> username.txt
> password.txt

# Karakter kümesini oluştur
base_chars='{a..z}{0..9}{!@#$%^&*+.,<>}'

# Kombinasyonları oluştur ve kaydet
for length in $(seq 1 $max_length); do
    chars="$base_chars"
    for (( i=1; i<$length; i++ )); do
        chars="$chars$base_chars"
    done
    generate_and_save $length "$chars"
done