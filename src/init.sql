CREATE DATABASE IF NOT EXISTS `data` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `data`; 

CREATE TABLE IF NOT EXISTS `accounts` ( 
`id` int(11) NOT NULL AUTO_INCREMENT, 
`username` varchar(50) NOT NULL, 
`password` varchar(255) NOT NULL, 
`email` varchar(100) NOT NULL,
`isVerified` boolean NOT NULL DEFAULT False,
`isPassChange` boolean NOT NULL DEFAULT False,
`isEmailChange` boolean NOT NULL DEFAULT False,
`VerifyCode` varchar(4) DEFAULT null,
`CodeExpire` timestamp NOT NULL DEFAULT current_timestamp(),
PRIMARY KEY (`id`) 
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `credentials` ( 
`id` int(11) NOT NULL AUTO_INCREMENT, 
`username` varchar(50) NOT NULL, 
`credentials` varchar(70) NOT NULL, 
`expire` 	timestamp NOT NULL DEFAULT current_timestamp(),
PRIMARY KEY (`id`),
FOREIGN KEY (`id`)
      REFERENCES `accounts` (`id`)
      ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `storage` ( 
`id` int(11) NOT NULL AUTO_INCREMENT,
`username` varchar(50) NOT NULL,
`star_character` json DEFAULT NULL,
`items` json DEFAULT NULL,
PRIMARY KEY (`id`),
FOREIGN KEY (`id`)
      REFERENCES `accounts` (`id`)
      ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;