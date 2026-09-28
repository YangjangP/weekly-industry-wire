# Weekly Industry Wire

패션 / 뷰티 / F&B 업계 뉴스와 5개 광고 매체(Meta, 네이버 검색광고, 네이버 GFA, 카카오모먼트, Google) 업데이트를 매주 모아 이메일·Slack으로 보내고, 같은 내용을 웹 아카이브 페이지로도 상시 열람할 수 있게 하는 프로젝트.

## 핵심 요구사항

- 업계는 패션 / 뷰티 / F&B 중 사용자가 원하는 것을 선택 (로그인 없는 구독 폼)
- 매체 업데이트(Meta / 네이버 검색광고 / 네이버 GFA / 카카오모먼트 / Google)는 어떤 업계를 선택해도 동일하게 포함
- 구독하지 않아도 아카이브 페이지에서 항상 확인 가능

## 아키텍처

```
수집(RSS/스크래핑/Playwright) → AI 요약(Claude) → 정적 사이트 생성(docs/) → GitHub Pages 배포
                                                  ↘ 구독자별 이메일/Slack 발송
```

- **호스팅**: GitHub Pages (`docs/` 디렉터리, 저장소는 Public — GitHub Free는 Private 저장소에서 Pages를 지원하지 않음)
- **스케줄링**: GitHub Actions cron (매주 1회, 파이프라인 완성 후 연결 예정)
- **구독자 관리**: Google Form(이메일 + 업계 체크박스 + 선택적 Slack Webhook URL) → Google Sheet
- **이메일 발송**: MVP는 Gmail/Apps Script, 발송량이 늘면 Resend + 도메인 인증으로 전환 검토

## 소스 목록 및 수집 방식

| 카테고리 | 소스 | 방식 | 상태 |
|---|---|---|---|
| F&B | 식품음료신문 | RSS (`/rss/allArticle.xml`) | ✅ 구현 완료 (`scripts/collectors/thinkfood.py`) |
| F&B | 푸드투데이 | 목록 페이지 스크래핑 | 예정 |
| 패션 | 어패럴뉴스 / 패션비즈 / 패션엔 | 목록 페이지 스크래핑 | 예정 |
| 뷰티 | 코스인 / 뷰티누리 / 코스모닝 | 목록 페이지 스크래핑 (코스모닝은 robots.txt 재확인 필요) | 예정 |
| 매체 | Meta for Business | 목록 페이지 스크래핑 | 예정 |
| 매체 | Google Ads 업데이트 | 목록 페이지 스크래핑 (정적 HTML) | 예정 |
| 매체 | 네이버 검색광고 | Playwright(헤드리스 브라우저) — 단순 fetch 접근 차단됨 | 예정 |
| 매체 | 네이버 GFA | Playwright — 단순 fetch 접근 차단됨 | 예정 |
| 매체 | 카카오모먼트 | Playwright — JS 렌더링(SPA) | 예정 |

"외식경영" 매체는 특정 소스를 찾지 못해 F&B 목록에서 제외했습니다 (2026-09-28 확인).

## 아카이브 페이지 디자인

`docs/` 사이트는 승인된 목업을 기반으로 만듭니다. 핵심 구조:
- 상단 탭(패션/뷰티/F&B) — 선택한 탭의 피드만 전환
- 오른쪽 "매체 업데이트" 레일 — 어떤 탭을 선택해도 항상 동일하게 노출 (업계 무관 공통 요구사항)
- 주차별 아카이브 (`docs/archive/<연도>-W<주차>/`)

## 로컬 실행

```bash
pip install -r requirements.txt
python scripts/run_collectors.py
```

수집 결과는 `data/raw/<연도>-W<주차>/<source_id>.json`에 저장됩니다 (git에는 커밋하지 않음).

## 진행 상황

- [x] 아카이브 페이지 목업 승인
- [x] 소스 목록 확정
- [x] 저장소 스캐폴딩 + 식품음료신문 RSS 수집기
- [ ] 나머지 스크래핑 수집기 (패션/뷰티/F&B, Meta, Google Ads)
- [ ] Playwright 기반 수집기 (네이버 검색광고/GFA, 카카오모먼트)
- [ ] AI 요약 단계 (Claude API)
- [ ] 정적 사이트 생성기 (목업 → 실제 데이터)
- [ ] 구독자 폼(Google Form) + Sheet 연동
- [ ] 이메일·Slack 발송
- [ ] 전체 주간 파이프라인 cron 연결
