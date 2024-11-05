-- phpMyAdmin SQL Dump
-- version 5.1.1deb5ubuntu1
-- https://www.phpmyadmin.net/
--
-- Anamakine: localhost:3306
-- Üretim Zamanı: 20 Oca 2024, 17:53:08
-- Sunucu sürümü: 8.0.35-0ubuntu0.22.04.1
-- PHP Sürümü: 8.1.2-1ubuntu2.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `hasmobile`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `cuzdan`
--

CREATE TABLE `cuzdan` (
  `cid` int NOT NULL,
  `username` varchar(1500) COLLATE utf8mb4_turkish_ci NOT NULL,
  `cuzdan_miktar` decimal(10,2) NOT NULL,
  `cuzdan_r_date` datetime NOT NULL,
  `odeme_tarihi` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

--
-- Tablo döküm verisi `cuzdan`
--

INSERT INTO `cuzdan` (`cid`, `username`, `cuzdan_miktar`, `cuzdan_r_date`, `odeme_tarihi`) VALUES
(9, '29', '0.00', '2024-01-20 04:43:46', '2024-01-20'),
(10, '30', '0.00', '2024-01-10 13:10:19', '2024-01-10');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `faiz`
--

CREATE TABLE `faiz` (
  `fid` int NOT NULL,
  `username` varchar(1500) COLLATE utf8mb4_turkish_ci NOT NULL,
  `hesap_adi` varchar(1500) COLLATE utf8mb4_turkish_ci NOT NULL,
  `tutar` decimal(10,2) NOT NULL,
  `vade_b_tarih` date NOT NULL,
  `vade_bitis_tarih` date NOT NULL,
  `vade_s_tutar` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `packets`
--

CREATE TABLE `packets` (
  `pid` int NOT NULL,
  `paket_adi` varchar(1500) COLLATE utf8mb4_turkish_ci NOT NULL,
  `paket_aciklama` varchar(1500) COLLATE utf8mb4_turkish_ci NOT NULL,
  `paket_f_oran` float NOT NULL,
  `paket_f_gun` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

--
-- Tablo döküm verisi `packets`
--

INSERT INTO `packets` (`pid`, `paket_adi`, `paket_aciklama`, `paket_f_oran`, `paket_f_gun`) VALUES
(1, 'Günlük Paket', 'Günlük paket ile her gece yatırımına 5% faiz uygulansın. Sende uyurken kazan..!', 5, 1),
(2, 'Aylık Paket', 'Aylık paket ile aylık %34 faiz uygulansın. Sende uyurken kazan..!', 34.22, 32),
(3, '3 Aylık Paket', 'Aylık paket ile aylık %35 faiz uygulansın. Sende uyurken kazan..!', 35.707, 92),
(4, '6 Aylık Paket', 'Aylık paket ile aylık %32 faiz uygulansın. Sende uyurken kazan..!', 32.087, 182);

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `ptalep`
--

CREATE TABLE `ptalep` (
  `pid` int NOT NULL,
  `username` varchar(1500) COLLATE utf8mb4_turkish_ci NOT NULL,
  `ptalep_isim` varchar(1500) COLLATE utf8mb4_turkish_ci NOT NULL,
  `ptalep_soyisim` varchar(1500) COLLATE utf8mb4_turkish_ci NOT NULL,
  `ptalep_iban` varchar(1500) COLLATE utf8mb4_turkish_ci NOT NULL,
  `ptalep_tutar` decimal(10,2) NOT NULL,
  `ptalep_onay` int NOT NULL,
  `ptalep_r_date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `users`
--

CREATE TABLE `users` (
  `uid` int NOT NULL,
  `username` varchar(1500) CHARACTER SET utf8mb4 COLLATE utf8mb4_turkish_ci NOT NULL,
  `usereposta` varchar(1500) CHARACTER SET utf8mb4 COLLATE utf8mb4_turkish_ci NOT NULL,
  `userpassword` varchar(1500) CHARACTER SET utf8mb4 COLLATE utf8mb4_turkish_ci NOT NULL,
  `user_giris` int NOT NULL,
  `user_statu` int NOT NULL,
  `user_r_date` date NOT NULL,
  `user_u_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

--
-- Tablo döküm verisi `users`
--

INSERT INTO `users` (`uid`, `username`, `usereposta`, `userpassword`, `user_giris`, `user_statu`, `user_r_date`, `user_u_date`) VALUES
(29, 'b\"\\x112\\xe5>\\x98A\\xbat\\xe2\\x01\\xbd\\x1by\\x8d\\xeb-\\xfc\'\\x9aZ\\xd6\\xe1\\x7f!PH\\xc7\\xc6\\xc3\\xb1\\xb7T\"', 'b\'\\x88\\x05\\x05j\\xd6\\x91\\xee\\xa2\\xbb\\xe4\\x87\\x9e\\x8a\\xe38-\\x90\\xd0o\\xf9\\xc8%\\xcf\\xfe\\xae\\xc4\\xecQD\\xbb1\\xb9q\\xedR\\x1f\\x13\\xeb\\x83O\\x97SR\\x9f_c\\xc3\\xc5\'', 'b\'tUR\\xff\\x91\\xc2\\x8fB\\x9f\\x01q\"\\xea\\x82\\xca\\xe0\\x12!M\\xbfZl\\xa3\\x950\\xf4\\x8b{\\xe0\\xcdY\\x94\'', 1, 2, '2024-01-09', '2024-01-20'),
(30, 'b\'\\x112\\xe5>\\x98A\\xbat\\xde\\x06\\x046\\xba_\\x08\\xe0\\x8a\\x9c\\xa9\\xbbX\\xcbr\\x06\\xeb\\xcd\\xf2\\x18m\\xbc\\xf9A\'', 'b\'?\\x9a\\xe7\\xcf@\\xd9\\xcf`\\x0e>\\x95\\xfe!\\xc6\\xb9\\xc5\\x9bH\\xab\\x18\\xe2\\x01Ye*\\x1c\\xf6\\xca\\x03\\xcf\\xf5dJ\\\\\\xb9`\\x87\\xad5\\xda\\x8e\\xca\\x0c\\xb77\\xceV\\x85\\xa1\\xcdc\\xd0\\xfbEa\\xd0\'', 'b\'tUR\\xff\\x91\\xc2\\x8fB\\x9f\\x01q\"\\xea\\x82\\xca\\xe0\\x12!M\\xbfZl\\xa3\\x950\\xf4\\x8b{\\xe0\\xcdY\\x94\'', 0, 2, '2024-01-10', '2024-01-10');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `usersiban`
--

CREATE TABLE `usersiban` (
  `ubid` int NOT NULL,
  `username` varchar(1500) CHARACTER SET utf8mb4 COLLATE utf8mb4_turkish_ci NOT NULL,
  `user_g_adi` varchar(1500) CHARACTER SET utf8mb4 COLLATE utf8mb4_turkish_ci NOT NULL,
  `user_g_soyadi` varchar(1500) CHARACTER SET utf8mb4 COLLATE utf8mb4_turkish_ci NOT NULL,
  `user_iban` varchar(1500) CHARACTER SET utf8mb4 COLLATE utf8mb4_turkish_ci NOT NULL,
  `user_iban_r_date` date NOT NULL,
  `user_iban_u_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

--
-- Tablo döküm verisi `usersiban`
--

INSERT INTO `usersiban` (`ubid`, `username`, `user_g_adi`, `user_g_soyadi`, `user_iban`, `user_iban_r_date`, `user_iban_u_date`) VALUES
(14, '29', 'b\'\\xc4U\\n\\xea@\\xf9\\x8c\\x9a\\xe3\\x9b\\xda\\xd9\\x1f\\x91M!\\xe1\\xf7 \\xed\\xeeg\\\\Bi\\xa97v\\xec\\xcbJ\\x1e\'', 'b\'J\\x10\\xf4R\\x7f\\xe0#S\\xd9\\xc6\\xf2\\xca\\x03\\x9b\\tF\\x96q\\xe5y\\xf6c\\r\\xeb\'', 'b\'\\x84\\xf6\\x8e4\\x9a\\xd6L\\xb7\\x1bca\\xa4d\\xc6\\x95?yO9h\\x0cl\\x0b\\x9f\\xf4\\x0b\\x00\\r\\xf7\\n\\xfca\\xf7T\\xd2\\xe6k\\x85\\x12JF\\xfc\\x88\\x94N\\x1f\\x0c\\xdf\'', '2024-01-09', '2024-01-09'),
(15, '30', 'b\'\\xc4U\\n\\xea@\\xf9\\x8c\\x9a\\xe3\\x9b\\xda\\xd9\\x1f\\x91M!\\xe1\\xf7 \\xed\\xeeg\\\\Bi\\xa97v\\xec\\xcbJ\\x1e\'', 'b\'J\\x10\\xf4R\\x7f\\xe0#S\\xd9\\xc6\\xf2\\xca\\x03\\x9b\\tF\\x96q\\xe5y\\xf6c\\r\\xeb\'', 'b\"\\x9f\\xf3\'4MR\\xc7\\x99\\xcd\\xee\\xfcd\\xde\\x12\\xe2\\x8a\\xeeM\\x11\\xfc\\xde\\xc0\\xfa\\x16\\x07\\x99\\xa7\\x10\'3\\xea\\x87\\xfc\\xce?\\xc5\\x12\\x856\\xdc\\xc4&\\x03\\x05b\\x92z\\xaa*I\\n[;\\xd0\\x89?\"', '2024-01-10', '2024-01-10');

--
-- Dökümü yapılmış tablolar için indeksler
--

--
-- Tablo için indeksler `cuzdan`
--
ALTER TABLE `cuzdan`
  ADD PRIMARY KEY (`cid`);

--
-- Tablo için indeksler `faiz`
--
ALTER TABLE `faiz`
  ADD PRIMARY KEY (`fid`);

--
-- Tablo için indeksler `packets`
--
ALTER TABLE `packets`
  ADD PRIMARY KEY (`pid`);

--
-- Tablo için indeksler `ptalep`
--
ALTER TABLE `ptalep`
  ADD PRIMARY KEY (`pid`);

--
-- Tablo için indeksler `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`uid`);

--
-- Tablo için indeksler `usersiban`
--
ALTER TABLE `usersiban`
  ADD PRIMARY KEY (`ubid`);

--
-- Dökümü yapılmış tablolar için AUTO_INCREMENT değeri
--

--
-- Tablo için AUTO_INCREMENT değeri `cuzdan`
--
ALTER TABLE `cuzdan`
  MODIFY `cid` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Tablo için AUTO_INCREMENT değeri `faiz`
--
ALTER TABLE `faiz`
  MODIFY `fid` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=64;

--
-- Tablo için AUTO_INCREMENT değeri `packets`
--
ALTER TABLE `packets`
  MODIFY `pid` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Tablo için AUTO_INCREMENT değeri `ptalep`
--
ALTER TABLE `ptalep`
  MODIFY `pid` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- Tablo için AUTO_INCREMENT değeri `users`
--
ALTER TABLE `users`
  MODIFY `uid` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- Tablo için AUTO_INCREMENT değeri `usersiban`
--
ALTER TABLE `usersiban`
  MODIFY `ubid` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

DELIMITER $$
--
-- Olaylar
--
CREATE DEFINER=`barron4335`@`%` EVENT `cikis_etkinligi_6265` ON SCHEDULE AT '2024-01-20 18:04:50' ON COMPLETION NOT PRESERVE ENABLE DO UPDATE `users`SET `user_giris` = 0 WHERE `uid` = 29$$

DELIMITER ;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
