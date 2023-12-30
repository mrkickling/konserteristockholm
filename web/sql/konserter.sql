CREATE TABLE `konserter` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`title` TEXT,
	`venue` INT,
	`date` DATETIME,
	`description` TEXT,
	PRIMARY KEY (`id`)
);