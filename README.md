# MyMiniProjects_lms_flask (In Progress)

Python + Flask 기반 LMS 기능을 웹 구조로 재구성하는 미니 프로젝트입니다.  
기존 CLI 구조를 Flask 웹 아키텍처로 확장하며  
**Layered Architecture + Blueprint 구조 + DB 모듈화**를 목표로 진행 중입니다.

---

## Project Goal

- LMS 기능을 Flask 웹 서비스로 재구성
- Service Layer 중심 구조 유지
- Blueprint 기반 라우트 분리
- DB 접근 모듈화
- UI + Backend 통합 구조 실습

---

## Current Structure

```
lms_flask/
├─ DB_sql/
│ ├─ ddl/
│ └─ dml/
│
├─ lms/
│ ├─ domain/
│ ├─ service/
│ ├─ repository/
│ ├─ routes/
│ ├─ templates/
│ └─ static/
```

---

## Implemented (현재 구현)

- 회원 기능
  - 회원가입
  - 로그인
  - 세션 인증
  - 마이페이지
  - 회원정보 수정

- 게시판 기능 (기본)
  - 게시글 목록
  - 게시글 등록
  - 게시글 상세

- 파일 업로드 게시판
  - 첨부파일 저장
  - 다운로드 처리

- DB 구조
  - members
  - boards
  - files
  - scores (연동 예정)

---

## Architecture Style

이 프로젝트는 다음 계층 분리를 기준으로 설계합니다.
```
Route (Blueprint)
↓
Service Layer
↓
Repository / DB Access
↓
MySQL
```

원칙:

- 비즈니스 로직은 Service에 위치
- SQL은 Repository 계층에서만 처리
- Route는 요청/응답만 담당
- Domain 모델 기반 처리

---

## Tech Stack

- Python
- Flask
- MySQL
- Bootstrap 5
- Jinja2 Template
- Session 인증

---

## Next Steps

- [ ] 관리자 기능 분리
- [ ] 권한(Role) 기반 메뉴 제어
- [ ] 게시판 고급 기능
- [ ] 검색 / 필터 / 페이징
- [ ] 성적 관리 모듈 연동
- [ ] API 구조 분리
- [ ] UI 템플릿 통합

---

## Design Notes

- CLI LMS 구조를 Web으로 확장하는 과정 기록
- DB → Service → Route 흐름 유지
- 구조 재사용 가능성 검증 목적

