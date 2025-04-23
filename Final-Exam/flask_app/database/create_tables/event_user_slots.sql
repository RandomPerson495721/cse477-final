CREATE TABLE IF NOT EXISTS `event_user_slots` (
    `event_id`    int(11)       NOT NULL                COMMENT 'A foreign key that references events.event_id',
    `users_id`    int(11)       NOT NULL                COMMENT 'A foreign key that references users.user_id',
    `slot_date`   datetime      NOT NULL                COMMENT 'The date of the event',
    `start_time`  time          NOT NULL                COMMENT 'The start time of the event',
    `end_time`    time          NOT NULL                COMMENT 'The end time of the event',
    `status`      varchar(10)   NOT NULL                COMMENT 'The status of the event; options include: accepted, declined, and maybe',
    FOREIGN KEY (`event_id`) REFERENCES events(`event_id`),
    FOREIGN KEY (`users_id`) REFERENCES users(`user_id`),
    PRIMARY KEY (`event_id`, `users_id`, `slot_date`, `start_time`, `end_time`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Contains the users that are attending the event";