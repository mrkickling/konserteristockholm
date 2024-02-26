CREATE TABLE `venues` (
	`name` VARCHAR(255) NOT NULL,
	`address` TEXT,
	`url` TEXT,
	`description` TEXT,
    `up` BOOLEAN DEFAULT 0,
	`latest_sync` DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (`name`)
);