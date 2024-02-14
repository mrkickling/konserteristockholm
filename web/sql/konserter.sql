CREATE TABLE `konserter` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`title` TEXT,
	`venue` TEXT,
	`date` DATETIME,
	`url` TEXT,
	`description` TEXT,
	`added` DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`)
);