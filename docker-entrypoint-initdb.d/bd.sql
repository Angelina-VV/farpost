-- -----------------------------------------------------
-- Table `mydb`.`users`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `mydb`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `is_logged_in` TINYINT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------
-- Table `mydb`.`topics`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `mydb`.`topics` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `user_id_idx` (`user_id`),
  CONSTRAINT `user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `mydb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------
-- Table `mydb`.`messages`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `mydb`.`messages` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `m_user_id` INT NOT NULL,
  `m_topic_id` INT NOT NULL,
  `content` LONGTEXT NOT NULL,
  `created_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `user_id_idx` (`m_user_id`),
  INDEX `topic_id_idx` (`m_topic_id`),
  CONSTRAINT `m_user_id`
    FOREIGN KEY (`m_user_id`)
    REFERENCES `mydb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `m_topic_id`
    FOREIGN KEY (`m_topic_id`)
    REFERENCES `mydb`.`topics` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------
-- Table `mydb`.`actions`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `mydb`.`actions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `a_user_id` INT NOT NULL,
  `action_type` VARCHAR(255) NOT NULL,
  `response` VARCHAR(50) NOT NULL,
  `action_time` DATETIME NOT NULL,
  `topic_id` INT NULL,
  `message_id` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `user_id_idx` (`a_user_id`),
  INDEX `message_id_idx` (`message_id`),
  INDEX `topic_id_idx` (`topic_id`),
  CONSTRAINT `a_user_id`
    FOREIGN KEY (`a_user_id`)
    REFERENCES `mydb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `message_id`
    FOREIGN KEY (`message_id`)
    REFERENCES `mydb`.`messages` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `topic_id`
    FOREIGN KEY (`topic_id`)
    REFERENCES `mydb`.`topics` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
