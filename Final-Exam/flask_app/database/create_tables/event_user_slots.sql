CREATE TABLE IF NOT EXISTS `event_user_slots`
(
    `event_id` int(11)     NOT NULL COMMENT 'A foreign key that references events.event_id',
    `user_id`  int(11)     NOT NULL COMMENT 'A foreign key that references users.user_id',
    `e_column` int(11)     NOT NULL COMMENT 'The column of the slot in the selector',
    `e_row`    int(11)     NOT NULL COMMENT 'The row of the slot in the selector',
    `status`   varchar(10) NOT NULL COMMENT 'The status of the event; options include: accepted, declined, and maybe',
    FOREIGN KEY (`event_id`) REFERENCES events (`event_id`),
    FOREIGN KEY (`user_id`) REFERENCES users (`user_id`),
    PRIMARY KEY (`event_id`, `user_id`, `e_column`, `e_row`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 1
  DEFAULT CHARSET = utf8mb4 COMMENT ="Contains the users that are attending the event";