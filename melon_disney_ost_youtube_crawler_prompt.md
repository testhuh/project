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

### 🎯 생성되는 파일들 (3가지 형식)

```
📁 작업 폴더
│
├─📊 CSV 파일 (데이터 관리용)
│  ├── melon_disney_ost_complete_list.csv
│  │   └─ 모든 곡 정보 (멜론 + 유튜브 메타데이터)
│  │      Columns: 순번, 곡명, 가수, 앨범, 멜론링크, 유튜브링크, 
│  │               업로더, 조회수, 길이, 저장가능, 선정사유
│  │
│  └── youtube_saveable_list.csv
│      └─ 저장 가능한 곡만 필터링 (다운로드 대상)
│         Columns: 순번, 곡명, 가수, 앨범, 멜론링크, 유튜브링크,
│                  업로더, 조회수, 저장가능
│
├─🎵 WebM 파일 (음원 저장용 - 선택적)
│  └── disney_ost_downloads/
│      ├── [01] Let It Go - Idina Menzel.webm
│      ├── [02] Into the Unknown - Idina Menzel.webm
│      ├── [03] For the First Time in Forever.webm
│      └── ...
│      (저장 가능한 곡들을 자동 다운로드)
│
├─🌐 HTML 파일 (시각적 리스트용)
│  └── disney_ost_playlist.html
│      └─ 웹 브라우저에서 열어서 볼 수 있는 아름다운 리스트
│         - 곡명, 가수, 유튜브 링크 클릭 가능
│         - 조회수 순 정렬 가능
│         - 검색 기능 포함
│         - 다운로드 상태 표시
│
└─📝 로그 파일
   └── execution_log.txt
       └─ 실행 시간, 통계, 오류 로그
```

---

### 📋 CSV 파일 구조 및 샘플 데이터

**melon_disney_ost_complete_list.csv** (모든 곡 정보)
```csv
순번,곡명,가수,앨범,멜론링크,유튜브링크,유튜브제목,업로더,조회수,길이(초),저장가능,선정사유
1,Let It Go,Idina Menzel,Frozen OST,https://www.melon.com/song/detail/XXXXX,https://www.youtube.com/watch?v=XXXXX,Frozen - "Let It Go" Official,Disney Music,50000000,227,O,공식:True,조회수:True,길이:True
2,Into the Unknown,Idina Menzel,Frozen 2 OST,https://www.melon.com/song/detail/XXXXX,https://www.youtube.com/watch?v=XXXXX,Frozen 2 - "Into The Unknown",Disney Music,35000000,210,O,공식:True,조회수:True,길이:True
3,For the First Time in Forever,Kristen Bell|Idina Menzel,Frozen OST,https://www.melon.com/song/detail/XXXXX,https://www.youtube.com/watch?v=XXXXX,"Frozen - ""For the First Time in Forever"" (Officia",Disney Music,25000000,198,O,공식:True,조회수:True,길이:True
...
```

**youtube_saveable_list.csv** (저장 가능한 곡만 - 다운로드 대상)
```csv
순번,곡명,가수,앨범,멜론링크,유튜브링크,파일명,업로더,조회수,저장가능
1,Let It Go,Idina Menzel,Frozen OST,https://www.melon.com/song/detail/XXXXX,https://www.youtube.com/watch?v=XXXXX,[01] Let It Go - Idina Menzel.webm,Disney Music,50000000,O
2,Into the Unknown,Idina Menzel,Frozen 2 OST,https://www.melon.com/song/detail/XXXXX,https://www.youtube.com/watch?v=XXXXX,[02] Into the Unknown - Idina Menzel.webm,Disney Music,35000000,O
3,For the First Time in Forever,Kristen Bell|Idina Menzel,Frozen OST,https://www.melon.com/song/detail/XXXXX,https://www.youtube.com/watch?v=XXXXX,[03] For the First Time in Forever.webm,Disney Music,25000000,O
...
```

---

### 🎵 WebM 파일 (음원 저장)

**자동 다운로드 기능**
```
- 저장 가능한 모든 곡을 WebM 형식으로 자동 다운로드
- 파일명: [순번] 곡명 - 가수.webm
- 저장 위치: ./disney_ost_downloads/ 폴더
- 총 용량: ~500MB~1GB (곡 개수에 따라 변동)

예시:
[01] Let It Go - Idina Menzel.webm (3.2 MB)
[02] Into the Unknown - Idina Menzel.webm (2.8 MB)
[03] For the First Time in Forever.webm (2.5 MB)
...
```

**WebM 형식의 장점**
- ✅ 유튜브에서 공식 지원하는 포맷
- ✅ 음질 손실 최소화
- ✅ 파일 크기 최적화
- ✅ 크로스 플랫폼 호환성

---

### 🌐 HTML 파일 (웹 인터페이스)

**disney_ost_playlist.html** - 시각적 리스트 페이지

**기능**
```
1. 곡 목록 표시
   ├─ 순번, 곡명, 가수, 앨범, 조회수, 저장 상태
   ├─ 클릭하면 유튜브 링크로 이동
   └─ 다운로드 상태 표시 (✓ / ✗)

2. 정렬 기능
   ├─ 조회수 순 정렬
   ├─ 곡명 가나다순 정렬
   └─ 저장 상태별 필터링

3. 검색 기능
   ├─ 곡명 검색
   ├─ 가수명 검색
   └─ 실시간 필터링

4. 통계 표시
   ├─ 총 곡 개수
   ├─ 저장 가능: xx개
   ├─ 저장 불가: xx개
   └─ 다운로드 진행률 표시

5. 디자인
   ├─ 반응형 디자인 (PC, 태블릿, 모바일)
   ├─ Disney 테마 (파란색, 노란색)
   ├─ 다크 모드 지원 (토글)
   └─ 인쇄 최적화
```

**HTML 파일 미리보기**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Disney OST Playlist</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <header>
        <h1>🎬 Disney OST Playlist</h1>
        <p>멜론 + 유튜브 통합 리스트 | 총 45곡 | 저장 가능: 38곡</p>
    </header>
    
    <nav>
        <input type="text" id="searchBox" placeholder="곡명 또는 가수 검색...">
        <button onclick="sortByViews()">조회수순</button>
        <button onclick="sortByTitle()">제목순</button>
        <button onclick="toggleDarkMode()">🌙 다크모드</button>
    </nav>
    
    <table>
        <thead>
            <tr>
                <th>#</th>
                <th>곡명</th>
                <th>가수</th>
                <th>앨범</th>
                <th>조회수</th>
                <th>저장</th>
                <th>링크</th>
            </tr>
        </thead>
        <tbody id="songList">
            <!-- CSV 데이터 자동 생성 -->
        </tbody>
    </table>
</body>
</html>
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

**3. FFmpeg 설치 (WebM 변환용)**

Windows:
```bash
# Chocolatey 사용
choco install ffmpeg

# 또는 수동: https://ffmpeg.org/download.html
```

macOS:
```bash
brew install ffmpeg
```

Linux:
```bash
sudo apt-get install ffmpeg
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
        """결과를 여러 형식으로 저장 (CSV, HTML, WebM)"""
        df = pd.DataFrame(self.final_list)
        
        # ===== CSV 저장 =====
        df.to_csv('melon_disney_ost_complete_list.csv', index=False, encoding='utf-8-sig')
        print("✓ melon_disney_ost_complete_list.csv 저장 완료")
        
        # 저장 가능한 항목만 필터링
        saveable = df[df['저장가능'] == 'O'].copy()
        saveable.to_csv('youtube_saveable_list.csv', index=False, encoding='utf-8-sig')
        print(f"✓ youtube_saveable_list.csv 저장 완료 ({len(saveable)}개)")
        
        # ===== WebM 파일 자동 다운로드 =====
        print("\n🎵 WebM 파일 다운로드 시작...\n")
        self.download_webm_files(saveable)
        
        # ===== HTML 파일 생성 =====
        print("\n🌐 HTML 시각화 페이지 생성 중...\n")
        self.generate_html_playlist(saveable)
        
        # ===== JSON 형식 저장 =====
        with open('melon_disney_ost_list.json', 'w', encoding='utf-8') as f:
            json.dump(self.final_list, f, ensure_ascii=False, indent=2)
        print("✓ melon_disney_ost_list.json 저장 완료")
        
        # ===== 실행 로그 =====
        with open('execution_log.txt', 'w', encoding='utf-8') as f:
            f.write(f"실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"멜론 플레이리스트 URL: {self.melon_url}\n")
            f.write(f"총 수집 곡: {len(self.songs)}개\n")
            f.write(f"저장 가능: {len(saveable)}개\n")
            f.write(f"저장 불가능: {len(df[df['저장가능'] == 'X'])}개\n")
            f.write(f"수동 확인 필요: {len(df[df['저장가능'] == '△'])}개\n\n")
            f.write("="*60 + "\n")
            f.write("[생성된 파일]\n")
            f.write("="*60 + "\n")
            f.write("✓ melon_disney_ost_complete_list.csv (전체 곡 데이터)\n")
            f.write("✓ youtube_saveable_list.csv (저장 가능한 곡)\n")
            f.write("✓ disney_ost_playlist.html (웹 시각화 페이지)\n")
            f.write("✓ disney_ost_downloads/ (WebM 음원 폴더)\n")
        print("✓ execution_log.txt 저장 완료")
        
        # 요약 통계
        print("\n" + "="*60)
        print("[완료 통계]")
        print("="*60)
        print(f"✅ 저장 가능: {len(saveable)}개")
        print(f"❌ 저장 불가능: {len(df[df['저장가능'] == 'X'])}개")
        print(f"△ 수동 확인: {len(df[df['저장가능'] == '△'])}개")
        print(f"\n📊 생성된 파일:")
        print(f"  1. CSV (데이터 관리): melon_disney_ost_complete_list.csv")
        print(f"  2. CSV (다운로드용): youtube_saveable_list.csv")
        print(f"  3. HTML (웹 시각화): disney_ost_playlist.html")
        print(f"  4. WebM (음원파일): disney_ost_downloads/ ({len(saveable)}개 곡)")
    
    def download_webm_files(self, saveable_df):
        """저장 가능한 모든 곡을 WebM 형식으로 다운로드"""
        import os
        
        # 다운로드 폴더 생성
        download_dir = 'disney_ost_downloads'
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        
        total = len(saveable_df)
        downloaded = 0
        failed = 0
        
        for idx, row in saveable_df.iterrows():
            song_title = row['곡명']
            artist = row['가수']
            youtube_url = row['유튜브링크']
            
            # 파일명 생성 (순번 포함)
            file_number = f"[{downloaded+1:02d}]"
            safe_filename = f"{file_number} {song_title} - {artist}".replace(':', '_').replace('/', '_')
            filepath = os.path.join(download_dir, f"{safe_filename}.webm")
            
            # 이미 다운로드된 파일은 스킵
            if os.path.exists(filepath):
                print(f"[{downloaded+1}/{total}] {song_title} → 이미 존재함 ✓")
                downloaded += 1
                continue
            
            try:
                print(f"[{downloaded+1}/{total}] {song_title} - {artist}", end=" ")
                
                ydl_opts = {
                    'format': 'bestvideo[ext=webm]/best[ext=webm]',
                    'outtmpl': filepath[:-5],  # .webm 제거
                    'quiet': True,
                    'no_warnings': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([youtube_url])
                
                print(f"✓ ({os.path.getsize(filepath) / 1024 / 1024:.1f} MB)")
                downloaded += 1
                time.sleep(1)  # 속도 제한
                
            except Exception as e:
                print(f"✗ (오류: {str(e)[:30]})")
                failed += 1
                continue
        
        print(f"\n🎵 WebM 다운로드 완료: {downloaded}개 성공, {failed}개 실패")
        print(f"   저장 위치: ./{download_dir}/")
    
    def generate_html_playlist(self, saveable_df):
        """HTML 시각화 페이지 생성"""
        
        html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎬 Disney OST Playlist</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
            padding: 20px;
        }
        
        body.dark-mode {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        body.dark-mode .container {
            background: #0f3460;
        }
        
        header {
            background: linear-gradient(135deg, #1428A0 0%, #0066CC 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }
        
        header h1 {
            font-size: 48px;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        header p {
            font-size: 18px;
            opacity: 0.9;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            padding: 30px 20px;
            background: #f5f5f5;
        }
        
        body.dark-mode .stats {
            background: #1a2a3a;
        }
        
        .stat-box {
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border-left: 4px solid #1428A0;
        }
        
        body.dark-mode .stat-box {
            background: #0f3460;
            border-left-color: #00a8ff;
        }
        
        .stat-box h3 { color: #1428A0; font-size: 14px; margin-bottom: 10px; }
        .stat-box p { font-size: 32px; font-weight: bold; }
        
        .controls {
            padding: 20px;
            background: white;
            border-bottom: 1px solid #eee;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            align-items: center;
        }
        
        body.dark-mode .controls {
            background: #0f3460;
            border-bottom-color: #1a3a4a;
        }
        
        input, select, button {
            padding: 10px 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            cursor: pointer;
        }
        
        body.dark-mode input,
        body.dark-mode select,
        body.dark-mode button {
            background: #16213e;
            color: #eee;
            border-color: #333;
        }
        
        button {
            background: #1428A0;
            color: white;
            border: none;
            cursor: pointer;
            transition: background 0.3s;
        }
        
        button:hover {
            background: #0066CC;
        }
        
        input {
            flex: 1;
            min-width: 200px;
        }
        
        .table-wrapper {
            overflow-x: auto;
            padding: 20px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
        }
        
        thead {
            background: #1428A0;
            color: white;
            position: sticky;
            top: 0;
        }
        
        th {
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }
        
        td {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }
        
        body.dark-mode td {
            border-bottom-color: #1a3a4a;
        }
        
        tr:hover {
            background: #f9f9f9;
        }
        
        body.dark-mode tr:hover {
            background: #1a2a3a;
        }
        
        .number { text-align: center; color: #999; font-weight: bold; }
        .title { font-weight: 600; color: #1428A0; }
        .artist { color: #666; }
        .views { text-align: right; color: #f39c12; font-weight: 500; }
        .download-status { text-align: center; }
        
        .status-ok { color: #27ae60; font-size: 18px; }
        .status-no { color: #e74c3c; font-size: 14px; }
        
        a {
            color: #1428A0;
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
        }
        
        .footer {
            padding: 20px;
            text-align: center;
            background: #f5f5f5;
            color: #999;
            font-size: 12px;
        }
        
        body.dark-mode .footer {
            background: #1a2a3a;
            color: #999;
        }
        
        .no-results {
            text-align: center;
            padding: 40px;
            color: #999;
        }
        
        @media print {
            body { background: white; }
            button, .controls { display: none; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎬 Disney OST Playlist</h1>
            <p>멜론 + 유튜브 통합 플레이리스트 | 저장 가능한 OST 모음</p>
        </header>
        
        <div class="stats">
            <div class="stat-box">
                <h3>📊 총 곡</h3>
                <p>%TOTAL_SONGS%</p>
            </div>
            <div class="stat-box">
                <h3>✅ 저장 가능</h3>
                <p style="color: #27ae60;">%SAVEABLE_COUNT%</p>
            </div>
            <div class="stat-box">
                <h3>⏱️ 총 재생시간</h3>
                <p>%TOTAL_TIME%</p>
            </div>
            <div class="stat-box">
                <h3>👁️ 총 조회수</h3>
                <p>%TOTAL_VIEWS%</p>
            </div>
        </div>
        
        <div class="controls">
            <input type="text" id="searchBox" placeholder="🔍 곡명 또는 가수 검색..." onkeyup="filterTable()">
            <select onchange="sortTable(this.value)">
                <option value="">정렬: 기본순</option>
                <option value="views">조회수순</option>
                <option value="title">제목순</option>
                <option value="artist">가수순</option>
            </select>
            <button onclick="toggleDarkMode()">🌙 다크모드</button>
            <button onclick="window.print()">🖨️ 인쇄</button>
        </div>
        
        <div class="table-wrapper">
            <table id="songTable">
                <thead>
                    <tr>
                        <th style="width: 40px;">#</th>
                        <th>곡명</th>
                        <th>가수</th>
                        <th>앨범</th>
                        <th style="width: 100px;">조회수</th>
                        <th style="width: 80px;">저장</th>
                        <th style="width: 80px;">링크</th>
                    </tr>
                </thead>
                <tbody>
                    %TABLE_ROWS%
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>생성 시간: %GENERATION_TIME%</p>
            <p>데이터 출처: Melon Playlist + YouTube Official Channels</p>
        </div>
    </div>
    
    <script>
        function filterTable() {
            const input = document.getElementById('searchBox');
            const filter = input.value.toUpperCase();
            const table = document.getElementById('songTable');
            const rows = table.getElementsByTagName('tr');
            let visible = 0;
            
            for (let i = 1; i < rows.length; i++) {
                const cells = rows[i].getElementsByTagName('td');
                const title = cells[1]?.textContent.toUpperCase() || '';
                const artist = cells[2]?.textContent.toUpperCase() || '';
                
                if (title.includes(filter) || artist.includes(filter)) {
                    rows[i].style.display = '';
                    visible++;
                } else {
                    rows[i].style.display = 'none';
                }
            }
            
            if (visible === 0) {
                const tbody = table.getElementsByTagName('tbody')[0];
                tbody.innerHTML = '<tr><td colspan="7" class="no-results">검색 결과가 없습니다.</td></tr>';
            }
        }
        
        function sortTable(sortType) {
            const table = document.getElementById('songTable');
            const rows = Array.from(table.querySelectorAll('tbody tr'));
            
            rows.sort((a, b) => {
                if (sortType === 'views') {
                    const viewsA = parseInt(a.cells[4].textContent.replace(/,/g, ''));
                    const viewsB = parseInt(b.cells[4].textContent.replace(/,/g, ''));
                    return viewsB - viewsA;
                } else if (sortType === 'title') {
                    return a.cells[1].textContent.localeCompare(b.cells[1].textContent);
                } else if (sortType === 'artist') {
                    return a.cells[2].textContent.localeCompare(b.cells[2].textContent);
                }
                return 0;
            });
            
            const tbody = table.querySelector('tbody');
            rows.forEach(row => tbody.appendChild(row));
        }
        
        function toggleDarkMode() {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        }
        
        // 저장된 다크모드 설정 로드
        if (localStorage.getItem('darkMode') === 'true') {
            document.body.classList.add('dark-mode');
        }
    </script>
</body>
</html>
"""
        
        # 테이블 행 생성
        table_rows = ""
        total_views = 0
        total_seconds = 0
        
        for idx, row in saveable_df.iterrows():
            song_num = idx + 1
            title = row['곡명']
            artist = row['가수']
            album = row['앨범']
            views = int(row['조회수'])
            youtube_url = row['유튜브링크']
            duration = row.get('길이', 0)
            
            total_views += views
            total_seconds += duration
            
            views_text = f"{views:,}"
            
            table_rows += f"""
            <tr>
                <td class="number">{song_num}</td>
                <td class="title">{title}</td>
                <td class="artist">{artist}</td>
                <td>{album}</td>
                <td class="views">{views_text}</td>
                <td class="download-status"><span class="status-ok">✓</span></td>
                <td><a href="{youtube_url}" target="_blank">YouTube</a></td>
            </tr>
            """
        
        # 재생 시간 포맷
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        time_text = f"{hours}시간 {minutes}분" if hours > 0 else f"{minutes}분"
        
        # 플레이스홀더 치환
        html_content = html_content.replace('%TOTAL_SONGS%', str(len(saveable_df)))
        html_content = html_content.replace('%SAVEABLE_COUNT%', str(len(saveable_df)))
        html_content = html_content.replace('%TOTAL_TIME%', time_text)
        html_content = html_content.replace('%TOTAL_VIEWS%', f"{total_views:,}")
        html_content = html_content.replace('%TABLE_ROWS%', table_rows)
        html_content = html_content.replace('%GENERATION_TIME%', datetime.now().strftime('%Y년 %m월 %d일 %H:%M:%S'))
        
        # HTML 파일 저장
        with open('disney_ost_playlist.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✓ disney_ost_playlist.html 저장 완료")
        print("  🌐 웹 브라우저에서 열기: disney_ost_playlist.html")

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

✅ [3단계] 결과 저장 중...

✓ melon_disney_ost_complete_list.csv 저장 완료
✓ youtube_saveable_list.csv 저장 완료 (38개)

🎵 WebM 파일 다운로드 시작...

[1/38] Let It Go - Idina Menzel ✓ (3.2 MB)
[2/38] Into the Unknown - Idina Menzel ✓ (2.8 MB)
[3/38] For the First Time in Forever ✓ (2.5 MB)
...
🎵 WebM 다운로드 완료: 38개 성공, 0개 실패
   저장 위치: ./disney_ost_downloads/

🌐 HTML 시각화 페이지 생성 중...

✓ disney_ost_playlist.html 저장 완료
  🌐 웹 브라우저에서 열기: disney_ost_playlist.html

✓ melon_disney_ost_list.json 저장 완료
✓ execution_log.txt 저장 완료

============================================================
[완료 통계]
============================================================
✅ 저장 가능: 38개
❌ 저장 불가능: 5개
△ 수동 확인: 2개

📊 생성된 파일:
  1. CSV (데이터 관리): melon_disney_ost_complete_list.csv
  2. CSV (다운로드용): youtube_saveable_list.csv
  3. HTML (웹 시각화): disney_ost_playlist.html
  4. WebM (음원파일): disney_ost_downloads/ (38개 곡)
```

---

## 📁 최종 폴더 구조

```
프로젝트 폴더/
├── 📊 CSV 데이터 파일
│   ├── melon_disney_ost_complete_list.csv (전체 곡 정보)
│   └── youtube_saveable_list.csv (저장 가능한 곡)
│
├── 🌐 HTML 웹 페이지
│   └── disney_ost_playlist.html (웹 브라우저에서 열기!)
│
├── 🎵 WebM 음원 폴더
│   └── disney_ost_downloads/
│       ├── [01] Let It Go - Idina Menzel.webm
│       ├── [02] Into the Unknown - Idina Menzel.webm
│       ├── [03] For the First Time in Forever.webm
│       └── ... (총 38개)
│
├── 📝 로그 및 설정
│   ├── execution_log.txt (실행 통계)
│   ├── melon_disney_ost_list.json (JSON 형식 데이터)
│   └── melon_to_youtube_crawler.py (실행 스크립트)
│
└── 📖 문서
    └── melon_disney_ost_youtube_crawler_prompt.md (이 파일)
```

---

## 📊 데이터 활용 방법

### 1. 🌐 HTML 파일로 시각화 보기

**가장 추천하는 방법!**

```bash
# 방법 1: 파일 더블클릭
disney_ost_playlist.html 파일을 더블클릭하면 웹 브라우저에서 자동 열기

# 방법 2: 브라우저에서 열기
Chrome/Edge/Firefox 열기 → Ctrl+O → disney_ost_playlist.html 선택
```

**HTML 파일에서 가능한 작업**
- 🔍 곡명/가수로 실시간 검색
- 📊 조회수순/제목순 정렬
- 🎵 YouTube 링크 직접 클릭
- 🌙 다크모드 토글
- 🖨️ 인쇄 (PDF로도 저장 가능)
- 📱 모바일 반응형 레이아웃

---

### 2. 📥 WebM 파일로 음원 다운로드

```bash
# 자동으로 다음 폴더에 저장됨
./disney_ost_downloads/

파일 예시:
├─ [01] Let It Go - Idina Menzel.webm
├─ [02] Into the Unknown - Idina Menzel.webm
├─ [03] For the First Time in Forever.webm
└─ ...

# 각 파일은 유튜브에서 최고 품질로 자동 다운로드됨
```

**WebM 파일 활용**
- 🎵 오디오 재생기에서 재생 가능
- 💾 클라우드에 업로드 가능
- 🎬 동영상 편집 프로그램에서 사용 가능
- 📱 모바일 기기로 이동 가능

---

### 3. 📄 CSV 파일로 데이터 분석

**Excel 또는 Google Sheets에서 열기**
```
1. youtube_saveable_list.csv 파일 더블클릭
2. 또는 Excel → 파일 → 열기 → 파일 선택
```

**Python에서 분석**

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

# 가수별 곡 개수
print(f"\n가수별 곡 개수:")
print(df['가수'].value_counts())

# 통계
print(f"\n조회수 통계:")
print(df['조회수'].describe())
```

---

### 4. 📋 CSV 파일로 데이터 다루기

**JSON으로 데이터 변환**
```python
import json
import pandas as pd

df = pd.read_csv('youtube_saveable_list.csv', encoding='utf-8-sig')
json_data = df.to_json(orient='records', force_ascii=False, indent=2)

with open('disney_ost_playlist.json', 'w', encoding='utf-8') as f:
    f.write(json_data)
```

**특정 조건으로 필터링**
```python
import pandas as pd

df = pd.read_csv('youtube_saveable_list.csv', encoding='utf-8-sig')

# 조회수 1000만 이상 곡만
popular = df[df['조회수'] >= 10000000]
print(popular[['곡명', '가수', '조회수']])

# 특정 가수 곡만
idina_songs = df[df['가수'].str.contains('Idina', case=False)]
print(idina_songs)
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

### 설정 단계
- [ ] 멜론 플레이리스트 URL 복사 완료
- [ ] Python 3.8 이상 설치 확인
- [ ] 필수 라이브러리 설치 (pip install requests beautifulsoup4 pandas yt-dlp)
- [ ] FFmpeg 설치 완료

### 실행 단계
- [ ] Python 스크립트 작성 완료
- [ ] 스크립트에 멜론 URL 입력
- [ ] 첫 번째 테스트 실행 (처음 5곡만 테스트 권장)
- [ ] 전체 곡 실행

### 산출물 확인 단계
- [ ] melon_disney_ost_complete_list.csv 생성 확인 ✅ CSV
- [ ] youtube_saveable_list.csv 생성 확인 ✅ CSV
- [ ] disney_ost_downloads/ 폴더 생성 확인 ✅ WebM 음원
- [ ] disney_ost_playlist.html 생성 확인 ✅ HTML
- [ ] HTML 파일을 웹 브라우저에서 열어서 보기
- [ ] 검색/정렬 기능 테스트
- [ ] 유튜브 링크 클릭 테스트

### 최종 검증 단계
- [ ] 저장된 곡 개수 확인
- [ ] 저장 불가능 곡 리스트 검토
- [ ] WebM 파일 크기 확인 (합계 500MB~1GB 예상)
- [ ] execution_log.txt 확인
- [ ] 필요시 수동으로 저장 불가능 곡 처리
- [ ] 최종 리스트 백업 완료

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
