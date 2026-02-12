CREATE DATABASE MiniProject_lms DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
SHOW DATABASES; /*DB 리스트 조회*/
USE MiniProject_lms; /*mbc DB 사용*/

DROP USER 'kdh'@'%'; /*이미 있거나 잘못 만들 때 삭제*/
CREATE USER 'kdh'@'192.168.0.%' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON MiniProject_lms.* TO 'kdh'@'192.168.0.%';
FLUSH PRIVILEGES /*즉시권한적용*/
