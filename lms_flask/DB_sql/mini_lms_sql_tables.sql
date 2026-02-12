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


