CREATE TABLE IF NOT EXISTS `events` (
    `event_id`       int(11)       NOT NULL AUTO_INCREMENT 	COMMENT 'The primary key, and unique identifier for each event',
    `owner_id`       int(11)       NOT NULL             	COMMENT 'The user id of the owner of the event',
    `name`           varchar(100)  NOT NULL                	COMMENT 'The name of the event',
    `start_date`     datetime      NOT NULL                	COMMENT 'The start date of the event',
    `end_date`       datetime      NOT NULL                	COMMENT 'The end date of the event',
    `start_time`     time          NOT NULL                	COMMENT 'The start time of the event',
    `end_time`       time          NOT NULL                	COMMENT 'The end time of the event',
    `invitee_emails` TEXT          DEFAULT NULL             COMMENT 'The emails of the invitees',
    PRIMARY KEY  (`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Events table that contains the events created by users";