USE MiniProject_lms;
CREATE TABLE members (
    id              INT AUTO_INCREMENT PRIMARY KEY,

    -- 로그인
    uid             VARCHAR(50) NOT NULL UNIQUE,     -- 로그인 아이디
    password        VARCHAR(255) NOT NULL,           -- 비밀번호(해시 예정)

    -- 기본 정보
    name            VARCHAR(50) NOT NULL,
    email           VARCHAR(100) NULL,

    -- 권한
    role            ENUM('user','manager','admin') 
                    NOT NULL DEFAULT 'user',

    -- 상태
    active          TINYINT(1) NOT NULL DEFAULT 1,   -- soft delete

    -- 프로필
    profile_img     VARCHAR(255) NULL,

    -- 감사/로그용
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                    ON UPDATE CURRENT_TIMESTAMP,
    last_login_at   DATETIME NULL
);

/*더미데이터 생성*/
INSERT INTO members
(uid, password, name, email, role, active, profile_img, last_login_at)
VALUES
-- 일반 사용자
('user01', '1234', '김학생', 'user01@test.com', 'user', 1, NULL, NULL),
('user02', '1234', '이학생', 'user02@test.com', 'user', 1, NULL, NULL),
('user03', '1234', '박학생', 'user03@test.com', 'user', 1, NULL, NULL),

-- 매니저
('manager01', '1234', '최매니저', 'mgr@test.com', 'manager', 1, NULL, NULL),

-- 관리자
('admin', 'admin123', '관리자', 'admin@test.com', 'admin', 1, NULL, NOW()),
('kdh', '1234', '관리자', 'admin@test.com', 'admin', 1, NULL, NOW()),

-- 탈퇴(비활성) 테스트용
('olduser', '1234', '탈퇴회원', 'old@test.com', 'user', 0, NULL, NULL),

-- 프로필 이미지 있는 사용자 테스트
('photo01', '1234', '이미지회원', 'photo@test.com', 'user', 1, 'sample.png', NOW());

CREATE TABLE boards (
  id INT AUTO_INCREMENT PRIMARY KEY,
  member_id INT NOT NULL,
  title VARCHAR(200) NOT NULL,
  content TEXT NOT NULL,

  views INT NOT NULL DEFAULT 0,
  likes INT NOT NULL DEFAULT 0,

  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  CONSTRAINT fk_boards_member
    FOREIGN KEY (member_id) REFERENCES members(id)
);

CREATE TABLE lectures (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    professor_id INT NOT NULL,
    visibility ENUM('PUBLIC', 'PRIVATE') DEFAULT 'PUBLIC',
    active TINYINT DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_lecture_prof FOREIGN KEY (professor_id)
        REFERENCES members (id)
);

SHOW CREATE TABLE lectures;
CREATE TABLE enrollments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  member_id INT NOT NULL,
  lecture_id INT NOT NULL,

  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (member_id) REFERENCES members(id),
  FOREIGN KEY (lecture_id) REFERENCES lectures(id),

  UNIQUE KEY uq_enroll (member_id, lecture_id)
);
CREATE TABLE scores (
  id INT AUTO_INCREMENT PRIMARY KEY,
  member_id INT NOT NULL,
  lecture_id INT NOT NULL,

  exam_name VARCHAR(100),
  score DECIMAL(5,2) NOT NULL,

  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (member_id) REFERENCES members(id),
  FOREIGN KEY (lecture_id) REFERENCES lectures(id)
);
/*더미 데이터*/
INSERT INTO members
(uid, password, name, email, role, active, profile_img, created_at, updated_at)
VALUES
('user10','1234','학생10','user10@test.com','user',1,NULL,NOW(),NOW()),
('user11','1234','학생11','user11@test.com','user',1,NULL,NOW(),NOW()),
('user12','1234','학생12','user12@test.com','user',1,NULL,NOW(),NOW()),
('user13','1234','학생13','user13@test.com','user',1,NULL,NOW(),NOW()),
('user14','1234','학생14','user14@test.com','user',1,NULL,NOW(),NOW()),

('black01','1234','차단학생1','black01@test.com','user',0,NULL,NOW(),NOW()),
('black02','1234','차단학생2','black02@test.com','user',0,NULL,NOW(),NOW()),

('prof01','1234','교수김','prof01@test.com','professor',1,NULL,NOW(),NOW()),
('prof02','1234','교수이','prof02@test.com','professor',1,NULL,NOW(),NOW());

INSERT INTO members
(uid,password,name,email,role,active,created_at,updated_at)
VALUES
('new01','1234','신규1','new01@test.com','user',1,NOW() - INTERVAL 5 DAY,NOW()),
('new02','1234','신규2','new02@test.com','user',1,NOW() - INTERVAL 2 DAY,NOW()),
('new03','1234','신규3','new03@test.com','user',1,NOW() - INTERVAL 1 DAY,NOW());

INSERT INTO members
(uid,password,name,email,role,active,created_at,updated_at)
VALUES
('mgr10','1234','김교수','mgr10@test.com','manager',1,NOW(),NOW()),
('mgr11','1234','이교수','mgr11@test.com','manager',1,NOW(),NOW());
SELECT id, uid FROM members WHERE role='manager';

INSERT INTO lectures
(title, description, professor_id, visibility, active)
VALUES
('파이썬 기초','입문 강의',4,'PUBLIC',1),
('Flask 실전','웹앱 제작',4,'PUBLIC',1),
('DB 튜닝','고급 과정',22,'PRIVATE',1);


ALTER TABLE boards
ADD is_notice TINYINT DEFAULT 0,
ADD active TINYINT DEFAULT 1,
ADD is_private TINYINT DEFAULT 0,
ADD is_inquiry TINYINT DEFAULT 0;

ALTER TABLE boards
ADD video_url VARCHAR(300),
ADD external_link VARCHAR(300);

ALTER TABLE enrollments
ADD status ENUM('ENROLLED','CANCELED') DEFAULT 'ENROLLED';

CREATE TABLE board_files (
  id INT AUTO_INCREMENT PRIMARY KEY,
  board_id INT NOT NULL,
  file_name VARCHAR(255),
  file_path VARCHAR(255),
  file_type ENUM('IMAGE','FILE'),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (board_id) REFERENCES boards(id)
);

CREATE TABLE banned_words (
  id INT AUTO_INCREMENT PRIMARY KEY,
  word VARCHAR(100) UNIQUE
);

CREATE TABLE inquiry_meta (
  board_id INT PRIMARY KEY,
  answered TINYINT DEFAULT 0,
  answered_by INT NULL,
  answered_at DATETIME NULL,

  FOREIGN KEY (board_id) REFERENCES boards(id),
  FOREIGN KEY (answered_by) REFERENCES members(id)
);

CREATE TABLE comments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  board_id INT,
  member_id INT,
  parent_id INT NULL,
  content TEXT,
  active TINYINT DEFAULT 1,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (board_id) REFERENCES boards(id),
  FOREIGN KEY (member_id) REFERENCES members(id),
  FOREIGN KEY (parent_id) REFERENCES comments(id)
);

SHOW TABLES;



