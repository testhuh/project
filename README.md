# 🎵 멜론 디즈니 OST → 유튜브 저장 리스트 자동화 프로젝트

## 📌 프로젝트 개요

멜론 플레이리스트에서 디즈니 OST 곡들을 자동으로 수집하고, 유튜브에서 저장 가능한 버전을 찾아 최종 리스트를 생성하는 **자동화 프로젝트**입니다.

**핵심 기능**
- ✅ 멜론 플레이리스트 크롤링
- ✅ 곡 정보 자동 추출 (곡명, 가수, 앨범)
- ✅ 유튜브 검색 및 저장 가능성 확인
- ✅ 최종 리스트 생성 (CSV, MD, JSON)

---

## 📦 프로젝트 파일 구성

```
📁 disney_auto_playlist2/1여기에
├── 📄 README.md (이 파일)
├── 📄 melon_disney_ost_youtube_crawler_prompt.md
│   └─ 상세 작업 프롬프트 (마크다운)
├── 📄 설치및실행가이드.md
│   └─ 라이브러리 설치 및 실행 방법
├── 📄 melon_to_youtube_crawler.py
│   └─ 메인 실행 스크립트 (Python)
└── 📝 requirements.txt
    └─ 필수 라이브러리 목록

생성될 파일 (실행 후):
├── melon_disney_ost_complete_list.csv
├── youtube_saveable_list.csv
├── melon_disney_ost_list.json
└── execution_log.txt
```

---

## 🚀 빠른 시작

### 1️⃣ 준비 (2분)

```bash
# 라이브러리 설치
pip install requests beautifulsoup4 pandas yt-dlp
```

### 2️⃣ 설정 (1분)

`melon_to_youtube_crawler.py` 파일의 마지막 부분 수정:

```python
MELON_PLAYLIST_URL = "https://www.melon.com/playlist/detail.htm?plstId=YOUR_ID"
```

### 3️⃣ 실행 (30~60분)

```bash
python melon_to_youtube_crawler.py
```

### 4️⃣ 결과 확인

생성된 CSV 파일로 최종 리스트 확인

---

## 📚 파일별 역할

| 파일명 | 타입 | 설명 |
|--------|------|------|
| `README.md` | 📄 텍스트 | 프로젝트 전체 개요 (이 파일) |
| `melon_disney_ost_youtube_crawler_prompt.md` | 📄 마크다운 | 상세 작업 프롬프트 및 스크립트 코드 |
| `설치및실행가이드.md` | 📄 마크다운 | 단계별 설치 및 실행 방법 |
| `melon_to_youtube_crawler.py` | 🐍 Python | 메인 자동화 스크립트 |

---

## 🎯 작업 흐름

```
멜론 플레이리스트 선정
    ↓
[단계 1] 멜론 크롤링
    ├─ 곡명 추출
    ├─ 가수명 추출
    ├─ 앨범명 추출
    └─ 멜론 링크 추출
    ↓
[단계 2] 유튜브 검색
    ├─ 검색 쿼리 생성
    ├─ 상위 5개 검색 결과 분석
    ├─ 필터링 (공식채널, 조회수, 길이)
    └─ 다운로드 가능 여부 확인
    ↓
[단계 3] 결과 저장
    ├─ CSV 파일 생성
    ├─ JSON 파일 생성
    └─ 실행 로그 기록
    ↓
최종 리스트 (youtube_saveable_list.csv)
```

---

## 📊 예상 결과

### 수집 통계 (예시)

```
총 멜론 플레이리스트: 45곡
├─ ✅ 저장 가능 (유튜브): 38곡 (84%)
├─ ❌ 저장 불가능: 5곡 (11%)
└─ △ 수동 확인 필요: 2곡 (5%)
```

### 최종 리스트 형식 (CSV)

| 순번 | 곡명 | 가수 | 앨범 | 유튜브링크 | 조회수 | 저장가능 |
|------|------|------|------|----------|--------|--------|
| 1 | Let It Go | Idina Menzel | Frozen OST | https://youtu.be/... | 50M | O |
| 2 | Into the Unknown | Idina Menzel | Frozen II OST | https://youtu.be/... | 30M | O |
| ... | ... | ... | ... | ... | ... | ... |

---

## 🛠️ 기술 스택

| 항목 | 도구 | 버전 |
|------|------|------|
| **언어** | Python | 3.8+ |
| **웹 크롤링** | BeautifulSoup4 | 4.12+ |
| **데이터 처리** | Pandas | 2.0+ |
| **HTTP 요청** | Requests | 2.31+ |
| **유튜브 처리** | yt-dlp | 2023.11+ |

---

## 💾 데이터 저장 형식

### CSV (melon_disney_ost_complete_list.csv)

```
순번,곡명,가수,앨범,멜론링크,유튜브링크,업로더,조회수,길이,저장가능,선정사유
1,Let It Go,Idina Menzel,Frozen OST,https://...melon.com...,https://...youtube.com...,Disney Music,50000000,227,O,"공식:True, 조회수:True, 길이:True"
```

### JSON (melon_disney_ost_list.json)

```json
[
  {
    "순번": 1,
    "곡명": "Let It Go",
    "가수": "Idina Menzel",
    "앨범": "Frozen OST",
    "멜론링크": "https://www.melon.com/song/detail/...",
    "유튜브링크": "https://www.youtube.com/watch?v=...",
    "업로더": "Disney Music",
    "조회수": 50000000,
    "길이": 227,
    "저장가능": "O",
    "선정사유": "공식:True, 조회수:True, 길이:True"
  }
]
```

---

## ⏱️ 소요 시간

| 단계 | 시간 |
|------|------|
| 라이브러리 설치 | 2분 |
| 설정 (URL 입력) | 1분 |
| 멜론 크롤링 (45곡 기준) | 2~3분 |
| 유튜브 검색 (45곡 기준) | 20~30분 |
| 결과 저장 | 1분 |
| **총 소요 시간** | **25~40분** |

※ 곡 개수, 인터넷 속도, 서버 상태에 따라 변동

---
⚠️ **서버 부하 최소화**
- 딜레이 설정으로 요청 간격 조절
- 과도한 크롤링 금지

⚠️ **VPN 사용**
- 지역 제한으로 실패 시 VPN 고려

---

## 🐛 문제 해결

### 가장 일반적인 오류

| 오류 | 원인 | 해결책 |
|------|------|--------|
| ModuleNotFoundError | 라이브러리 미설치 | `pip install yt-dlp` |
| ConnectionError | 멜론/유튜브 연결 실패 | 인터넷 확인, VPN 고려 |
| HTTP 429 | 요청 속도 제한 | `time.sleep()` 증가 |
| UnicodeEncodeError | 한글 인코딩 오류 | 첫 줄에 `# -*- coding: utf-8 -*-` 추가 |

더 자세한 해결법은 `설치및실행가이드.md` 참고

---

## 📖 문서 읽기 순서

추천 읽기 순서:

1. **README.md** (이 파일) - 전체 개요
2. **설치및실행가이드.md** - 설치 및 실행
3. **melon_disney_ost_youtube_crawler_prompt.md** - 상세 내용 및 코드
4. **melon_to_youtube_crawler.py** - 스크립트 검토

---

## 📞 추가 정보

### 참고 자료
- [멜론 공식 사이트](https://www.melon.com)
- [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)
- [BeautifulSoup 문서](https://www.crummy.com/software/BeautifulSoup/)
- [Pandas 문서](https://pandas.pydata.org/docs/)

### 유사 프로젝트
- Spotify → YouTube 플레이리스트 변환
- 음악 스트리밍 서비스 통합
- 음악 메타데이터 크롤링

---

## 📝 프로젝트 이력

| 날짜 | 내용 |
|------|------|
| 2026-06-14 | 프로젝트 초기 생성 및 문서화 |
| | - 멜론 크롤링 스크립트 작성 |
| | - 유튜브 검색 기능 추가 |
| | - 마크다운 프롬프트 정리 |
| | - 설치 가이드 작성 |

---

## ✨ 특징

✅ **자동화** - 수동 작업 최소화  
✅ **효율적** - 배치 처리로 빠른 실행  
✅ **안정적** - 오류 처리 및 재시도 로직  
✅ **명확한 결과** - CSV, JSON, 로그 파일 생성  
✅ **확장 가능** - 다른 서비스로 쉽게 확장 가능  

---

## 🎓 학습 포인트

이 프로젝트를 통해 배울 수 있는 것:

- 웹 크롤링 (BeautifulSoup)
- API 활용 (yt-dlp)
- 데이터 처리 (Pandas)
- 자동화 스크립트 작성
- 오류 처리 및 로깅
- 파일 입출력 (CSV, JSON)

---
**작성일**: 2026-06-14  
