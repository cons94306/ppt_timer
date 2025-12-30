import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser, filedialog
from tkinter import ttk
import configparser
import os
import time
import ctypes
import keyboard
from screeninfo import get_monitors
import threading

CONFIG_FILE = "timer_config.ini"
LANG_FILE = "language.ini"

# --- 預設 Config 內容 (當 timer_config.ini 不存在時使用) ---
DEFAULT_CONFIG_CONTENT = """[Main]
duration = 1200
ahead = 60
fontface = Calibri
fontweight = bold
fontsize = 54
width = 240
height = 70
margin = 24
position = RT
opacity = 230
backgroundcolor = #FFFFFF
textcolor = #000000
aheadcolor = #000000
timeoutcolor = #F87171
playwarningsound = 0
playfinishsound = 0
stopresetstimer = 0
sendontimeout = 0
warningsoundfile = 
finishsoundfile = 

[shortcuts]
startkey = F9
pausekey = F10
resetkey = F12
quitkey = Ctrl+Shift+K

[Profile_1]
name = 10分鐘
duration = 600

[Profile_2]
name = 5分鐘
duration = 300

[Status]
lastprofile = 0
lastmonitor = 0
lastposition = TR
"""

# --- 預設語言檔內容 ---
DEFAULT_LANG_CONTENT = """[zh_TW]
name = 繁體中文
start = 開始
pause = 暫停
reset = 重置
custom_time = 自訂時間 (分鐘)...
settings = 設定...
reload = 重新讀取設定
quit = 離開
position = 位置
pos_tl = ↖ 左上 (TL)
pos_tr = ↗ 右上 (TR)
pos_bl = ↙ 左下 (BL)
pos_br = ↘ 右下 (BR)
profile_main = Main (預設)
input_profile_name = 請輸入設定檔名稱 (例如: 5分鐘演講):
confirm_delete = 確定要刪除設定檔 [{}] 嗎？
cannot_delete_main = 不能刪除預設的 Main 設定檔。
saved_success = 設定已儲存！
save_error = 儲存失敗: {}
tab_general = 一般
tab_appearance = 外觀
tab_alert = 警示
tab_hotkey = 快捷鍵
tab_language = 語言
lbl_lang_select = 選擇語言 (Select Language)
lbl_lang_note = * 修改後請點擊儲存，介面將自動更新。
lbl_profile_name = 設定檔名稱
lbl_duration = 時間長度 (秒)
lbl_width = 視窗寬度
lbl_height = 視窗高度
lbl_opacity = 透明度 (0-255)
lbl_margin = 邊緣距離
lbl_fontsize = 字體大小
lbl_fontface = 字體名稱
lbl_fontweight = 字體粗細 (bold/normal)
lbl_color_settings = --- 顏色設定 ---
lbl_bg_color = 背景顏色
lbl_text_color = 文字顏色
lbl_ahead = 倒數前警告 (秒)
lbl_ahead_color = 警告文字顏色
lbl_timeout_color = 時間到文字顏色
lbl_sound_action = --- 音效與動作 ---
lbl_play_warn = 播放警告音效
lbl_warn_file = 警告音效檔
lbl_play_finish = 播放結束音效
lbl_finish_file = 結束音效檔
lbl_key_start = 開始計時
lbl_key_pause = 暫停計時
lbl_key_reset = 重置計時
lbl_key_quit = 關閉程式
btn_add = ➕ 新增
btn_del = ➖ 刪除
btn_save = 儲存全部並套用
btn_cancel = 取消
btn_pick_color = 選色
editor_title = 設定編輯器

[en_US]
name = English
start = Start
pause = Pause
reset = Reset
custom_time = Custom Time (min)...
settings = Settings...
reload = Reload Config
quit = Quit
position = Position
pos_tl = ↖ Top-Left (TL)
pos_tr = ↗ Top-Right (TR)
pos_bl = ↙ Bot-Left (BL)
pos_br = ↘ Bot-Right (BR)
profile_main = Main (Default)
input_profile_name = Enter Profile Name:
confirm_delete = Delete profile [{}]?
cannot_delete_main = Cannot delete Main profile.
saved_success = Settings Saved!
save_error = Error: {}
tab_general = General
tab_appearance = Appearance
tab_alert = Alerts
tab_hotkey = Hotkeys
tab_language = Language
lbl_lang_select = Select Language
lbl_lang_note = * Save to apply language changes.
lbl_profile_name = Profile Name
lbl_duration = Duration (sec)
lbl_width = Width
lbl_height = Height
lbl_opacity = Opacity (0-255)
lbl_margin = Margin
lbl_fontsize = Font Size
lbl_fontface = Font Family
lbl_fontweight = Font Weight
lbl_color_settings = --- Colors ---
lbl_bg_color = Background
lbl_text_color = Text Color
lbl_ahead = Warning Time (sec)
lbl_ahead_color = Warning Color
lbl_timeout_color = Timeout Color
lbl_sound_action = --- Sound & Actions ---
lbl_play_warn = Play Warning Sound
lbl_warn_file = Warning File
lbl_play_finish = Play Finish Sound
lbl_finish_file = Finish File
lbl_key_start = Start Key
lbl_key_pause = Pause Key
lbl_key_reset = Reset Key
lbl_key_quit = Quit Key
btn_add = ➕ Add
btn_del = ➖ Del
btn_save = Save & Apply
btn_cancel = Cancel
btn_pick_color = Pick
editor_title = Settings Editor
"""

class LanguageHelper:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.current_lang = "zh_TW"
        self.load_languages()

    def load_languages(self):
        if not os.path.exists(LANG_FILE):
            try:
                with open(LANG_FILE, "w", encoding="utf-8") as f:
                    f.write(DEFAULT_LANG_CONTENT)
            except: pass
        
        try:
            self.config.read(LANG_FILE, encoding="utf-8")
        except:
            self.config.read(LANG_FILE)

    def set_language(self, lang_code):
        self.current_lang = lang_code

    def get(self, key):
        val = self.config.get(self.current_lang, key, fallback=None)
        if val is None:
            val = self.config.get("zh_TW", key, fallback=key)
        return val

    def get_available_languages(self):
        langs = []
        for section in self.config.sections():
            name = self.config.get(section, "name", fallback=section)
            langs.append((section, name))
        return langs

class SoundPlayer:
    @staticmethod
    def play(filepath):
        if not filepath or not os.path.exists(filepath):
            return
        alias = "timer_sound"
        try:
            ctypes.windll.winmm.mciSendStringW(f"close {alias}", None, 0, 0)
            cmd_open = f'open "{filepath}" type mpegvideo alias {alias}'
            cmd_play = f'play {alias}'
            ctypes.windll.winmm.mciSendStringW(cmd_open, None, 0, 0)
            ctypes.windll.winmm.mciSendStringW(cmd_play, None, 0, 0)
        except Exception as e:
            print(f"Sound Error: {e}")

    @staticmethod
    def stop():
        try:
            ctypes.windll.winmm.mciSendStringW("close timer_sound", None, 0, 0)
        except:
            pass

class SettingsEditor(tk.Toplevel):
    def __init__(self, parent, config, current_profile_section, lang_helper):
        super().__init__(parent.root)
        self.parent = parent
        self.config = config
        self.editing_section = current_profile_section
        self.lang = lang_helper
        
        self.title(self.lang.get("editor_title"))
        self.geometry("520x620")
        
        self.ui_vars = {} 
        
        self.attributes('-topmost', True)
        self.grab_set()
        
        self.setup_ui()
        self.load_section_to_ui(self.editing_section)

    def setup_ui(self):
        top_frame = tk.Frame(self, bg="#dddddd", pady=5)
        top_frame.pack(fill='x')

        self.profile_combo = ttk.Combobox(top_frame, state="readonly", width=25)
        self.profile_combo.pack(side='left', padx=10)
        self.profile_combo.bind("<<ComboboxSelected>>", self.on_profile_change)
        
        self.refresh_profile_list()

        tk.Button(top_frame, text=self.lang.get("btn_add"), command=self.add_profile, width=6).pack(side='left', padx=2)
        tk.Button(top_frame, text=self.lang.get("btn_del"), command=self.delete_profile, width=6).pack(side='left', padx=2)

        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.create_general_tab(notebook)
        self.create_appearance_tab(notebook)
        self.create_alert_tab(notebook)
        self.create_hotkey_tab(notebook)
        self.create_language_tab(notebook)

        btn_frame = tk.Frame(self)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(btn_frame, text=self.lang.get("btn_save"), command=self.save_and_close, bg="#4CAF50", fg="white", width=15).pack(side='right', padx=5)
        tk.Button(btn_frame, text=self.lang.get("btn_cancel"), command=self.destroy, width=10).pack(side='right', padx=5)

    def refresh_profile_list(self):
        values = ["Main"]
        profiles = [s for s in self.config.sections() if s.startswith("Profile_")]
        profiles.sort(key=lambda x: int(x.split('_')[1]) if '_' in x else 0)
        
        display_values = []
        self.section_map = {}

        main_name = self.lang.get("profile_main")
        display_values.append(main_name)
        self.section_map[main_name] = "Main"

        for p in profiles:
            name = self.config.get(p, "name", fallback=p)
            display_str = f"{name} ({p})"
            display_values.append(display_str)
            self.section_map[display_str] = p

        self.profile_combo['values'] = display_values
        
        current_display = next((k for k, v in self.section_map.items() if v == self.editing_section), main_name)
        self.profile_combo.set(current_display)

    def on_profile_change(self, event):
        display_name = self.profile_combo.get()
        new_section = self.section_map.get(display_name, "Main")
        
        if new_section == self.editing_section:
            return

        self.save_ui_to_virtual_config()
        self.editing_section = new_section
        self.load_section_to_ui(self.editing_section)

    def add_profile(self):
        self.save_ui_to_virtual_config()
        name = simpledialog.askstring("New Profile", self.lang.get("input_profile_name"), parent=self)
        if not name: return

        idx = 1
        while True:
            candidate = f"Profile_{idx}"
            if not self.config.has_section(candidate):
                break
            idx += 1
        
        new_section = f"Profile_{idx}"
        self.config.add_section(new_section)
        
        for key, value in self.config.items("Main"):
            if key != "name":
                self.config.set(new_section, key, value)
        
        self.config.set(new_section, "name", name)
        self.config.set(new_section, "duration", "300")
        
        self.refresh_profile_list()
        
        display_name = f"{name} ({new_section})"
        self.profile_combo.set(display_name)
        self.editing_section = new_section
        self.load_section_to_ui(new_section)

    def delete_profile(self):
        if self.editing_section == "Main":
            messagebox.showwarning("Warning", self.lang.get("cannot_delete_main"), parent=self)
            return
        
        if not messagebox.askyesno("Confirm", self.lang.get("confirm_delete").format(self.editing_section), parent=self):
            return

        self.config.remove_section(self.editing_section)
        
        self.editing_section = "Main"
        self.refresh_profile_list()
        self.load_section_to_ui("Main")

    def load_section_to_ui(self, section):
        for key, var in self.ui_vars.items():
            if key in ["startKey", "pauseKey", "resetKey", "quitKey"]:
                val = self.config.get("shortcuts", key, fallback="")
                var.set(val)
                continue
            
            if key == "language":
                val = self.config.get("General", "language", fallback="zh_TW")
                langs = self.lang.get_available_languages()
                display = next((name for code, name in langs if code == val), val)
                var.set(display)
                continue

            val = self.config.get(section, key, fallback=None)
            if val is None and section != "Main":
                val = self.config.get("Main", key, fallback="")
            
            if val is None: val = ""
            var.set(val)

    def save_ui_to_virtual_config(self):
        section = self.editing_section
        for key, var in self.ui_vars.items():
            val = str(var.get())
            if key in ["startKey", "pauseKey", "resetKey", "quitKey"]:
                if not self.config.has_section("shortcuts"):
                    self.config.add_section("shortcuts")
                self.config.set("shortcuts", key, val)
            elif key == "language":
                if not self.config.has_section("General"):
                    self.config.add_section("General")
                langs = self.lang.get_available_languages()
                code = next((code for code, name in langs if name == val), "zh_TW")
                self.config.set("General", "language", code)
            else:
                self.config.set(section, key, val)

    def add_entry(self, parent, row, label_text, key):
        tk.Label(parent, text=label_text).grid(row=row, column=0, sticky='w', padx=10, pady=5)
        var = tk.StringVar()
        self.ui_vars[key] = var
        tk.Entry(parent, textvariable=var, width=20).grid(row=row, column=1, padx=10, pady=5)

    def add_scale(self, parent, row, label_text, key, min_val, max_val):
        tk.Label(parent, text=label_text).grid(row=row, column=0, sticky='w', padx=10, pady=5)
        proxy_var = tk.IntVar()
        def on_scale_change(*args):
            self.ui_vars[key].set(str(proxy_var.get()))
        proxy_var.trace("w", on_scale_change)
        self.ui_vars[key] = tk.StringVar()
        def on_str_change(*args):
            try: proxy_var.set(int(float(self.ui_vars[key].get())))
            except: proxy_var.set(max_val)
        self.ui_vars[key].trace("w", on_str_change)
        tk.Scale(parent, from_=min_val, to=max_val, orient='horizontal', variable=proxy_var).grid(row=row, column=1, sticky='ew', padx=10)

    def add_checkbox(self, parent, row, label_text, key):
        var = tk.StringVar()
        self.ui_vars[key] = var
        tk.Checkbutton(parent, text=label_text, variable=var, onvalue="1", offvalue="0").grid(row=row, column=0, columnspan=2, sticky='w', padx=10, pady=2)

    def add_color_picker(self, parent, row, label_text, key):
        tk.Label(parent, text=label_text).grid(row=row, column=0, sticky='w', padx=10, pady=5)
        var = tk.StringVar()
        self.ui_vars[key] = var
        frame = tk.Frame(parent)
        frame.grid(row=row, column=1, sticky='w', padx=10)
        entry = tk.Entry(frame, textvariable=var, width=10)
        entry.pack(side='left')
        btn = tk.Button(frame, text=self.lang.get("btn_pick_color"), width=5)
        def update_btn_color(*args):
            c = var.get()
            if not c.startswith("#") and len(c) == 6: c = "#" + c
            try: btn.config(bg=c)
            except: pass
        var.trace("w", update_btn_color)
        def pick_color():
            current = var.get()
            if not current.startswith("#"): current = "#" + current
            color = colorchooser.askcolor(initialcolor=current, parent=self)
            if color[1]: var.set(color[1])
        btn.config(command=pick_color)
        btn.pack(side='left', padx=5)

    def add_file_picker(self, parent, row, label_text, key):
        tk.Label(parent, text=label_text).grid(row=row, column=0, sticky='w', padx=10, pady=5)
        var = tk.StringVar()
        self.ui_vars[key] = var
        frame = tk.Frame(parent)
        frame.grid(row=row, column=1, sticky='ew', padx=10)
        entry = tk.Entry(frame, textvariable=var, width=15)
        entry.pack(side='left', fill='x', expand=True)
        def pick_file():
            filename = filedialog.askopenfilename(parent=self, filetypes=[("Audio Files", "*.mp3 *.wav *.mid")])
            if filename: var.set(filename)
        tk.Button(frame, text="...", command=pick_file, width=3).pack(side='right')
    
    def add_combo(self, parent, row, label_text, key, values):
        tk.Label(parent, text=label_text).grid(row=row, column=0, sticky='w', padx=10, pady=5)
        var = tk.StringVar()
        self.ui_vars[key] = var
        cb = ttk.Combobox(parent, textvariable=var, values=values, state="readonly", width=18)
        cb.grid(row=row, column=1, padx=10, pady=5)

    def create_general_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=self.lang.get("tab_general"))
        self.add_entry(frame, 1, self.lang.get("lbl_profile_name"), "name")
        self.add_entry(frame, 2, self.lang.get("lbl_duration"), "Duration")
        self.add_entry(frame, 3, self.lang.get("lbl_width"), "width")
        self.add_entry(frame, 4, self.lang.get("lbl_height"), "height")
        self.add_scale(frame, 5, self.lang.get("lbl_opacity"), "opacity", 50, 255)
        self.add_entry(frame, 6, self.lang.get("lbl_margin"), "margin")

    def create_appearance_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=self.lang.get("tab_appearance"))
        self.add_entry(frame, 0, self.lang.get("lbl_fontsize"), "fontsize")
        self.add_entry(frame, 1, self.lang.get("lbl_fontface"), "fontface")
        self.add_entry(frame, 2, self.lang.get("lbl_fontweight"), "fontweight")
        tk.Label(frame, text=self.lang.get("lbl_color_settings")).grid(row=3, column=0, columnspan=3, pady=10)
        self.add_color_picker(frame, 4, self.lang.get("lbl_bg_color"), "backgroundColor")
        self.add_color_picker(frame, 5, self.lang.get("lbl_text_color"), "textcolor")

    def create_alert_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=self.lang.get("tab_alert"))
        self.add_entry(frame, 0, self.lang.get("lbl_ahead"), "Ahead")
        self.add_color_picker(frame, 1, self.lang.get("lbl_ahead_color"), "AheadColor")
        self.add_color_picker(frame, 2, self.lang.get("lbl_timeout_color"), "timeoutColor")
        tk.Label(frame, text=self.lang.get("lbl_sound_action")).grid(row=3, column=0, columnspan=3, pady=10)
        self.add_checkbox(frame, 4, self.lang.get("lbl_play_warn"), "PlayWarningSound")
        self.add_file_picker(frame, 5, self.lang.get("lbl_warn_file"), "WarningSoundFile")
        self.add_checkbox(frame, 6, self.lang.get("lbl_play_finish"), "PlayFinishSound")
        self.add_file_picker(frame, 7, self.lang.get("lbl_finish_file"), "FinishSoundFile")

    def create_hotkey_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=self.lang.get("tab_hotkey"))
        self.add_entry(frame, 0, self.lang.get("lbl_key_start"), "startKey")
        self.add_entry(frame, 1, self.lang.get("lbl_key_pause"), "pauseKey")
        self.add_entry(frame, 2, self.lang.get("lbl_key_reset"), "resetKey")
        self.add_entry(frame, 3, self.lang.get("lbl_key_quit"), "quitKey")

    def create_language_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=self.lang.get("tab_language"))
        langs = self.lang.get_available_languages()
        lang_names = [name for code, name in langs]
        self.add_combo(frame, 0, self.lang.get("lbl_lang_select"), "language", lang_names)
        tk.Label(frame, text=self.lang.get("lbl_lang_note"), fg="gray").grid(row=1, column=0, columnspan=2, padx=10, pady=20)

    def save_and_close(self):
        self.save_ui_to_virtual_config()
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                self.config.write(f)
            messagebox.showinfo("OK", self.lang.get("saved_success"), parent=self)
            self.parent.reload_config()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", self.lang.get("save_error").format(e), parent=self)

class AdvancedTimer:
    def __init__(self):
        self.root = tk.Tk()
        try:
            if os.path.exists("icon.ico"):
                self.root.iconbitmap("icon.ico")
        except:
            pass
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)

        self.config = configparser.ConfigParser()
        self.lang_helper = LanguageHelper()
        
        self.current_profile = "Main"
        self.monitor_index = 0
        self.state = "STOPPED" 
        self.start_timestamp = 0
        self.target_timestamp = 0
        self.paused_time = 0
        self.duration = 0
        self.warning_triggered = False
        self.finish_triggered = False
        
        self.custom_duration = None 
        self.user_has_moved = False
        self.last_fixed_position = None
        self.manual_x = 0
        self.manual_y = 0

        self.profile_var = tk.StringVar()
        self.position_var = tk.StringVar()

        self.setup_ui()
        self.load_ini()
        
        self.root.bind("<Button-3>", self.show_context_menu)
        self.label.bind("<Button-3>", self.show_context_menu)
        self.hint_label.bind("<Button-3>", self.show_context_menu)
        self.tooltip_label.bind("<Button-3>", self.show_context_menu)
        self.bind_hover_events()
        
        self.profile_var.set(self.current_profile)
        self.update_hint_display()
        self.update_timer()
        
        self.root.after(500, self.register_hotkeys)
        
        self.root.mainloop()

    def load_ini(self):
        if not os.path.exists(CONFIG_FILE):
            self.create_default_ini()
        self.read_config_file()
        
        lang_code = self.config.get("General", "language", fallback="zh_TW")
        self.lang_helper.set_language(lang_code)

        try:
            last_profile_idx = self.config.get('Status', 'lastProfile', fallback="0")
            if last_profile_idx == "0":
                self.current_profile = "Main"
            else:
                self.current_profile = f"Profile_{last_profile_idx}"
                if not self.config.has_section(self.current_profile):
                    self.current_profile = "Main"
        except:
            self.current_profile = "Main"

        try:
            self.monitor_index = int(self.config.get('Status', 'lastMonitor', fallback="0"))
        except:
            self.monitor_index = 0

        last_pos = self.config.get('Status', 'lastPosition', fallback="")
        if "MANUAL" in last_pos:
            self.user_has_moved = True
            self.last_fixed_position = None
            self.position_var.set("MANUAL")
            try:
                coords = last_pos.split(":")[1].split(",")
                self.manual_x = int(coords[0])
                self.manual_y = int(coords[1])
            except:
                self.user_has_moved = False
        elif last_pos in ["TL", "TR", "BL", "BR"]:
            self.user_has_moved = False
            self.last_fixed_position = last_pos
            self.position_var.set(last_pos)
        else:
            self.position_var.set("TR") 

        self.apply_profile(self.current_profile)
        self.reset_timer()

    def reload_config(self):
        SoundPlayer.stop()
        try: keyboard.unhook_all_hotkeys()
        except: pass
        
        self.config = configparser.ConfigParser()
        self.read_config_file()
        
        self.lang_helper.load_languages()
        lang_code = self.config.get("General", "language", fallback="zh_TW")
        self.lang_helper.set_language(lang_code)

        target_profile = self.current_profile
        if not self.config.has_section(target_profile) and target_profile != "Main":
            target_profile = "Main"
        
        self.root.after(10, lambda: self._perform_profile_change(target_profile))
        self.root.after(500, self.register_hotkeys)

    def read_config_file(self):
        try: self.config.read(CONFIG_FILE, encoding='utf-8')
        except: self.config.read(CONFIG_FILE)

    def get_conf(self, key, section=None, dtype=str):
        sect = section if section else self.current_profile
        val = None
        if self.config.has_section(sect):
            val = self.config.get(sect, key, fallback=None)
        if val is None and self.config.has_section("Main"):
            val = self.config.get("Main", key, fallback=None)
        
        if val is None:
            defaults = {
                'Duration': 1200, 'opacity': 220, 'width': 220, 'height': 70, 
                'fontsize': 48, 'fontface': 'Calibri', 'fontweight': 'bold',
                'backgroundColor': '1E1E1E', 'textcolor': 'E0E0E0',
                'AheadColor': 'FCD34D', 'timeoutColor': 'EF4444',
                'margin': 0, 'position': 'RT', 'Ahead': 60,
                'PlayWarningSound': 0, 'PlayFinishSound': 0,
                'stopResetsTimer': 0, 'sendOnTimeout': 0
            }
            val = defaults.get(key, 0)

        try:
            if dtype == int: return int(val)
            elif dtype == bool: return str(val) == "1"
            return str(val)
        except:
            return 0 if dtype == int else str(val)

    def apply_profile(self, profile_name):
        self.current_profile = profile_name
        self.custom_duration = None 
        
        raw_bg = self.get_conf("backgroundColor")
        bg_color = "#" + raw_bg.replace("#", "") if raw_bg and raw_bg != "0" else "#1E1E1E"
        raw_fg = self.get_conf("textcolor")
        fg_color = "#" + raw_fg.replace("#", "") if raw_fg and raw_fg != "0" else "#E0E0E0"
        
        font_face = self.get_conf("fontface")
        font_size = self.get_conf("fontsize", dtype=int)
        font_weight = self.get_conf("fontweight")
        opacity = self.get_conf("opacity", dtype=int)
        
        try:
            self.root.configure(bg=bg_color)
            if hasattr(self, 'label'):
                self.label.configure(bg=bg_color, fg=fg_color, font=(font_face, font_size, font_weight))
            if hasattr(self, 'hint_label'):
                self.hint_label.configure(bg=bg_color, fg=fg_color, font=("Calibri", 10))
        except tk.TclError:
            pass

        self.root.attributes('-alpha', opacity / 255.0)
        self.update_geometry()
        self.update_hint_display()

    def update_geometry(self):
        w = self.get_conf("width", dtype=int)
        h = self.get_conf("height", dtype=int)
        if w == 0: w = 220
        if h == 0: h = 70
        
        try:
            monitors = get_monitors()
            if not monitors: raise Exception
            if self.monitor_index >= len(monitors): self.monitor_index = 0
            m = monitors[self.monitor_index]
        except:
            class Mock: x, y, width, height = 0, 0, self.root.winfo_screenwidth(), self.root.winfo_screenheight()
            m = Mock()

        x, y = 0, 0
        if self.user_has_moved:
            x = self.manual_x
            y = self.manual_y
        else:
            pos_code = "TR"
            if self.last_fixed_position:
                pos_code = self.last_fixed_position
            else:
                conf_pos = self.get_conf("position")
                if "L" in conf_pos and "T" in conf_pos: pos_code = "TL"
                elif "R" in conf_pos and "T" in conf_pos: pos_code = "TR"
                elif "L" in conf_pos and "B" in conf_pos: pos_code = "BL"
                elif "R" in conf_pos and "B" in conf_pos: pos_code = "BR"

            actual_margin = 0 
            if pos_code == "TL":
                x = m.x + actual_margin
                y = m.y + actual_margin
            elif pos_code == "TR":
                x = m.x + m.width - w - actual_margin
                y = m.y + actual_margin
            elif pos_code == "BL":
                x = m.x + actual_margin
                y = m.y + m.height - h - actual_margin
            elif pos_code == "BR":
                x = m.x + m.width - w - actual_margin
                y = m.y + m.height - h - actual_margin

        self.root.geometry(f"{w}x{h}+{int(x)}+{int(y)}")

    def set_position(self, pos_code):
        self.user_has_moved = False
        self.last_fixed_position = pos_code
        self.position_var.set(pos_code)
        self.save_status("lastPosition", pos_code)
        self.update_geometry()

    def set_custom_time(self):
        minutes = simpledialog.askinteger(self.lang_helper.get("custom_time"), self.lang_helper.get("custom_time"), parent=self.root, minvalue=1, maxvalue=9999)
        if minutes is not None:
            self.custom_duration = minutes * 60
            self.reset_timer()

    def open_settings(self):
        SettingsEditor(self, self.config, self.current_profile, self.lang_helper)

    def setup_ui(self):
        self.label = tk.Label(self.root, text="00:00", cursor="hand2")
        self.label.pack(fill=tk.BOTH, expand=True)
        self.label.bind("<Double-Button-1>", lambda e: self.quit_app())
        self.label.bind("<Button-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)
        self.label.bind("<ButtonRelease-1>", self.stop_move)

        self.hint_label = tk.Label(self.root, text="", anchor="e", justify="right")
        self.hint_label.place(relx=1.0, y=2, x=0, anchor="ne")

        self.tooltip_label = tk.Label(self.root, text="", bg="#222222", fg="#FFFFFF", font=("Microsoft JhengHei UI", 9), padx=5, pady=2)

    def bind_hover_events(self):
        widgets = [self.root, self.label, self.hint_label, self.tooltip_label]
        for w in widgets:
            w.bind("<Enter>", self.show_tooltip)
            w.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        s = "shortcuts"
        start = self.config.get(s, "startKey", fallback="F9").upper()
        pause = self.config.get(s, "pauseKey", fallback="F11").upper()
        reset = self.config.get(s, "resetKey", fallback="F12").upper()
        text = f"► {start}  |  ∥ {pause}  |  ⟳ {reset}"
        self.tooltip_label.config(text=text)
        self.tooltip_label.place(relx=0.5, rely=0.8, anchor="center")
        self.tooltip_label.lift()

    def hide_tooltip(self, event):
        self.tooltip_label.place_forget()

    def update_hint_display(self):
        self.hint_label.config(text="")
        self.hint_label.lift()

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
        self.user_has_moved = True
        self.manual_x = x
        self.manual_y = y

    def stop_move(self, event):
        if self.user_has_moved:
            val = f"MANUAL:{self.root.winfo_x()},{self.root.winfo_y()}"
            self.save_status("lastPosition", val)
            self.position_var.set("MANUAL")

    def start_timer(self):
        if self.state == "RUNNING": return
        if self.state == "STOPPED":
            self.start_timestamp = time.time()
            self.target_timestamp = self.start_timestamp + self.duration
        elif self.state == "PAUSED":
            self.target_timestamp = time.time() + self.paused_time
        self.state = "RUNNING"
        self.warning_triggered = False
        self.finish_triggered = False
        self.update_display_color()

    def pause_timer(self):
        if self.state == "RUNNING":
            self.state = "PAUSED"
            self.paused_time = self.target_timestamp - time.time()

    def reset_timer(self):
        self.state = "STOPPED"
        SoundPlayer.stop() 
        self.warning_triggered = False
        self.finish_triggered = False
        
        if self.custom_duration is not None:
            self.duration = self.custom_duration
        else:
            self.duration = self.get_conf("Duration", dtype=int)
            
        mins, secs = divmod(self.duration, 60)
        self.label.config(text=f"{mins:02d}:{secs:02d}")
        self.label.update()
        
        self.update_display_color(force_normal=True)

    def update_timer(self):
        if self.state == "RUNNING":
            now = time.time()
            diff = self.target_timestamp - now
            if diff > 0:
                mins, secs = divmod(int(diff) + 1, 60)
                self.label.config(text=f"{mins:02d}:{secs:02d}")
                ahead = self.get_conf("Ahead", dtype=int)
                if diff <= ahead and not self.warning_triggered:
                    self.warning_triggered = True
                    color = self.get_conf("AheadColor")
                    if not color or color == "0": color = "FCD34D"
                    self.label.config(fg="#" + color.replace("#", ""))
                    if self.get_conf("PlayWarningSound", dtype=bool):
                        SoundPlayer.play(self.get_conf("WarningSoundFile"))
            else:
                if not self.finish_triggered:
                    self.finish_triggered = True
                    color = self.get_conf("timeoutColor")
                    if not color or color == "0": color = "EF4444"
                    self.label.config(fg="#" + color.replace("#", ""))
                    if self.get_conf("PlayFinishSound", dtype=bool):
                        SoundPlayer.play(self.get_conf("FinishSoundFile"))
                    keys = self.get_conf("sendOnTimeout")
                    if keys and keys != "0": self.send_keys_action(keys)
                abs_diff = abs(int(diff))
                mins, secs = divmod(abs_diff, 60)
                self.label.config(text=f"{mins:02d}:{secs:02d}")
        self.root.after(100, self.update_timer)

    def update_display_color(self, force_normal=False):
        raw = self.get_conf("textcolor")
        color = "#" + raw.replace("#", "") if raw and raw != "0" else "#E0E0E0"
        self.label.config(fg=color)
        if hasattr(self, 'hint_label'):
             self.hint_label.configure(fg=color)

    def send_keys_action(self, key_string):
        try:
            keys = key_string.split(',')
            for k in keys:
                k = k.strip()
                if k == "{ESC}": k = "esc"
                if k == "#d": k = "windows+d"
                threading.Thread(target=lambda: keyboard.press_and_release(k)).start()
        except: pass

    def quit_app(self):
        SoundPlayer.stop()
        self.save_status("lastProfile", self.current_profile.replace("Profile_", "").replace("Main", "0"))
        try: self.root.destroy()
        except: pass
        os._exit(0)

    def save_status(self, key, value):
        if not self.config.has_section("Status"): self.config.add_section("Status")
        self.config.set("Status", key, value)
        try: 
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f: self.config.write(f)
        except: pass

    def register_hotkeys(self):
        try: keyboard.unhook_all_hotkeys()
        except: pass
        
        try:
            def safe_call(func): self.root.after_idle(func)
            s = "shortcuts"
            if self.config.has_section(s):
                keyboard.add_hotkey(self.config.get(s, "startKey"), lambda: safe_call(self.start_timer))
                keyboard.add_hotkey(self.config.get(s, "pauseKey"), lambda: safe_call(self.pause_timer))
                keyboard.add_hotkey(self.config.get(s, "resetKey"), lambda: safe_call(self.reset_timer))
                keyboard.add_hotkey(self.config.get(s, "quitKey"), lambda: safe_call(self.quit_app))
        except Exception as e:
            print(f"Hotkey Error: {e}")

    def change_profile(self, profile_name):
        self.profile_var.set(profile_name)
        self.root.after(10, lambda: self._perform_profile_change(profile_name))

    def _perform_profile_change(self, profile_name):
        self.root.withdraw()
        self.apply_profile(profile_name)
        self.reset_timer() 
        idx = profile_name.replace("Profile_", "").replace("Main", "0")
        self.save_status("lastProfile", idx)
        self.root.deiconify()
        self.root.update_idletasks()
        self.root.update()

    def show_context_menu(self, event):
        menu = tk.Menu(self.root, tearoff=0)
        
        s = "shortcuts"
        start_key = self.config.get(s, "startKey", fallback="F9").upper()
        pause_key = self.config.get(s, "pauseKey", fallback="F11").upper()
        reset_key = self.config.get(s, "resetKey", fallback="F12").upper()
        quit_key = self.config.get(s, "quitKey", fallback="Ctrl+Shift+K").upper()

        menu.add_command(label=f"► {self.lang_helper.get('start')} ({start_key})", command=self.start_timer)
        menu.add_command(label=f"∥ {self.lang_helper.get('pause')} ({pause_key})", command=self.pause_timer)
        menu.add_command(label=f"⟳ {self.lang_helper.get('reset')} ({reset_key})", command=self.reset_timer)
        menu.add_command(label=f"⌛  {self.lang_helper.get('custom_time')}", command=self.set_custom_time)
        
        menu.add_separator()

        pos_menu = tk.Menu(menu, tearoff=0)
        positions = [
            (self.lang_helper.get("pos_tl"), "TL"), 
            (self.lang_helper.get("pos_tr"), "TR"), 
            (self.lang_helper.get("pos_bl"), "BL"), 
            (self.lang_helper.get("pos_br"), "BR")
        ]
        
        for label, code in positions:
            pos_menu.add_radiobutton(
                label=label,
                variable=self.position_var,
                value=code,
                command=lambda c=code: self.set_position(c)
            )
        menu.add_cascade(label=f"📍 {self.lang_helper.get('position')}", menu=pos_menu)
        menu.add_separator()

        menu.add_radiobutton(
            label=self.lang_helper.get("profile_main"),
            variable=self.profile_var,
            value="Main",
            command=lambda: self.change_profile("Main")
        )

        for section in self.config.sections():
            if section.startswith("Profile_"):
                name = self.config.get(section, "name", fallback=section)
                menu.add_radiobutton(
                    label=name,
                    variable=self.profile_var,
                    value=section,
                    command=lambda s=section: self.change_profile(s)
                )
        
        menu.add_separator()
        menu.add_command(label=f"⚙ {self.lang_helper.get('settings')}", command=self.open_settings)
        menu.add_command(label=f"⟳ {self.lang_helper.get('reload')}", command=self.reload_config)
        menu.add_separator()
        menu.add_command(label=f"× {self.lang_helper.get('quit')} ({quit_key})", command=self.quit_app)
        
        menu.tk_popup(event.x_root, event.y_root)
        return "break"

    def create_default_ini(self):
        # 修正：這裡應該寫入預設的 config 內容，避免空檔案錯誤
        default_config = """[Main]
duration = 1200
ahead = 60
fontface = Calibri
fontweight = bold
fontsize = 54
width = 240
height = 70
margin = 24
position = RT
opacity = 230
backgroundcolor = #FFFFFF
textcolor = #000000
aheadcolor = #000000
timeoutcolor = #F87171
playwarningsound = 0
playfinishsound = 0
stopresetstimer = 0
sendontimeout = 0
warningsoundfile = 
finishsoundfile = 

[shortcuts]
startkey = F9
pausekey = F10
resetkey = F12
quitkey = Ctrl+Shift+K

[Profile_1]
name = 10分鐘
duration = 600

[Profile_2]
name = 5分鐘
duration = 300

[Status]
lastprofile = 0
lastmonitor = 0
lastposition = TR
"""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                f.write(default_config)
        except: pass

if __name__ == "__main__":
    app = AdvancedTimer()