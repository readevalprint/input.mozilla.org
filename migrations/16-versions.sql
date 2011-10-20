CREATE TABLE `version_count` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `product` smallint UNSIGNED NOT NULL,
    `version` varchar(30) NOT NULL,
    `version_int` bigint NOT NULL,
    `num_opinions` integer NOT NULL,
    `active` bool NOT NULL,
    UNIQUE (`product`, `version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE INDEX `version_count_7e1f2157` ON `version_count` (`product`);
CREATE INDEX `version_count_659105e4` ON `version_count` (`version`);
CREATE INDEX `version_count_6fd24c02` ON `version_count` (`version_int`);
CREATE INDEX `version_count_34d728db` ON `version_count` (`active`);
