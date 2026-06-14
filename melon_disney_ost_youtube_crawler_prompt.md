# 멜론 디즈니 OST 플레이리스트 → 유튜브 저장 리스트 구축

## 📋 작업 개요

| 항목 | 설명 |
|------|------|
| **목표** | 멜론 플레이리스트에서 디즈니 OST를 수집하고, 유튜브에서 저장 가능한 버전을 찾아 최종 리스트 생성 |
| **소요 시간** | 약 30~60분 (곡 개수에 따라 변동) |
| **최종 산출물** | CSV, JSON, 실행 로그 |

---

## 🎯 상세 실행 단계

### 1️⃣ **멜론 플레이리스트 선정 및 링크 수집**

#### 작업 내용
```
1. 멜론(melon.com) 접속
   └─ URL: https://www.melon.com

2. 플레이리스트 검색
   └─ 검색어: "디즈니 OST"
   └─ 필터: 팔로워/조회수 많은 순

3. 플레이리스트 선택
   └─ 기준: 팔로워 1만 이상, 곡 30곡 이상
   └─ 예시 플레이리스트명: "디즈니 OST 명곡모음", "Disney Animation Classics"

4. 링크 복사
   └─ 형식: https://www.melon.com/playlist/detail.htm?plstId=XXXXXXX
   └─ 메모: 뒤의 plstId 숫자 기억
```

#### 예시
```
멜론 플레이리스트 URL:
https://www.melon.com/playlist/detail.htm?plstId=123456789
```

---

### 2️⃣ **멜론 플레이리스트 크롤링**

#### 수집할 정보
| 항목 | 설명 | 예시 |
|------|------|------|
| **곡명** | 정확한 곡 제목 | Let It Go |
| **가수/아티스트** | 곡의 가수명 | Idina Menzel |
| **앨범명** | 원작 앨범명 | Frozen OST |
| **멜론링크** | 멜론 내 곡 상세 페이지 | https://www.melon.com/song/detail/XXXXX |

#### 기대 출력
```
[1] Let It Go - Idina Menzel ✓
[2] Into the Unknown - Idina Menzel ✓
[3] For the First Time in Forever - Kristen Bell, Idina Menzel ✓
...
✅ 총 45개 곡 수집 완료
```

---

### 3️⃣ **유튜브 검색 및 저장 가능성 확인**

#### 검색 및 필터링 기준

**검색 쿼리 형식**
```
[곡명] [가수명] OST
→ 예: "Let It Go Idina Menzel OST"
```

**선정 기준 (우선순위)**

| 조건 | 필수/권장 | 설명 |
|------|---------|------|
| **공식 채널** | 필수 | Official, Disney Music, Original 등 포함된 채널 |
| **조회수** | 필수 | 100,000회 이상 |
| **길이** | 권장 | 3~8분 (대부분의 OST 표준) |
| **업로드 연도** | 권장 | 2015년 이후 (품질 관계) |
| **다운로드 가능** | 필수 | yt-dlp 라이브러리로 실제 저장 가능 확인 |

#### 기대 출력 예시
```
[1/45] Let It Go - Idina Menzel → O
[2/45] Into the Unknown - Idina Menzel → O
[3/45] For the First Time in Forever - Kristen Bell, Idina Menzel → X
...
```

---

### 4️⃣ **데이터 검증 및 최종 정리**

#### 검증 항목
- ✅ 총 수집 곡 개수
- ✅ 저장 가능한 곡 개수
- ✅ 저장 불가능한 곡 리스트
- ✅ 수동 확인 필요 곡 리스트

#### 통계 예시
```
✅ 저장 가능: 38개
❌ 저장 불가능: 5개
△ 수동 확인: 2개
```

---

## 🛠️ 오류 처리 및 대응

| 오류 상황 | 대응 방법 |
|----------|---------|
| **크롤링 실패** | 해당 곡 스킵, 로그에 기록 |
| **유튜브 검색 실패** | 해당 곡은 NOT_FOUND로 표시, 수동 입력 대기 |
| **속도 제한 (429 오류)** | 요청 간격을 2초 → 3초로 증가 |
| **멜론 차단** | User-Agent 변경 또는 VPN 사용 검토 |
| **메모리 부족** | 배치 처리 (예: 10곡씩 나누어 처리) |

---

## 📦 최종 산출물

### 생성되는 파일들

```
📁 작업 폴더
├── melon_disney_ost_complete_list.csv
│   └─ 모든 곡 정보 (멜론 + 유튜브)
│
├── youtube_saveable_list.csv
│   └─ 저장 가능한 곡만 필터링
│
├── melon_disney_ost_list.json
│   └─ JSON 형식 (데이터 구조화)
│
└── execution_log.txt
    └─ 실행 시간, 통계, 오류 로그
```

### CSV 파일 구조

**melon_disney_ost_complete_list.csv**
```
순번,곡명,가수,앨범,멜론링크,유튜브링크,유튜브제목,업로더,조회수,길이,저장가능,선정사유
1,Let It Go,Idina Menzel,Frozen OST,https://...melon.com/song/...,https://...youtube.com/watch?v=...,Frozen - "Let It Go"...,Disney Music,50000000,227,O,공식:True, 조회수:True, 길이:True
2,...
```

**youtube_saveable_list.csv** (저장가능='O'인 항목만)
```
순번,곡명,가수,앨범,멜론링크,유튜브링크,업로더,조회수,저장가능
1,Let It Go,Idina Menzel,Frozen OST,https://...melon.com...,https://...youtube.com...,Disney Music,50000000,O
2,...
```

---

## 💻 Python 스크립트 설치 및 실행

### 사전 준비

**1. 필수 라이브러리 설치**
```bash
pip install requests beautifulsoup4 pandas yt-dlp
```

**2. Python 버전 확인**
```bash
python --version
# 권장: Python 3.8 이상
```

### 스크립트 작성

**파일명:** `melon_to_youtube_crawler.py`

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import yt_dlp
import json
from datetime import datetime

class MelonDisneyOST:
    def __init__(self, melon_playlist_url):
        self.melon_url = melon_playlist_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.songs = []
        self.final_list = []
    
    # === 1단계: 멜론 플레이리스트 크롤링 ===
    def crawl_melon_playlist(self):
        """멜론 플레이리스트에서 곡 정보 추출"""
        try:
            response = requests.get(self.melon_url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 곡 목록 찾기 (멜론 HTML 구조에 따라 수정 필요)
            song_elements = soup.find_all('tr', class_='lst50')
            
            for idx, element in enumerate(song_elements, 1):
                try:
                    # 곡명 추출
                    title = element.find('span', class_='ellipsis').text.strip()
                    
                    # 가수명 추출
                    artist = element.find_all('span', class_='ellipsis')[1].text.strip()
                    
                    # 앨범명 추출
                    album = element.find_all('span', class_='ellipsis')[2].text.strip()
                    
                    # 곡 링크 추출
                    song_link = element.find('a', href=True)['href']
                    if not song_link.startswith('http'):
                        song_link = 'https://www.melon.com' + song_link
                    
                    self.songs.append({
                        '순번': idx,
                        '곡명': title,
                        '가수': artist,
                        '앨범': album,
                        '멜론링크': song_link
                    })
                    
                    print(f"[{idx}] {title} - {artist} ✓")
                    time.sleep(0.5)  # 속도 제한
                    
                except Exception as e:
                    print(f"곡 {idx} 파싱 오류: {e}")
                    continue
            
            print(f"\n✅ 총 {len(self.songs)}개 곡 수집 완료\n")
            return self.songs
        
        except Exception as e:
            print(f"❌ 멜론 크롤링 실패: {e}")
            return []
    
    # === 2단계: 유튜브 검색 및 저장 가능성 확인 ===
    def search_youtube_and_check_download(self, title, artist):
        """각 곡을 유튜브에서 검색하고 저장 가능 여부 확인"""
        search_query = f"{title} {artist} OST"
        
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': 'in_playlist',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # 검색 실행
                info = ydl.extract_info(f"ytsearch5:{search_query}", download=False)
                
                if info and 'entries' in info:
                    # 상위 5개 중 조건 맞는 항목 찾기
                    for entry in info['entries']:
                        if entry:
                            video_id = entry['id']
                            url = f"https://www.youtube.com/watch?v={video_id}"
                            title_yt = entry.get('title', 'Unknown')
                            uploader = entry.get('uploader', 'Unknown')
                            view_count = entry.get('view_count', 0)
                            duration = entry.get('duration', 0)
                            
                            # 필터: 공식 채널, 10만+ 조회, 3~8분
                            is_official = any(x in uploader.lower() 
                                            for x in ['official', 'disney', 'music'])
                            is_valid_duration = 180 <= duration <= 480
                            is_sufficient_views = view_count >= 100000
                            
                            # 저장 가능 여부 최종 확인
                            can_download = self.check_downloadable(url)
                            
                            return {
                                '유튜브링크': url,
                                '유튜브제목': title_yt,
                                '업로더': uploader,
                                '조회수': view_count,
                                '길이': duration,
                                '저장가능': 'O' if can_download else 'X',
                                '선정사유': f"공식:{is_official}, 조회수:{is_sufficient_views}, 길이:{is_valid_duration}"
                            }
                    
                    # 조건 맞는 것이 없으면 첫 번째라도 반환
                    return {
                        '유튜브링크': f"https://www.youtube.com/watch?v={info['entries'][0]['id']}",
                        '유튜브제목': info['entries'][0]['title'],
                        '업로더': info['entries'][0].get('uploader', 'Unknown'),
                        '조회수': info['entries'][0].get('view_count', 0),
                        '길이': info['entries'][0].get('duration', 0),
                        '저장가능': '△',
                        '선정사유': '조건 미충족, 수동 확인 권장'
                    }
                    
        except Exception as e:
            print(f"⚠️  [{title} - {artist}] 유튜브 검색 실패: {e}")
        
        return {
            '유튜브링크': 'NOT_FOUND',
            '유튜브제목': 'NOT_FOUND',
            '업로더': 'N/A',
            '조회수': 0,
            '길이': 0,
            '저장가능': 'X',
            '선정사유': '검색 실패'
        }
    
    def check_downloadable(self, url):
        """yt-dlp로 실제 다운로드 가능 여부 확인"""
        try:
            ydl_opts = {'quiet': True, 'no_warnings': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(url, download=False)
            return True
        except:
            return False
    
    # === 3단계: 전체 프로세스 실행 ===
    def execute_full_process(self):
        """전체 파이프라인 실행"""
        print("="*60)
        print("[시작] 멜론 디즈니 OST → 유튜브 저장 리스트 구축")
        print("="*60 + "\n")
        
        # 1단계: 멜론 크롤링
        print("📱 [1단계] 멜론 플레이리스트 크롤링 중...\n")
        self.crawl_melon_playlist()
        
        # 2단계: 각 곡마다 유튜브 검색
        print("\n📺 [2단계] 유튜브 검색 및 저장 가능성 확인 중...\n")
        
        for idx, song in enumerate(self.songs, 1):
            print(f"[{idx}/{len(self.songs)}] {song['곡명']} - {song['가수']}", end=" ")
            
            yt_info = self.search_youtube_and_check_download(
                song['곡명'], 
                song['가수']
            )
            
            song.update(yt_info)
            self.final_list.append(song)
            
            print(f"→ {yt_info['저장가능']}")
            time.sleep(1)  # 유튜브 속도 제한
        
        # 3단계: 결과 저장
        print("\n✅ [3단계] 결과 저장 중...\n")
        self.save_results()
        
        return self.final_list
    
    def save_results(self):
        """결과를 여러 형식으로 저장"""
        # CSV 저장
        df = pd.DataFrame(self.final_list)
        df.to_csv('melon_disney_ost_complete_list.csv', index=False, encoding='utf-8-sig')
        print("✓ melon_disney_ost_complete_list.csv 저장 완료")
        
        # 저장 가능한 항목만 필터링
        saveable = df[df['저장가능'] == 'O'].copy()
        saveable.to_csv('youtube_saveable_list.csv', index=False, encoding='utf-8-sig')
        print(f"✓ youtube_saveable_list.csv 저장 완료 ({len(saveable)}개)")
        
        # JSON 형식도 저장
        with open('melon_disney_ost_list.json', 'w', encoding='utf-8') as f:
            json.dump(self.final_list, f, ensure_ascii=False, indent=2)
        print("✓ melon_disney_ost_list.json 저장 완료")
        
        # 실행 로그
        with open('execution_log.txt', 'w', encoding='utf-8') as f:
            f.write(f"실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"멜론 플레이리스트 URL: {self.melon_url}\n")
            f.write(f"총 수집 곡: {len(self.songs)}개\n")
            f.write(f"저장 가능: {len(saveable)}개\n")
            f.write(f"저장 불가능: {len(df[df['저장가능'] == 'X'])}개\n")
            f.write(f"수동 확인 필요: {len(df[df['저장가능'] == '△'])}개\n")
        print("✓ execution_log.txt 저장 완료")
        
        # 요약 통계
        print("\n" + "="*60)
        print("[완료 통계]")
        print("="*60)
        print(f"✅ 저장 가능: {len(saveable)}개")
        print(f"❌ 저장 불가능: {len(df[df['저장가능'] == 'X'])}개")
        print(f"△ 수동 확인: {len(df[df['저장가능'] == '△'])}개")

# === 실행 ===
if __name__ == "__main__":
    # ⚠️  여기에 멜론 플레이리스트 URL을 입력하세요
    MELON_PLAYLIST_URL = "https://www.melon.com/playlist/detail.htm?plstId=XXXXXX"
    
    crawler = MelonDisneyOST(MELON_PLAYLIST_URL)
    result = crawler.execute_full_process()
```

### 실행 방법

**Step 1: 스크립트에 URL 입력**
```python
# 23번째 줄 수정
MELON_PLAYLIST_URL = "https://www.melon.com/playlist/detail.htm?plstId=123456789"
```

**Step 2: 터미널에서 실행**
```bash
python melon_to_youtube_crawler.py
```

**Step 3: 진행 상황 확인**
```
============================================================
[시작] 멜론 디즈니 OST → 유튜브 저장 리스트 구축
============================================================

📱 [1단계] 멜론 플레이리스트 크롤링 중...

[1] Let It Go - Idina Menzel ✓
[2] Into the Unknown - Idina Menzel ✓
...
✅ 총 45개 곡 수집 완료

📺 [2단계] 유튜브 검색 및 저장 가능성 확인 중...

[1/45] Let It Go - Idina Menzel → O
[2/45] Into the Unknown - Idina Menzel → O
...

============================================================
[완료 통계]
============================================================
✅ 저장 가능: 38개
❌ 저장 불가능: 5개
△ 수동 확인: 2개
```

---

## 📊 데이터 활용 방법

### 1. CSV 파일로 열기

**Excel 또는 Google Sheets에서 열기**
```
1. youtube_saveable_list.csv 파일 더블클릭
2. 또는 Excel → 파일 → 열기 → 파일 선택
```

### 2. Python에서 데이터 분석

```python
import pandas as pd

# 저장 가능한 곡 목록 로드
df = pd.read_csv('youtube_saveable_list.csv', encoding='utf-8-sig')

# 기본 정보
print(f"총 곡 개수: {len(df)}")
print(f"\n상위 10개 곡:")
print(df[['곡명', '가수', '조회수']].head(10))

# 조회수 순으로 정렬
df_sorted = df.sort_values('조회수', ascending=False)
print(f"\n조회수 많은 순서:")
print(df_sorted[['곡명', '가수', '조회수', '업로더']].head())
```

### 3. JSON으로 데이터 다루기

```python
import json

# JSON 로드
with open('melon_disney_ost_list.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 첫 번째 곡 정보 확인
print(json.dumps(data[0], ensure_ascii=False, indent=2))
```

---

## ⚠️ 주의사항 및 팁

| 항목 | 내용 |
|------|------|
| **저작권** | 개인 수집용으로만 사용, 배포 금지 |
| **속도** | 멜론/유튜브 서버 부하 최소화를 위해 딜레이 설정 |
| **오류 재시도** | 실패한 곡은 수동으로 다시 검색 권장 |
| **메모리** | 곡이 100개 이상인 경우 배치 처리 검토 |
| **VPN** | 지역 제한으로 실패 시 VPN 사용 검토 |

---

## 📝 체크리스트

진행 상황을 확인하며 작업하세요.

- [ ] 멜론 플레이리스트 URL 복사 완료
- [ ] 필수 라이브러리 설치 (pip install)
- [ ] Python 스크립트 작성 완료
- [ ] 스크립트에 URL 입력
- [ ] 첫 번째 테스트 실행 (처음 5곡만 테스트 권장)
- [ ] 전체 곡 실행
- [ ] CSV 파일 생성 확인
- [ ] 저장 가능 리스트 검증
- [ ] 수동 확인 필요 곡 처리
- [ ] 최종 리스트 정리 완료

---

## 🔗 참고 자료

- **멜론 공식 사이트**: https://www.melon.com
- **yt-dlp 문서**: https://github.com/yt-dlp/yt-dlp
- **BeautifulSoup 문서**: https://www.crummy.com/software/BeautifulSoup/
- **Pandas 문서**: https://pandas.pydata.org/docs/

---

**작성일**: 2026-06-14  
**수정일**: 최종  
**상태**: ✅ 실행 준비 완료
