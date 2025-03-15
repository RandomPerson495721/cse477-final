CREATE TABLE IF NOT EXISTS `skills` (
    `skill_id`       int(11)       NOT NULL AUTO_INCREMENT 	COMMENT 'The primary key, and unique identifier for each comment',
    `experience_id`  int(11)       DEFAULT NULL            	COMMENT 'The primary key, and unique identifier for each comment',
    `name`           varchar(100)  NOT NULL                	COMMENT 'The commentators name',
    `skill_level`    int(11)       DEFAULT NULL            	COMMENT 'The text of the comment',
    PRIMARY KEY  (`skill_id`),
    FOREIGN KEY (experience_id) REFERENCES experiences(experience_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="skills I have";