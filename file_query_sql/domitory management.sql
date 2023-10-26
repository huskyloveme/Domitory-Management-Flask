SET GLOBAL sql_mode = '';
CREATE TABLE `students` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `room_id` integer,
  `msv` varchar(255) UNIQUE NOT NULL,
  `name` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `gender` ENUM ('MALE', 'FEMALE', 'OTHER') NOT NULL,
  `birthday` timestamp,
  `day_in` timestamp,
  `day_out` timestamp,
  `status` ENUM ('ACTIVE', 'INACTIVE'),
  `created_at` timestamp DEFAULT (now()),
  `updated_at` timestamp NOT NULL DEFAULT (now()) COMMENT 'TODO: Add ON UPDATE ON UPDATE CURRENT_TIMESTAMP'
);

CREATE TABLE `vistors` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `student_id` integer,
  `cccd` varchar(255) UNIQUE NOT NULL,
  `name` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `gender` ENUM ('MALE', 'FEMALE', 'OTHER') NOT NULL,
  `time_in` timestamp NOT NULL,
  `time_out` timestamp,
  `created_at` timestamp DEFAULT (now()),
  `updated_at` timestamp NOT NULL DEFAULT (now()) COMMENT 'TODO: Add ON UPDATE ON UPDATE CURRENT_TIMESTAMP'
);

CREATE TABLE `buildings` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `created_at` timestamp DEFAULT (now()),
  `updated_at` timestamp NOT NULL DEFAULT (now()) COMMENT 'TODO: Add ON UPDATE ON UPDATE CURRENT_TIMESTAMP'
);

CREATE TABLE `rooms` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `building_id` integer,
  `name` varchar(255) NOT NULL,
  `accommodate` varchar(255),
  `type` ENUM ('PRIVATE', 'PUBLIC') NOT NULL,
  `capacity` integer NOT NULL,
  `price` double NOT NULL,
  `status` ENUM ('AVAILABLE', 'UNAVAILABLE'),
  `created_at` timestamp DEFAULT (now()),
  `updated_at` timestamp NOT NULL DEFAULT (now()) COMMENT 'TODO: Add ON UPDATE ON UPDATE CURRENT_TIMESTAMP'
);

CREATE TABLE `services` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `price` double NOT NULL,
  `unit` varchar(255) NOT NULL,
  `description` varchar(255),
  `created_at` timestamp DEFAULT (now()),
  `updated_at` timestamp NOT NULL DEFAULT (now()) COMMENT 'TODO: Add ON UPDATE ON UPDATE CURRENT_TIMESTAMP'
);

CREATE TABLE `student_service` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `student_id` integer,
  `service_id` integer,
  `time_use` integer NOT NULL,
  `time_end` timestamp,
  `created_at` timestamp DEFAULT (now()),
  `updated_at` timestamp NOT NULL DEFAULT (now()) COMMENT 'TODO: Add ON UPDATE ON UPDATE CURRENT_TIMESTAMP'
);

CREATE TABLE `motorbikes` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `student_id` integer,
  `name` varchar(500) NOT NULL,
  `license_plate` varchar(255) UNIQUE NOT NULL,
  `time_registration` timestamp NOT NULL,
  `status` ENUM ('REGISTER', 'UNREGISTER'),
  `created_at` timestamp DEFAULT (now()),
  `updated_at` timestamp NOT NULL DEFAULT (now()) COMMENT 'TODO: Add ON UPDATE ON UPDATE CURRENT_TIMESTAMP'
);

CREATE TABLE `parking_histories` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `student_id` integer,
  `motorbike_id` integer,
  `time_in` timestamp NOT NULL,
  `time_out` timestamp,
  `status` ENUM ('FREE', 'PAID') NOT NULL,
  `price` double,
  `created_at` timestamp DEFAULT (now()),
  `updated_at` timestamp NOT NULL DEFAULT (now()) COMMENT 'TODO: Add ON UPDATE ON UPDATE CURRENT_TIMESTAMP'
);

ALTER TABLE `rooms` ADD FOREIGN KEY (`building_id`) REFERENCES `buildings` (`id`);

ALTER TABLE `vistors` ADD FOREIGN KEY (`student_id`) REFERENCES `students` (`id`);

ALTER TABLE `students` ADD FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`);

ALTER TABLE `student_service` ADD FOREIGN KEY (`student_id`) REFERENCES `students` (`id`);

ALTER TABLE `student_service` ADD FOREIGN KEY (`service_id`) REFERENCES `services` (`id`);

ALTER TABLE `parking_histories` ADD FOREIGN KEY (`motorbike_id`) REFERENCES `motorbikes` (`id`);

ALTER TABLE `parking_histories` ADD FOREIGN KEY (`student_id`) REFERENCES `students` (`id`);

ALTER TABLE `motorbikes` ADD FOREIGN KEY (`student_id`) REFERENCES `students` (`id`);
