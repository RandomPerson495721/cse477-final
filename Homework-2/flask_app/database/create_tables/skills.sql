CREATE TABLE IF NOT EXISTS `skills` (
    `skill_id`       int(11)       NOT NULL AUTO_INCREMENT 	COMMENT 'The primary key, and unique identifier for each comment',
    `experience_id`  int(11)       DEFAULT NULL            	COMMENT 'The primary key, and unique identifier for each comment',
    `name`           varchar(100)  NOT NULL                	COMMENT 'The name of the skill',
    `skill_level`    int(11)       DEFAULT NULL            	COMMENT 'The level of the skill',
    PRIMARY KEY  (`skill_id`),
    FOREIGN KEY (experience_id) REFERENCES experiences(experience_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Skills I have";