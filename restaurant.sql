-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 26, 2025 at 12:25 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

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
-- Table structure for table `ingredients`
--

CREATE TABLE `ingredients` (
  `ingredient_id` int(11) NOT NULL,
  `ingredient_name` text NOT NULL,
  `quantity` int(11) NOT NULL,
  `ingredient_type` text NOT NULL COMMENT 'ex. grams, ml, piece'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Dumping data for table `ingredients`
--

INSERT INTO `ingredients` (`ingredient_id`, `ingredient_name`, `quantity`, `ingredient_type`) VALUES
(1, 'potato', 50, 'KG'),
(2, 'oil', 20, 'L'),
(3, 'salt', 10, 'KG'),
(4, 'flour', 30, 'KG'),
(5, 'herbs', 5, 'KG'),
(6, 'cheese', 25, 'KG'),
(7, 'tomato', 24, 'KG'),
(8, 'ham', 15, 'KG'),
(9, 'sausage', 15, 'KG'),
(10, 'pasta', 50, 'KG'),
(11, 'beef', 30, 'KG'),
(12, 'chicken', 20, 'KG'),
(13, 'vegetable', 20, 'KG'),
(14, 'pork chop', 15, 'KG'),
(15, 'brad crumps', 10, 'KG'),
(16, 'egg', 120, 'piece');

-- --------------------------------------------------------

--
-- Table structure for table `loyalty_cards`
--

CREATE TABLE `loyalty_cards` (
  `guest_id` int(255) NOT NULL,
  `name` text NOT NULL,
  `surname` text NOT NULL,
  `phone_number` int(12) NOT NULL COMMENT 'format => +xxx 123-456-789',
  `discount` int(2) NOT NULL COMMENT '% value',
  `created_at` timestamp(6) NOT NULL DEFAULT current_timestamp(6),
  `modified_at` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `menu`
--

CREATE TABLE `menu` (
  `menu_id` int(100) NOT NULL,
  `position_name` text NOT NULL,
  `required_ingredients` text NOT NULL COMMENT 'ex. ingr1, ingr2, ingr3, ...',
  `quantity` text NOT NULL COMMENT 'quan1,quan2,quan3,quan...',
  `course_cost` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Dumping data for table `menu`
--

INSERT INTO `menu` (`menu_id`, `position_name`, `required_ingredients`, `quantity`, `course_cost`) VALUES
(1, 'Frytki', 'ziemniaki,olej,sól', '1,1,1', 8),
(2, 'Pizza', 'mąka,zioła,ser,pomidor,szynka,kielbasa', '1,1,3,2,2,1', 30),
(3, 'Sphagetti', 'makaron,pomidory,ser,zioła,wołowina', '1,3,2,2,1', 27),
(4, 'Rosół', 'kurczak,warzywa,zioła,sól', '2,1,2,1', 18),
(5, 'Schabowy z Ziemniakami', 'ziemniaki,schab,bułka tarta,zioła,jajko,', '1,1,1,1,2', 34);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL,
  `table_id` int(11) NOT NULL,
  `positions` text NOT NULL COMMENT 'ex. pos1, pos2, pos3, ...',
  `quantity` text NOT NULL COMMENT 'ex. quan1, quan2, quan3, ...',
  `order_status` varchar(255) NOT NULL DEFAULT 'Active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `transaction_id` int(100) NOT NULL,
  `order_id` int(100) NOT NULL,
  `course_names` text NOT NULL COMMENT 'ex. pos1, pos2, pos3, ...',
  `guest_id` int(100) DEFAULT NULL,
  `total_cost` int(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ingredients`
--
ALTER TABLE `ingredients`
  ADD PRIMARY KEY (`ingredient_id`),
  ADD KEY `ingredient_id` (`ingredient_id`);

--
-- Indexes for table `loyalty_cards`
--
ALTER TABLE `loyalty_cards`
  ADD PRIMARY KEY (`guest_id`);

--
-- Indexes for table `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`menu_id`),
  ADD KEY `required_ingredients` (`required_ingredients`(768));

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`transaction_id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `guest_id` (`guest_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ingredients`
--
ALTER TABLE `ingredients`
  MODIFY `ingredient_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `loyalty_cards`
--
ALTER TABLE `loyalty_cards`
  MODIFY `guest_id` int(255) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `menu`
--
ALTER TABLE `menu`
  MODIFY `menu_id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `transaction_id` int(100) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`),
  ADD CONSTRAINT `transactions_ibfk_2` FOREIGN KEY (`guest_id`) REFERENCES `loyalty_cards` (`guest_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
