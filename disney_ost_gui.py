"""
Disney OST Playlist — 카드 그리드 대시보드 GUI
실행: python disney_ost_gui.py

요구사항:
    pip install playwright python-dotenv
    playwright install chromium
"""

import os
import json
import time
import shutil
import random
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from datetime import datetime
from pathlib import Path

PLAYLIST_TITLE = "disney_ost_playlist"

SONGS = [
    "Jessie J Part Of Your World From The Little Mermaid",
    "Gregory Porter When You Wish Upon A Star Disney",
    "Frozen 2 Karaoke Show Yourself Instrumental with Chorus",
    "Lofi Pixar Disney Lofi Steal The Show Lofi Ver",
    "Sofia the First Main Title Theme Cast Disney Junior",
    "Christina Aguilera Reflection Official Disney",
    "Daveed Diggs Under the Sea The Little Mermaid Disney",
    "Brad Kane Lea Salonga A Whole New World Remastered 2022",
    "Sara Bareilles When You Wish Upon a Star Disney 100",
    "Lang Lang Royal Philharmonic Orchestra Remember Me Coco",
    "Cliff Edwards Disney Studio Chorus When You Wish Upon a Star",
    "Angela Lansbury Disney Beauty and the Beast",
    "Royal Philharmonic Orchestra How Far I'll Go Moana",
    "DCappella Love Is an Open Door Disney",
    "Peabo Bryson Regina Belle A Whole New World",
    "Samuel E Wright Disney Under the Sea Official",
    "Naomi Scott Speechless Full Aladdin Official",
    "Royal Philharmonic Orchestra I See The Light Tangled",
]

TOTAL = len(SONGS)

# ── 색상 팔레트 ────────────────────────────────────────────────
C = {
    "bg":      "#0a0a1a",
    "panel":   "#12122a",
    "card":    "#1c1c35",
    "border":  "#2a2a50",
    "accent":  "#1e90ff",
    "accent2": "#6ab0ff",
    "success": "#00c896",
    "fail":    "#ff4747",
    "text":    "#e8eaf6",
    "muted":   "#7788aa",
    "white":   "#ffffff",
    "gold":    "#ffd700",
    # 카드 상태별
    "c_wait_bg":  "#1c1c35", "c_wait_bd":  "#2a2a50", "c_wait_fg":  "#7788aa",
    "c_act_bg":   "#0d1f3c", "c_act_bd":   "#1e90ff", "c_act_fg":   "#6ab0ff",
    "c_done_bg":  "#0a2420", "c_done_bd":  "#00c896", "c_done_fg":  "#00c896",
    "c_fail_bg":  "#2a0d10", "c_fail_bd":  "#ff4747", "c_fail_fg":  "#ff4747",
}

# ── 카드 상태 설정 ─────────────────────────────────────────────
CARD_CFG = {
    "waiting": dict(icon="⏳", label="대기",   bg=C["c_wait_bg"], bd=C["c_wait_bd"], fg=C["c_wait_fg"]),
    "active":  dict(icon="▶",  label="진행중", bg=C["c_act_bg"],  bd=C["c_act_bd"],  fg=C["c_act_fg"]),
    "success": dict(icon="✅", label="완료",   bg=C["c_done_bg"], bd=C["c_done_bd"], fg=C["c_done_fg"]),
    "fail":    dict(icon="❌", label="실패",   bg=C["c_fail_bg"], bd=C["c_fail_bd"], fg=C["c_fail_fg"]),
}

# ── 공유 상태 ──────────────────────────────────────────────────
state = {
    "running":    False,
    "stop_flag":  False,
    "success":    0,
    "fail":       0,
    "current":    0,
    "results":    [],
    "start_time": None,
}


# ══════════════════════════════════════════════════════════════
#  리스트 행 위젯
# ══════════════════════════════════════════════════════════════
ROW_CFG = {
    "waiting": dict(icon="⏳", label="대기",   fg=C["muted"],   bg=C["card"],     bd=C["border"]),
    "active":  dict(icon="▶",  label="진행중", fg=C["accent"],  bg=C["c_act_bg"], bd=C["accent"]),
    "success": dict(icon="✅", label="완료",   fg=C["success"], bg=C["c_done_bg"],bd=C["success"]),
    "fail":    dict(icon="❌", label="실패",   fg=C["fail"],    bg=C["c_fail_bg"],bd=C["fail"]),
}

class SongRow(tk.Frame):
    def __init__(self, parent, number: int, song: str, **kw):
        cfg = ROW_CFG["waiting"]
        super().__init__(parent, bg=cfg["bg"], pady=5, padx=10,
                         highlightthickness=1, highlightbackground=cfg["bd"], **kw)
        self._status    = "waiting"
        self._blink_job = None
        self._blink_on  = True
        self._master    = None

        self._num = tk.Label(self, text=f"{number:02d}",
                             font=("Segoe UI", 9, "bold"),
                             bg=cfg["bg"], fg="#334466", width=3, anchor="center")
        self._num.pack(side="left")

        self._icon = tk.Label(self, text=cfg["icon"],
                              font=("Segoe UI", 12),
                              bg=cfg["bg"], fg=cfg["fg"], width=3, anchor="center")
        self._icon.pack(side="left", padx=(4, 8))

        self._title = tk.Label(self, text=song,
                               font=("Segoe UI", 9),
                               bg=cfg["bg"], fg=C["text"], anchor="w")
        self._title.pack(side="left", fill="x", expand=True)

        self._status_lbl = tk.Label(self, text=cfg["label"],
                                    font=("Segoe UI", 8, "bold"),
                                    bg=cfg["bg"], fg=cfg["fg"], width=6, anchor="e")
        self._status_lbl.pack(side="right", padx=(8, 0))

    def set_status(self, status: str, master: tk.Misc = None):
        if self._blink_job and self._master:
            self._master.after_cancel(self._blink_job)
            self._blink_job = None

        self._status = status
        self._master = master
        cfg = ROW_CFG[status]

        self.configure(bg=cfg["bg"], highlightbackground=cfg["bd"])
        for w in (self._num, self._icon, self._title, self._status_lbl):
            w.configure(bg=cfg["bg"])
        self._icon.configure(fg=cfg["fg"], text=cfg["icon"])
        self._status_lbl.configure(fg=cfg["fg"], text=cfg["label"])
        self._num.configure(fg="#334466" if status == "waiting" else cfg["fg"])

        if status == "active" and master:
            self._blink_on = True
            self._blink(master)

    def _blink(self, master: tk.Misc):
        if self._status != "active":
            return
        self._icon.configure(text="▶" if self._blink_on else "  ")
        self._blink_on = not self._blink_on
        self._blink_job = master.after(480, lambda: self._blink(master))


# ══════════════════════════════════════════════════════════════
#  자동화 스레드
# ══════════════════════════════════════════════════════════════
def run_automation(log_cb, stat_cb, done_cb):
    try:
        from dotenv import load_dotenv
        load_dotenv(Path(__file__).parent / ".env")
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    except ImportError as e:
        log_cb(f"[ERROR] 패키지 없음: {e}\npip install playwright python-dotenv 후 재시도", "fail")
        done_cb()
        return

    CHROME_USER_DATA = Path(os.environ.get("LOCALAPPDATA", "")) / "Google" / "Chrome" / "User Data"
    TEMP_PROFILE     = Path(os.environ.get("TEMP", ""))         / "yt-playlist-profile-disney"
    BROWSER_ARGS = [
        "--disable-blink-features=AutomationControlled",
        "--no-first-run", "--no-default-browser-check",
        "--disable-sync", "--no-sandbox",
    ]

    TEMP_PROFILE.mkdir(parents=True, exist_ok=True)
    (TEMP_PROFILE / "Default").mkdir(exist_ok=True)
    for f in ["Local State", "Default/Cookies", "Default/Preferences", "Default/Login Data"]:
        src, dst = CHROME_USER_DATA / f, TEMP_PROFILE / f
        if src.exists():
            try:
                shutil.copy2(src, dst)
            except Exception:
                pass
    log_cb("Chrome 프로필 복사 완료", "info")

    def open_save_panel(page):
        page.evaluate("window.scrollTo(0, 250)")
        time.sleep(1.0)
        for sel in [
            'button[aria-label*="저장"]',
            'button[aria-label*="Save to playlist"]',
            'button[aria-label*="재생목록에 저장"]',
        ]:
            try:
                el = page.locator(sel).filter(visible=True).first
                if el.is_visible(timeout=2000):
                    el.click()
                    time.sleep(1.5)
                    return
            except PWTimeout:
                pass
        more_btn = page.locator(
            'button[aria-label="추가 작업"], button[aria-label="More actions"]'
        ).filter(visible=True).first
        more_btn.wait_for(timeout=10000)
        more_btn.click()
        time.sleep(1.0)
        menu_save = page.locator(
            'ytd-menu-service-item-renderer, yt-list-item-view-model'
        ).filter(has_text="저장").first
        menu_save.wait_for(timeout=5000)
        menu_save.click()
        time.sleep(1.5)

    def add_to_playlist(page, title):
        open_save_panel(page)
        items = page.locator("yt-list-item-view-model")
        items.first.wait_for(timeout=10000)
        for i in range(items.count()):
            label = items.nth(i).text_content() or ""
            if title in label.strip():
                items.nth(i).click()
                time.sleep(0.8)
                try:
                    page.keyboard.press("Escape")
                except Exception:
                    pass
                return
        raise RuntimeError(f'"{title}" 플레이리스트를 목록에서 찾을 수 없음')

    def go_to_video(page, query):
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.locator("ytd-video-renderer a#video-title").first.click()
        page.wait_for_url("**/watch**", timeout=15000)
        time.sleep(3.5)

    YT_EMAIL    = os.environ.get("YT_EMAIL", "")
    YT_PASSWORD = os.environ.get("YT_PASSWORD", "")

    def auto_login(page):
        log_cb("로그인 시도 중...", "info")
        page.goto(
            "https://accounts.google.com/signin/v2/identifier?service=youtube&hl=ko",
            wait_until="domcontentloaded", timeout=30000,
        )
        time.sleep(1.5)
        email_input = page.locator('input[type="email"]')
        email_input.wait_for(timeout=10000)
        email_input.fill(YT_EMAIL)
        page.keyboard.press("Enter")
        time.sleep(2.0)
        pw_input = page.locator('input[type="password"]')
        pw_input.wait_for(timeout=10000)
        pw_input.fill(YT_PASSWORD)
        page.keyboard.press("Enter")
        time.sleep(3.0)
        page.goto("https://www.youtube.com", wait_until="domcontentloaded", timeout=30000)
        time.sleep(2.0)
        page.wait_for_selector("#avatar-btn, button[aria-label*='계정']", timeout=15000)
        log_cb("자동 로그인 성공 ✓", "success")

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            str(TEMP_PROFILE),
            channel="chrome", headless=False, args=BROWSER_ARGS,
            ignore_https_errors=True, bypass_csp=True,
            locale="ko-KR", viewport={"width": 1280, "height": 800},
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://www.youtube.com", wait_until="domcontentloaded")

        try:
            page.wait_for_selector("#avatar-btn, button[aria-label*='계정']", timeout=8000)
            log_cb("YouTube 로그인 확인됨 ✓", "success")
        except PWTimeout:
            log_cb("로그인 세션 없음 — 자동 로그인 시작", "info")
            try:
                auto_login(page)
            except Exception as e:
                log_cb(f"자동 로그인 실패: {e}\nChrome 창에서 직접 로그인 후 30초 대기", "fail")
                time.sleep(30)

        state["start_time"] = time.time()
        log_cb(f'플레이리스트 추가 시작: "{PLAYLIST_TITLE}" — 총 {TOTAL}곡', "info")

        for i, song in enumerate(SONGS):
            if state["stop_flag"]:
                log_cb("⏹ 사용자가 중단했습니다.", "fail")
                break

            state["current"] = i + 1
            stat_cb(i, "active")
            log_cb(f"[{i+1}/{TOTAL}] 🔍 {song}", "info")
            t0 = time.time()
            try:
                go_to_video(page, song)
                add_to_playlist(page, PLAYLIST_TITLE)
                elapsed = round(time.time() - t0, 1)
                state["success"] += 1
                state["results"].append((i + 1, song, "success", elapsed, ""))
                stat_cb(i, "success")
                log_cb(f"  ✅ 추가됨  ({elapsed}s)", "success")
            except Exception as e:
                elapsed = round(time.time() - t0, 1)
                err_msg = str(e).splitlines()[0]
                state["fail"] += 1
                state["results"].append((i + 1, song, "fail", elapsed, err_msg))
                stat_cb(i, "fail")
                log_cb(f"  ❌ 실패: {err_msg}", "fail")

            time.sleep(1.5 + random.random() * 1.2)

        try:
            context.close()
        except Exception:
            pass
    done_cb()


# ══════════════════════════════════════════════════════════════
#  메인 앱
# ══════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("✨ Disney OST Playlist — 대시보드")
        self.configure(bg=C["bg"])
        self.geometry("1020x860")
        self.minsize(860, 720)
        self._auto_job = None
        self.rows: list[SongRow] = []
        self._build_ui()

    # ── UI ────────────────────────────────────────────────────
    def _build_ui(self):
        self._build_header()
        self._build_stats()
        self._build_progress()
        self._build_controls()   # 버튼을 곡 목록 위에 배치
        self._build_song_list()  # 곡 목록은 컨트롤 아래
        self._build_log()

    def _build_header(self):
        hf = tk.Frame(self, bg=C["bg"], pady=14)
        hf.pack(fill="x", padx=24)

        tk.Label(hf, text="✨  Disney OST Playlist",
                 font=("Segoe UI", 20, "bold"),
                 bg=C["bg"], fg=C["gold"]).pack(side="left")
        tk.Label(hf, text=f"총 {TOTAL}곡",
                 font=("Segoe UI", 11),
                 bg=C["bg"], fg=C["muted"]).pack(side="left", padx=16)

        self.lbl_time = tk.Label(hf, text="00:00",
                                 font=("Courier New", 13, "bold"),
                                 bg=C["bg"], fg=C["accent2"])
        self.lbl_time.pack(side="right")
        tk.Label(hf, text="경과  ",
                 font=("Segoe UI", 9),
                 bg=C["bg"], fg=C["muted"]).pack(side="right")

    def _build_stats(self):
        sf = tk.Frame(self, bg=C["bg"])
        sf.pack(fill="x", padx=24, pady=(0, 8))

        cards = [
            ("✅ 성공",  "lbl_success", C["success"]),
            ("❌ 실패",  "lbl_fail",    C["fail"]),
            ("▶ 진행",  "lbl_cur",     C["accent2"]),
            ("📋 남은곡", "lbl_remain",  C["muted"]),
        ]
        for text, attr, color in cards:
            card = tk.Frame(sf, bg=C["card"], padx=22, pady=10,
                            highlightthickness=1, highlightbackground=C["border"])
            card.pack(side="left", padx=5)
            tk.Label(card, text=text, font=("Segoe UI", 8),
                     bg=C["card"], fg=C["muted"]).pack()
            lbl = tk.Label(card, text="0", font=("Segoe UI", 24, "bold"),
                           bg=C["card"], fg=color)
            lbl.pack()
            setattr(self, attr, lbl)

    def _build_progress(self):
        pf = tk.Frame(self, bg=C["bg"], padx=24, pady=2)
        pf.pack(fill="x")

        self.lbl_cur_song = tk.Label(pf, text="대기 중...",
                                     font=("Segoe UI", 9, "italic"),
                                     bg=C["bg"], fg=C["muted"], anchor="w")
        self.lbl_cur_song.pack(fill="x", pady=(0, 3))

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Disney.Horizontal.TProgressbar",
                        troughcolor=C["card"],
                        background=C["accent"],
                        bordercolor=C["border"],
                        lightcolor=C["accent"],
                        darkcolor=C["accent"])
        self.pbar = ttk.Progressbar(pf, style="Disney.Horizontal.TProgressbar",
                                    maximum=TOTAL, mode="determinate")
        self.pbar.pack(fill="x")

        self.lbl_pct = tk.Label(pf, text=f"0 / {TOTAL}  (0%)",
                                font=("Segoe UI", 8),
                                bg=C["bg"], fg=C["muted"], anchor="e")
        self.lbl_pct.pack(fill="x")

    def _build_song_list(self):
        outer = tk.Frame(self, bg=C["bg"])
        outer.pack(fill="both", expand=True, padx=20, pady=(0, 4))

        header = tk.Frame(outer, bg=C["bg"])
        header.pack(fill="x", padx=2, pady=(4, 4))
        tk.Label(header, text="  #", font=("Segoe UI", 8, "bold"),
                 bg=C["bg"], fg=C["muted"], width=4, anchor="w").pack(side="left")
        tk.Label(header, text="상태", font=("Segoe UI", 8, "bold"),
                 bg=C["bg"], fg=C["muted"], width=4, anchor="center").pack(side="left", padx=(4, 8))
        tk.Label(header, text="곡 제목", font=("Segoe UI", 8, "bold"),
                 bg=C["bg"], fg=C["muted"], anchor="w").pack(side="left", fill="x", expand=True)
        tk.Label(header, text="진행", font=("Segoe UI", 8, "bold"),
                 bg=C["bg"], fg=C["muted"], width=6, anchor="e").pack(side="right")

        tk.Frame(outer, bg=C["border"], height=1).pack(fill="x", padx=2, pady=(0, 4))

        # 스크롤 가능한 캔버스
        canvas = tk.Canvas(outer, bg=C["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=C["bg"])

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # 마우스 휠 스크롤
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        for i, song in enumerate(SONGS):
            row = SongRow(scroll_frame, number=i + 1, song=song)
            row.pack(fill="x", padx=2, pady=2)
            self.rows.append(row)

    def _build_log(self):
        lf = tk.Frame(self, bg=C["panel"], padx=12, pady=8,
                      highlightthickness=1, highlightbackground=C["border"])
        lf.pack(fill="both", expand=True, padx=24, pady=(4, 4))

        tk.Label(lf, text="실행 로그",
                 font=("Segoe UI", 9, "bold"),
                 bg=C["panel"], fg=C["muted"]).pack(anchor="w")

        self.log_box = scrolledtext.ScrolledText(
            lf, font=("Consolas", 9),
            bg="#080815", fg=C["text"],
            insertbackground=C["text"],
            bd=0, relief="flat", wrap="word",
            state="disabled", height=8,
        )
        self.log_box.pack(fill="both", expand=True, pady=(4, 0))
        self.log_box.tag_config("info",    foreground=C["text"])
        self.log_box.tag_config("success", foreground=C["success"])
        self.log_box.tag_config("fail",    foreground=C["fail"])
        self.log_box.tag_config("ts",      foreground="#2a3558")

    def _build_controls(self):
        cf = tk.Frame(self, bg=C["bg"], padx=24, pady=10)
        cf.pack(fill="x")

        btn = dict(font=("Segoe UI", 10, "bold"), relief="flat",
                   cursor="hand2", padx=18, pady=8, bd=0)

        self.btn_start = tk.Button(cf, text="▶  자동화 시작",
                                   bg=C["accent"], fg=C["white"],
                                   activebackground=C["accent2"],
                                   activeforeground=C["white"],
                                   command=self._start, **btn)
        self.btn_start.pack(side="left", padx=(0, 8))

        self.btn_stop = tk.Button(cf, text="⏹  중단",
                                  bg=C["card"], fg=C["fail"],
                                  activebackground="#2a2a50",
                                  activeforeground=C["fail"],
                                  command=self._stop, state="disabled", **btn)
        self.btn_stop.pack(side="left", padx=(0, 8))

        tk.Button(cf, text="💾  결과 저장",
                  bg=C["card"], fg=C["text"],
                  activebackground="#2a2a50", activeforeground=C["white"],
                  command=self._save_results, **btn).pack(side="left", padx=(0, 8))

        tk.Button(cf, text="🔄  초기화",
                  bg=C["card"], fg=C["muted"],
                  activebackground="#2a2a50", activeforeground=C["white"],
                  command=self._reset, **btn).pack(side="left", padx=(0, 8))

        self.auto_var = tk.BooleanVar(value=False)
        tk.Checkbutton(cf, text="2초 자동 새로고침",
                       variable=self.auto_var,
                       bg=C["bg"], fg=C["muted"],
                       activebackground=C["bg"], selectcolor=C["card"],
                       font=("Segoe UI", 9),
                       command=self._toggle_auto).pack(side="left", padx=12)

    # ── 이벤트 ───────────────────────────────────────────────
    def _start(self):
        if state["running"]:
            return
        state.update(running=True, stop_flag=False,
                     success=0, fail=0, current=0,
                     results=[], start_time=time.time())
        self.pbar["value"] = 0
        for card in self.rows:
            card.set_status("waiting")
        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")
        self._log("═" * 54, "ts")
        self._log(f"  자동화 시작  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "info")
        self._log("═" * 54, "ts")
        self._tick()
        threading.Thread(
            target=run_automation,
            args=(self._log, self._on_card_update, self._done),
            daemon=True,
        ).start()

    def _stop(self):
        state["stop_flag"] = True
        self._log("⏹ 중단 요청 — 현재 곡 완료 후 정지합니다.", "fail")
        self.btn_stop.config(state="disabled")

    def _done(self):
        state["running"] = False
        self.after(0, lambda: self.btn_start.config(state="normal"))
        self.after(0, lambda: self.btn_stop.config(state="disabled"))
        self._refresh_stats()
        total_sec = int(time.time() - (state["start_time"] or time.time()))
        m, s = divmod(total_sec, 60)
        self._log("═" * 54, "ts")
        self._log(
            f"  완료  ✅ {state['success']}곡  ❌ {state['fail']}곡  ⏱ {m:02d}:{s:02d}",
            "success",
        )
        self._log("═" * 54, "ts")

    def _on_card_update(self, song_index: int, status: str):
        """자동화 스레드에서 호출 — 카드 상태 + 통계 갱신"""
        def _update():
            if song_index < len(self.rows):
                self.rows[song_index].set_status(status, master=self)
            self._refresh_stats()
            if status == "active" and song_index < len(SONGS):
                self.lbl_cur_song.config(text=f"▶  지금 처리 중: {SONGS[song_index]}")
        self.after(0, _update)

    def _refresh_stats(self):
        def _update():
            done   = state["success"] + state["fail"]
            remain = TOTAL - done
            pct    = int(done / TOTAL * 100)
            self.lbl_success.config(text=str(state["success"]))
            self.lbl_fail.config(text=str(state["fail"]))
            self.lbl_cur.config(text=str(state["current"]))
            self.lbl_remain.config(text=str(remain))
            self.pbar["value"] = done
            self.lbl_pct.config(text=f"{done} / {TOTAL}  ({pct}%)")
        self.after(0, _update)

    def _tick(self):
        if not state["running"]:
            return
        elapsed = int(time.time() - (state["start_time"] or time.time()))
        m, s = divmod(elapsed, 60)
        self.lbl_time.config(text=f"{m:02d}:{s:02d}")
        self.after(1000, self._tick)

    def _log(self, msg: str, tag: str = "info"):
        def _write():
            ts = datetime.now().strftime("%H:%M:%S")
            self.log_box.config(state="normal")
            self.log_box.insert("end", f"[{ts}] ", "ts")
            self.log_box.insert("end", msg + "\n", tag)
            self.log_box.see("end")
            self.log_box.config(state="disabled")
        self.after(0, _write)

    def _toggle_auto(self):
        if self.auto_var.get():
            self._auto_refresh()
        elif self._auto_job:
            self.after_cancel(self._auto_job)
            self._auto_job = None

    def _auto_refresh(self):
        if not self.auto_var.get():
            return
        self._refresh_stats()
        self._auto_job = self.after(2000, self._auto_refresh)

    def _reset(self):
        if state["running"]:
            messagebox.showwarning("실행 중", "자동화 실행 중에는 초기화할 수 없습니다.")
            return
        state.update(success=0, fail=0, current=0, results=[], start_time=None)
        self.pbar["value"] = 0
        self.lbl_cur_song.config(text="대기 중...")
        self.lbl_time.config(text="00:00")
        self._refresh_stats()
        for card in self.rows:
            card.set_status("waiting")
        self.log_box.config(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.config(state="disabled")

    # ── 결과 저장 ─────────────────────────────────────────────
    def _save_results(self):
        if not state["results"]:
            messagebox.showinfo("저장", "저장할 결과가 없습니다.")
            return
        fmt = messagebox.askquestion("저장 형식",
                                     "HTML 형식으로 저장할까요?\n(아니오 → TXT / JSON)")
        if fmt == "yes":
            self._save_html()
        else:
            if messagebox.askquestion("형식", "TXT로 저장할까요?\n(아니오 → JSON)") == "yes":
                self._save_txt()
            else:
                self._save_json()

    def _save_html(self):
        rows = ""
        for idx, song, st, elapsed, reason in state["results"]:
            color = C["success"] if st == "success" else C["fail"]
            icon  = "✅ 완료" if st == "success" else "❌ 실패"
            reason_cell = f'<span style="color:#ff6b6b;font-size:0.85em">{reason}</span>' if reason else ""
            rows += (
                f'<tr>'
                f'<td>{idx}</td>'
                f'<td>{song}</td>'
                f'<td style="color:{color}">{icon}</td>'
                f'<td>{elapsed}s</td>'
                f'<td>{reason_cell}</td>'
                f'</tr>\n'
            )
        html = f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8">
<title>Disney OST 결과</title>
<style>
  body{{background:#0a0a1a;color:#e8eaf6;font-family:'Segoe UI',sans-serif;padding:32px}}
  h1{{color:#ffd700}} p{{color:#7788aa}}
  table{{border-collapse:collapse;width:100%}}
  th{{background:#1c1c35;padding:10px 16px;text-align:left;color:#7788aa}}
  td{{padding:9px 16px;border-bottom:1px solid #2a2a50;vertical-align:top}}
  tr:hover td{{background:#12122a}}
  .fail-reason{{color:#ff6b6b;font-size:0.85em;margin-top:4px}}
</style></head><body>
<h1>✨ Disney OST Playlist 자동화 결과</h1>
<p>✅ {state['success']}곡 완료 / ❌ {state['fail']}곡 실패 — {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
<table><tr><th>#</th><th>곡</th><th>결과</th><th>소요시간</th><th>실패 사유</th></tr>
{rows}</table></body></html>"""
        path = filedialog.asksaveasfilename(
            defaultextension=".html", filetypes=[("HTML", "*.html")],
            initialfile="disney_ost_result.html",
        )
        if path:
            Path(path).write_text(html, encoding="utf-8")
            messagebox.showinfo("저장 완료", f"HTML 저장:\n{path}")

    def _save_txt(self):
        lines = [
            "Disney OST Playlist 자동화 결과",
            f"✅ {state['success']} / ❌ {state['fail']} — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            *[f"{idx:>3}. {'✅' if st=='success' else '❌'}  {song}  ({elapsed}s)"
              + (f"\n       사유: {reason}" if reason else "")
              for idx, song, st, elapsed, reason in state["results"]],
        ]
        path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("TXT", "*.txt")],
            initialfile="disney_ost_result.txt",
        )
        if path:
            Path(path).write_text("\n".join(lines), encoding="utf-8")
            messagebox.showinfo("저장 완료", f"TXT 저장:\n{path}")

    def _save_json(self):
        data = {
            "playlist": PLAYLIST_TITLE,
            "date": datetime.now().isoformat(),
            "success": state["success"],
            "fail": state["fail"],
            "results": [
                {"index": i, "song": s, "status": st, "elapsed": e, "reason": r}
                for i, s, st, e, r in state["results"]
            ],
        }
        path = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON", "*.json")],
            initialfile="disney_ost_result.json",
        )
        if path:
            Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            messagebox.showinfo("저장 완료", f"JSON 저장:\n{path}")


# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()
