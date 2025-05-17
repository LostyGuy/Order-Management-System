-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Maj 15, 2025 at 02:28 PM
-- Wersja serwera: 10.4.32-MariaDB
-- Wersja PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `restaurant`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `dish_ingredients`
--

CREATE TABLE `dish_ingredients` (
  `id` int(11) NOT NULL,
  `dish_id` int(11) NOT NULL,
  `ingredient_id` int(11) NOT NULL,
  `quantity_required` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `dish_ingredients`
--

INSERT INTO `dish_ingredients` (`id`, `dish_id`, `ingredient_id`, `quantity_required`) VALUES
(1, 1, 2, 0.40),
(2, 1, 1, 0.10),
(3, 1, 3, 0.01),
(4, 2, 3, 0.01),
(5, 2, 4, 0.50),
(6, 2, 5, 0.01),
(7, 2, 6, 0.10),
(8, 2, 7, 0.80),
(9, 2, 8, 0.30),
(10, 2, 9, 0.30),
(11, 3, 2, 0.03),
(12, 3, 3, 0.02),
(13, 3, 5, 0.20),
(14, 3, 7, 1.00),
(15, 3, 10, 0.60),
(16, 3, 11, 1.00),
(17, 4, 3, 0.02),
(18, 4, 5, 0.20),
(19, 4, 10, 0.40),
(20, 4, 13, 1.00),
(21, 5, 1, 0.40),
(22, 5, 2, 0.08),
(23, 5, 3, 0.01),
(24, 5, 5, 0.10),
(25, 5, 14, 0.20),
(26, 5, 15, 0.60),
(27, 5, 16, 0.10),
(28, 5, 17, 2.00);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `ingredients`
--

CREATE TABLE `ingredients` (
  `ingredient_id` int(11) NOT NULL,
  `ingredient_name` varchar(100) NOT NULL,
  `quantity` decimal(10,2) NOT NULL,
  `locked_quantity` decimal(10,2) DEFAULT 0.00,
  `unit` enum('KG','L','piece') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ingredients`
--

INSERT INTO `ingredients` (`ingredient_id`, `ingredient_name`, `quantity`, `locked_quantity`, `unit`) VALUES
(1, 'potato', 50.00, 0.00, 'KG'),
(2, 'oil', 20.00, 0.00, 'L'),
(3, 'salt', 5.00, 0.00, 'KG'),
(4, 'flour', 15.00, 0.00, 'KG'),
(5, 'herb', 2.00, 0.00, 'KG'),
(6, 'cheese', 10.00, 0.00, 'KG'),
(7, 'tomato', 15.00, 0.00, 'KG'),
(8, 'ham', 5.00, 0.00, 'KG'),
(9, 'sausage', 5.00, 0.00, 'KG'),
(10, 'pasta', 10.00, 0.00, 'KG'),
(11, 'beef', 25.00, 0.00, 'KG'),
(12, 'potato', 5.00, 0.00, 'KG'),
(13, 'chicken', 25.00, 0.00, 'KG'),
(14, 'vegetable', 15.00, 0.00, 'KG'),
(15, 'pork chop', 15.00, 0.00, 'KG'),
(16, 'bread crumps', 5.00, 0.00, 'KG'),
(17, 'egg', 500.00, 0.00, 'piece');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `menu_items`
--

CREATE TABLE `menu_items` (
  `dish_id` int(11) NOT NULL,
  `dish_name` varchar(100) NOT NULL,
  `course_cost` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `menu_items`
--

INSERT INTO `menu_items` (`dish_id`, `dish_name`, `course_cost`) VALUES
(1, 'Fries', 8.00),
(2, 'Pizza', 30.00),
(3, 'Sphagetti', 27.00),
(4, 'Chicken Broth', 18.00),
(5, 'Pork Chop with Potatoes', 34.00);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `ordered_dishes`
--

CREATE TABLE `ordered_dishes` (
  `id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `dish_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `orders`
--

CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL,
  `display_id` int(11) NOT NULL,
  `order_status` enum('active','completed','cancelled') DEFAULT 'active',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `transactions`
--

CREATE TABLE `transactions` (
  `transaction_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `full_cost` decimal(10,2) NOT NULL,
  `discount` decimal(5,2) DEFAULT 0.00,
  `status` enum('paid','notpaid') DEFAULT 'notpaid'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `dish_ingredients`
--
ALTER TABLE `dish_ingredients`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dish_id` (`dish_id`),
  ADD KEY `ingredient_id` (`ingredient_id`);

--
-- Indeksy dla tabeli `ingredients`
--
ALTER TABLE `ingredients`
  ADD PRIMARY KEY (`ingredient_id`);

--
-- Indeksy dla tabeli `menu_items`
--
ALTER TABLE `menu_items`
  ADD PRIMARY KEY (`dish_id`);

--
-- Indeksy dla tabeli `ordered_dishes`
--
ALTER TABLE `ordered_dishes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `dish_id` (`dish_id`);

--
-- Indeksy dla tabeli `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`);

--
-- Indeksy dla tabeli `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`transaction_id`),
  ADD KEY `order_id` (`order_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `dish_ingredients`
--
ALTER TABLE `dish_ingredients`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `ingredients`
--
ALTER TABLE `ingredients`
  MODIFY `ingredient_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `menu_items`
--
ALTER TABLE `menu_items`
  MODIFY `dish_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `ordered_dishes`
--
ALTER TABLE `ordered_dishes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `transaction_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `dish_ingredients`
--
ALTER TABLE `dish_ingredients`
  ADD CONSTRAINT `dish_ingredients_ibfk_1` FOREIGN KEY (`dish_id`) REFERENCES `menu_items` (`dish_id`),
  ADD CONSTRAINT `dish_ingredients_ibfk_2` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients` (`ingredient_id`);

--
-- Constraints for table `ordered_dishes`
--
ALTER TABLE `ordered_dishes`
  ADD CONSTRAINT `ordered_dishes_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`),
  ADD CONSTRAINT `ordered_dishes_ibfk_2` FOREIGN KEY (`dish_id`) REFERENCES `menu_items` (`dish_id`);

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
