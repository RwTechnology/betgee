-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost:8889
-- Généré le : lun. 09 jan. 2023 à 22:03
-- Version du serveur :  5.7.34
-- Version de PHP : 7.4.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `geebet`
--

-- --------------------------------------------------------

--
-- Structure de la table `bets`
--

CREATE TABLE `bets` (
  `id` int(11) NOT NULL,
  `code_pariage` varchar(10) NOT NULL,
  `account_id` int(11) NOT NULL,
  `bet_date` date NOT NULL,
  `bet_amount` double(7,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `credits`
--

CREATE TABLE `credits` (
  `id` int(11) NOT NULL,
  `code_user` int(11) NOT NULL,
  `amount` float(7,2) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `credits`
--

INSERT INTO `credits` (`id`, `code_user`, `amount`, `date`) VALUES
(1, 522, 10.00, '2023-01-05'),
(2, 522, 20.00, '2023-01-06'),
(3, 5325, 100.00, '2023-01-06'),
(4, 522, 90.00, '2023-01-09'),
(5, 522, 10.00, '2023-01-09'),
(6, 8399, 100.00, '2023-01-09'),
(7, 8399, 100.00, '2023-01-09'),
(8, 8399, 0.00, '2023-01-09'),
(9, 8399, 0.00, '2023-01-09'),
(10, 8399, 100.00, '2023-01-09');

-- --------------------------------------------------------

--
-- Structure de la table `matchs`
--

CREATE TABLE `matchs` (
  `id` varchar(255) NOT NULL,
  `match_type` varchar(255) NOT NULL,
  `country` varchar(255) NOT NULL,
  `match_date` date NOT NULL,
  `match_time` varchar(255) NOT NULL,
  `receiver_team` varchar(255) NOT NULL,
  `visitor_team` varchar(255) NOT NULL,
  `cote_match` double(7,2) NOT NULL,
  `score` varchar(255) NOT NULL,
  `state` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `match_choisi`
--

CREATE TABLE `match_choisi` (
  `id` int(11) NOT NULL,
  `code_pariage` varchar(10) NOT NULL,
  `id_match` int(11) NOT NULL,
  `equipe_choisie` varchar(50) NOT NULL,
  `cote` double NOT NULL,
  `score_prevu` varchar(50) NOT NULL,
  `etat_pariage` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `payments`
--

CREATE TABLE `payments` (
  `id` int(11) NOT NULL,
  `bet_id` int(11) NOT NULL,
  `payment_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `date_of_birth` date NOT NULL,
  `gender` enum('M','F') NOT NULL,
  `phone` varchar(255) NOT NULL,
  `nif_cin` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `balance` decimal(10,2) NOT NULL DEFAULT '0.00',
  `status` enum('active','inactive','deleted') NOT NULL DEFAULT 'active',
  `user_type` enum('admin','user') NOT NULL DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `users`
--

INSERT INTO `users` (`id`, `last_name`, `first_name`, `username`, `date_of_birth`, `gender`, `phone`, `nif_cin`, `password`, `balance`, `status`, `user_type`) VALUES
(1, 'Dadenskys', 'PIERRE', 'Dadenskey', '2023-01-26', 'M', '+50934567833', '112345678', '12345678', '359.58', 'active', 'admin'),
(522, 'CHARLOTIN', 'Carlowensky', 'Al-khami', '2023-01-18', 'M', '+50933832629', '123456789', '12345678', '211.60', 'active', 'user'),
(2537, 'JEFF', 'Dadensky', 'Dadenskey', '2023-01-26', 'M', '+50934567833', '112345678', '12345678', '0.00', 'active', 'user'),
(5325, 'ANTOINE', 'Valerie', 'Vava', '2023-01-10', 'F', '+50944069411', '102345678', '12345678', '160.00', 'active', 'user'),
(7045, 'VICTOR', 'Christan', 'chris22', '2023-01-18', 'M', '+50936988433', '123456789', '12345678', '0.00', 'active', 'admin'),
(8399, 'Leandre', 'Woodly', 'wood', '2023-01-11', 'F', '+50936988433', '123456789', '12345678', '300.00', 'active', 'user');

-- --------------------------------------------------------

--
-- Structure de la table `user_auth`
--

CREATE TABLE `user_auth` (
  `id` int(11) NOT NULL,
  `code_user` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `bets`
--
ALTER TABLE `bets`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `credits`
--
ALTER TABLE `credits`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `matchs`
--
ALTER TABLE `matchs`
  ADD UNIQUE KEY `id` (`id`);

--
-- Index pour la table `match_choisi`
--
ALTER TABLE `match_choisi`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `users`
--
ALTER TABLE `users`
  ADD UNIQUE KEY `id` (`id`);

--
-- Index pour la table `user_auth`
--
ALTER TABLE `user_auth`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `bets`
--
ALTER TABLE `bets`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `credits`
--
ALTER TABLE `credits`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT pour la table `match_choisi`
--
ALTER TABLE `match_choisi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `payments`
--
ALTER TABLE `payments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `user_auth`
--
ALTER TABLE `user_auth`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
