CREATE TABLE `konserter` (
	`title` VARCHAR(255),
	`venue` VARCHAR(255),
	`date` DATETIME,
	`url` VARCHAR(255),
	`description` TEXT,
	`show` BOOLEAN DEFAULT 1,
	`first_seen`DATETIME DEFAULT CURRENT_TIMESTAMP,
	`last_seen` DATETIME DEFAULT CURRENT_TIMESTAMP,
	`static` BOOLEAN DEFAULT 0,
	PRIMARY KEY (`title`, `venue`, `date`, `url`)
);