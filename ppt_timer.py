__version__ = "2.4.4"

import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser, filedialog, font
from tkinter import ttk
import configparser
import os
import time
import ctypes
import keyboard
from screeninfo import get_monitors
import threading
import winreg
import sys

CONFIG_FILE = "timer_config.ini"
LANG_FILE = "language.ini"

# --- 預設 Config ---
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
thememode = system
backgroundcolor = #FFFFFF
textcolor = #000000
aheadcolor = #000000
timeoutcolor = #F87171
playwarningsound = 0
playfinishsound = 0
stopresetstimer = 0
sendontimeout = 0
showstatusindicator = 1
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

# --- 預設語言檔 ---
DEFAULT_LANG_CONTENT = """[zh_TW]
name = 繁體中文
start = 開始
pause = 暫停
reset = 重置
custom_time = 自訂時間...
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
tab_interface = 介面設定
tab_about = 關於
lbl_lang_select = 語言 (Language)
lbl_lang_note = * 修改設定後請點擊儲存，介面將自動更新。
lbl_profile_name = 設定檔名稱
lbl_duration = 時間長度 (秒)
lbl_width = 視窗寬度
lbl_height = 視窗高度
lbl_opacity = 透明度 (0-255)
lbl_margin = 邊緣距離
lbl_fontsize = 字體大小
lbl_fontface = 字體名稱
lbl_fontweight = 字體粗細
lbl_theme_mode = 設定視窗主題
lbl_show_indicator = 顯示狀態指示燈 (►/∥/■)
lbl_color_settings = --- 計時器顏色設定 ---
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
lbl_version = 版本
lbl_author = 開發者
lbl_license = 授權
theme_system = 💻 跟隨系統
theme_dark = 🌙 深色模式
theme_light = ☀ 淺色模式
ct_title = 自訂時間
ct_min = 分鐘
ct_sec = 秒鐘
ct_ok = 確定
ct_cancel = 取消
about_desc = 這是一個專為演講者、簡報者與直播主設計的輕量級、透明置頂倒數計時器
btn_add = ➕ 新增
btn_del = ➖ 刪除
btn_save = 儲存全部並套用
btn_cancel = 取消
btn_pick_color = 選色
editor_title = 設定編輯器
about_title = 關於 PPT Timer
about_msg = PPT Timer\\n版本: {}\\n\\n一個專為演講者設計的\\n輕量級、透明置頂倒數計時器。\\n\\nLicense: MIT

[en_US]
name = English
start = Start
pause = Pause
reset = Reset
custom_time = Custom Time...
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
tab_interface = Interface
tab_about = About
lbl_lang_select = Language
lbl_lang_note = * Save to apply changes.
lbl_profile_name = Profile Name
lbl_duration = Duration (sec)
lbl_width = Width
lbl_height = Height
lbl_opacity = Opacity (0-255)
lbl_margin = Margin
lbl_fontsize = Font Size
lbl_fontface = Font Family
lbl_fontweight = Font Weight
lbl_theme_mode = Editor Theme
lbl_show_indicator = Show Status Indicator (►/∥/■)
lbl_color_settings = --- Timer Colors ---
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
lbl_version = Version
lbl_author = Developer
lbl_license = License
theme_system = 💻 System Default
theme_dark = 🌙 Dark Mode
theme_light = ☀ Light Mode
ct_title = Custom Time
ct_min = Minutes
ct_sec = Seconds
ct_ok = OK
ct_cancel = Cancel
about_desc = A lightweight, always-on-top timer designed for presenters and streamers.
btn_del = ➖ Del
btn_save = Save & Apply
btn_cancel = Cancel
btn_pick_color = Pick
editor_title = Settings Editor
about_title = About PPT Timer
about_msg = PPT Timer\\nVersion: {}\\n\\nA lightweight, always-on-top\\ntimer designed for presenters.\\n\\nLicense: MIT

[zh_CN]
name = 简体中文
start = 开始
pause = 暂停
reset = 重置
custom_time = 自定义时间...
settings = 设置...
reload = 重新读取设置
quit = 退出
position = 位置
pos_tl = ↖ 左上 (TL)
pos_tr = ↗ 右上 (TR)
pos_bl = ↙ 左下 (BL)
pos_br = ↘ 右下 (BR)
profile_main = Main (默认)
input_profile_name = 请输入配置文件名称 (例如: 5分钟演讲):
confirm_delete = 确定要删除配置文件 [{}] 吗？
cannot_delete_main = 不能删除默认的 Main 配置文件。
saved_success = 设置已保存！
save_error = 保存失败: {}
tab_general = 常规
tab_appearance = 外观
tab_alert = 警示
tab_hotkey = 快捷键
tab_interface = 界面设置
tab_about = 关于
lbl_lang_select = 语言 (Language)
lbl_lang_note = * 修改设置后请点击保存，界面将自动更新。
lbl_profile_name = 配置文件名称
lbl_duration = 时间长度 (秒)
lbl_width = 窗口宽度
lbl_height = 窗口高度
lbl_opacity = 透明度 (0-255)
lbl_margin = 边缘距离
lbl_fontsize = 字体大小
lbl_fontface = 字体名称
lbl_fontweight = 字体粗细
lbl_theme_mode = 设置窗口主题
lbl_show_indicator = 显示状态指示灯 (►/∥/■)
lbl_color_settings = --- 计时器颜色设置 ---
lbl_bg_color = 背景颜色
lbl_text_color = 文字颜色
lbl_ahead = 倒数前警告 (秒)
lbl_ahead_color = 警告文字颜色
lbl_timeout_color = 时间到文字颜色
lbl_sound_action = --- 音效与动作 ---
lbl_play_warn = 播放警告音效
lbl_warn_file = 警告音效档
lbl_play_finish = 播放结束音效
lbl_finish_file = 结束音效档
lbl_key_start = 开始计时
lbl_key_pause = 暂停计时
lbl_key_reset = 重置计时
lbl_key_quit = 关闭程序
lbl_version = 版本
lbl_author = 开发者
lbl_license = 授权
theme_system = 💻 跟随系统
theme_dark = 🌙 深色模式
theme_light = ☀ 浅色模式
ct_title = 自定义时间
ct_min = 分钟
ct_sec = 秒
ct_ok = 确定
ct_cancel = 取消
about_desc = 这是一个专为演讲者、演示者与主播设计的轻量级、透明置顶倒数计时器
btn_add = ➕ 新增
btn_del = ➖ 删除
btn_save = 保存全部并应用
btn_cancel = 取消
btn_pick_color = 选色
editor_title = 设置编辑器
about_title = 关于 PPT Timer
about_msg = PPT Timer\\n版本: {}\\n\\n一个专为演讲者设计的\\n轻量级、透明置顶倒数计时器。\\n\\nLicense: MIT

[ja_JP]
name = 日本語
start = スタート
pause = 一時停止
reset = リセット
custom_time = 時間を指定...
settings = 設定...
reload = 設定を再読み込み
quit = 終了
position = 位置
pos_tl = ↖ 左上 (TL)
pos_tr = ↗ 右上 (TR)
pos_bl = ↙ 左下 (BL)
pos_br = ↘ 右下 (BR)
profile_main = Main (デフォルト)
input_profile_name = プロファイル名を入力 (例: 5分スピーチ):
confirm_delete = プロファイル [{}] を削除しますか？
cannot_delete_main = Main プロファイルは削除できません。
saved_success = 設定を保存しました！
save_error = エラー: {}
tab_general = 一般
tab_appearance = 外観
tab_alert = アラート
tab_hotkey = ホットキー
tab_interface = インターフェース
tab_about = 情報
lbl_lang_select = 言語 (Language)
lbl_lang_note = * 保存すると変更が適用されます。
lbl_profile_name = プロファイル名
lbl_duration = 時間 (秒)
lbl_width = ウィンドウ幅
lbl_height = ウィンドウ高さ
lbl_opacity = 不透明度 (0-255)
lbl_margin = マージン
lbl_fontsize = フォントサイズ
lbl_fontface = フォント名
lbl_fontweight = 太さ
lbl_theme_mode = 設定画面のテーマ
lbl_show_indicator = ステータスアイコンを表示 (►/∥/■)
lbl_color_settings = --- タイマーの配色 ---
lbl_bg_color = 背景色
lbl_text_color = 文字色
lbl_ahead = 警告タイミング (秒前)
lbl_ahead_color = 警告時の文字色
lbl_timeout_color = 終了時の文字色
lbl_sound_action = --- 音効とアクション ---
lbl_play_warn = 警告音を再生
lbl_warn_file = 警告音ファイル
lbl_play_finish = 終了音を再生
lbl_finish_file = 終了音ファイル
lbl_key_start = 開始キー
lbl_key_pause = 一時停止キー
lbl_key_reset = リセットキー
lbl_key_quit = 終了キー
lbl_version = バージョン
lbl_author = 開発者
lbl_license = ライセンス
theme_system = 💻 システム準拠
theme_dark = 🌙 ダークモード
theme_light = ☀ ライトモード
ct_title = 時間指定
ct_min = 分
ct_sec = 秒
ct_ok = OK
ct_cancel = キャンセル
about_desc = プレゼンターや配信者のために設計された、軽量で常に手前に表示されるタイマーです。
btn_add = ➕ 追加
btn_del = ➖ 削除
btn_save = 保存して適用
btn_cancel = キャンセル
btn_pick_color = 色選択
editor_title = 設定エディタ
about_title = PPT Timer について
about_msg = PPT Timer\\nバージョン: {}\\n\\nプレゼンター向けに設計された\\n軽量・透明・最前面表示のタイマーソフト。\\n\\nLicense: MIT

[ko_KR]
name = 한국어
start = 시작
pause = 일시정지
reset = 초기화
custom_time = 시간 지정...
settings = 설정...
reload = 설정 다시 불러오기
quit = 종료
position = 위치
pos_tl = ↖ 좌측 상단 (TL)
pos_tr = ↗ 우측 상단 (TR)
pos_bl = ↙ 좌측 하단 (BL)
pos_br = ↘ 우측 하단 (BR)
profile_main = Main (기본)
input_profile_name = 프로필 이름을 입력하세요 (예: 5분 발표):
confirm_delete = 프로필 [{}] 을(를) 삭제하시겠습니까?
cannot_delete_main = Main 프로필은 삭제할 수 없습니다.
saved_success = 설정이 저장되었습니다!
save_error = 저장 실패: {}
tab_general = 일반
tab_appearance = 외관
tab_alert = 알림
tab_hotkey = 단축키
tab_interface = 인터페이스
tab_about = 정보
lbl_lang_select = 언어 (Language)
lbl_lang_note = * 저장 버튼을 누르면 언어가 변경됩니다.
lbl_profile_name = 프로필 이름
lbl_duration = 시간 설정 (초)
lbl_width = 창 너비
lbl_height = 창 높이
lbl_opacity = 불투명도 (0-255)
lbl_margin = 여백
lbl_fontsize = 글꼴 크기
lbl_fontface = 글꼴 이름
lbl_fontweight = 글꼴 굵기
lbl_theme_mode = 설정창 테마
lbl_show_indicator = 상태 아이콘 표시 (►/∥/■)
lbl_color_settings = --- 타이머 색상 설정 ---
lbl_bg_color = 배경 색상
lbl_text_color = 텍스트 색상
lbl_ahead = 경고 시간 (초 전)
lbl_ahead_color = 경고 텍스트 색상
lbl_timeout_color = 종료 텍스트 색상
lbl_sound_action = --- 소리 및 동작 ---
lbl_play_warn = 경고음 재생
lbl_warn_file = 경고음 파일
lbl_play_finish = 종료음 재생
lbl_finish_file = 종료음 파일
lbl_key_start = 시작 키
lbl_key_pause = 일시정지 키
lbl_key_reset = 초기화 키
lbl_key_quit = 종료 키
lbl_version = 버전
lbl_author = 개발자
lbl_license = 라이선스
theme_system = 💻 시스템 기본값
theme_dark = 🌙 다크 모드
theme_light = ☀ 라이트 모드
ct_title = 시간 지정
ct_min = 분
ct_sec = 초
ct_ok = 확인
ct_cancel = 취소
about_desc = 발표자 및 스트리머를 위해 설계된 가볍고 항상 위에 표시되는 타이머입니다.
btn_add = ➕ 추가
btn_del = ➖ 삭제
btn_save = 저장 및 적용
btn_cancel = 취소
btn_pick_color = 색상 선택
editor_title = 설정 편집기
about_title = PPT Timer 정보
about_msg = PPT Timer\\n버전: {}\\n\\n발표자를 위해 설계된\\n가볍고 투명한 최상위 타이머입니다.\\n\\nLicense: MIT

[ru_RU]
name = Русский
start = Старт
pause = Пауза
reset = Сброс
custom_time = Своё время...
settings = Настройки...
reload = Перезагрузить
quit = Выход
position = Позиция
pos_tl = ↖ Верх-Лев (TL)
pos_tr = ↗ Верх-Прав (TR)
pos_bl = ↙ Низ-Лев (BL)
pos_br = ↘ Низ-Прав (BR)
profile_main = Main (По умолч.)
input_profile_name = Введите имя профиля (напр.: 5 минут):
confirm_delete = Удалить профиль [{}]?
cannot_delete_main = Нельзя удалить главный профиль.
saved_success = Настройки сохранены!
save_error = Ошибка: {}
tab_general = Общие
tab_appearance = Вид
tab_alert = Оповещ.
tab_hotkey = Хоткеи
tab_interface = Интерфейс
tab_about = О прог.
lbl_lang_select = Язык (Language)
lbl_lang_note = * Сохраните, чтобы применить язык.
lbl_profile_name = Имя профиля
lbl_duration = Длительность (сек)
lbl_width = Ширина окна
lbl_height = Высота окна
lbl_opacity = Прозрачность (0-255)
lbl_margin = Отступ
lbl_fontsize = Размер шрифта
lbl_fontface = Шрифт
lbl_fontweight = Жирность
lbl_theme_mode = Тема окна
lbl_show_indicator = Индикатор статуса (►/∥/■)
lbl_color_settings = --- Цвета таймера ---
lbl_bg_color = Фон
lbl_text_color = Текст
lbl_ahead = Предупреждение (сек)
lbl_ahead_color = Цвет предупр.
lbl_timeout_color = Цвет финиша
lbl_sound_action = --- Звук и действия ---
lbl_play_warn = Звук предупр.
lbl_warn_file = Файл предупр.
lbl_play_finish = Звук финиша
lbl_finish_file = Файл финиша
lbl_key_start = Старт
lbl_key_pause = Пауза
lbl_key_reset = Сброс
lbl_key_quit = Выход
lbl_version = Версия
lbl_author = Автор
lbl_license = Лицензия
theme_system = 💻 Системная
theme_dark = 🌙 Тёмная
theme_light = ☀ Светлая
ct_title = Своё время
ct_min = Минуты
ct_sec = Секунды
ct_ok = ОК
ct_cancel = Отмена
about_desc = Легкий таймер поверх всех окон для спикеров и стримеров.
btn_add = ➕ Доб.
btn_del = ➖ Удал.
btn_save = Сохранить
btn_cancel = Отмена
btn_pick_color = Цвет
editor_title = Редактор настроек
about_title = О программе PPT Timer
about_msg = PPT Timer\\nВерсия: {}\\n\\nЛегкий таймер поверх всех окон,\\nразработанный для презентаций.\\n\\nLicense: MIT

[es_ES]
name = Español
start = Iniciar
pause = Pausar
reset = Reiniciar
custom_time = Tiempo personal...
settings = Configuración...
reload = Recargar
quit = Salir
position = Posición
pos_tl = ↖ Arriba-Izq (TL)
pos_tr = ↗ Arriba-Der (TR)
pos_bl = ↙ Abajo-Izq (BL)
pos_br = ↘ Abajo-Der (BR)
profile_main = Main (Predet.)
input_profile_name = Nombre del perfil (ej. Charla 5min):
confirm_delete = ¿Eliminar perfil [{}]?
cannot_delete_main = No se puede eliminar el perfil Main.
saved_success = ¡Guardado con éxito!
save_error = Error: {}
tab_general = General
tab_appearance = Apariencia
tab_alert = Alertas
tab_hotkey = Atajos
tab_interface = Interfaz
tab_about = Acerca de
lbl_lang_select = Idioma (Language)
lbl_lang_note = * Guarde para aplicar cambios.
lbl_profile_name = Nombre de Perfil
lbl_duration = Duración (seg)
lbl_width = Ancho
lbl_height = Alto
lbl_opacity = Opacidad (0-255)
lbl_margin = Margen
lbl_fontsize = Tamaño fuente
lbl_fontface = Fuente
lbl_fontweight = Grosor
lbl_theme_mode = Tema del Editor
lbl_show_indicator = Indicador de estado (►/∥/■)
lbl_color_settings = --- Colores del Temporizador ---
lbl_bg_color = Fondo
lbl_text_color = Color Texto
lbl_ahead = Aviso (seg antes)
lbl_ahead_color = Color de Aviso
lbl_timeout_color = Color de Fin
lbl_sound_action = --- Sonido y Acción ---
lbl_play_warn = Sonido de Aviso
lbl_warn_file = Archivo Aviso
lbl_play_finish = Sonido de Fin
lbl_finish_file = Archivo Fin
lbl_key_start = Tecla Inicio
lbl_key_pause = Tecla Pausa
lbl_key_reset = Tecla Reset
lbl_key_quit = Tecla Salir
lbl_version = Versión
lbl_author = Desarrollador
lbl_license = Licencia
theme_system = 💻 Sistema
theme_dark = 🌙 Oscuro
theme_light = ☀ Claro
ct_title = Tiempo personal
ct_min = Minutos
ct_sec = Segundos
ct_ok = OK
ct_cancel = Cancelar
about_desc = Un temporizador ligero y siempre visible para presentadores.
btn_add = ➕ Añadir
btn_del = ➖ Borrar
btn_save = Guardar
btn_cancel = Cancelar
btn_pick_color = Color
editor_title = Editor de Configuración
about_title = Acerca de PPT Timer
about_msg = PPT Timer\\nVersión: {}\\n\\nUn temporizador ligero y siempre visible\\ndiseñado para presentadores.\\n\\nLicense: MIT

[fr_FR]
name = Français
start = Démarrer
pause = Pause
reset = Réinitialiser
custom_time = Temps perso...
settings = Paramètres...
reload = Recharger
quit = Quitter
position = Position
pos_tl = ↖ Haut-Gauche (TL)
pos_tr = ↗ Haut-Droite (TR)
pos_bl = ↙ Bas-Gauche (BL)
pos_br = ↘ Bas-Droite (BR)
profile_main = Main (Défaut)
input_profile_name = Nom du profil (ex: Talk 5min):
confirm_delete = Supprimer le profil [{}] ?
cannot_delete_main = Impossible de supprimer le profil Main.
saved_success = Paramètres sauvegardés !
save_error = Erreur : {}
tab_general = Général
tab_appearance = Apparence
tab_alert = Alertes
tab_hotkey = Raccourcis
tab_interface = Interface
tab_about = À propos
lbl_lang_select = Langue (Language)
lbl_lang_note = * Enregistrez pour appliquer.
lbl_profile_name = Nom du profil
lbl_duration = Durée (sec)
lbl_width = Largeur
lbl_height = Hauteur
lbl_opacity = Opacité (0-255)
lbl_margin = Marge
lbl_fontsize = Taille police
lbl_fontface = Police
lbl_fontweight = Graisse
lbl_theme_mode = Thème (Éditeur)
lbl_show_indicator = Indicateur d'état (►/∥/■)
lbl_color_settings = --- Couleurs du Timer ---
lbl_bg_color = Arrière-plan
lbl_text_color = Couleur du texte
lbl_ahead = Avertissement (sec)
lbl_ahead_color = Couleur Avert.
lbl_timeout_color = Couleur Fin
lbl_sound_action = --- Sons et Actions ---
lbl_play_warn = Son d'avertissement
lbl_warn_file = Fichier Avert.
lbl_play_finish = Son de fin
lbl_finish_file = Fichier Fin
lbl_key_start = Touche Début
lbl_key_pause = Touche Pause
lbl_key_reset = Touche Reset
lbl_key_quit = Touche Quitter
lbl_version = Version
lbl_author = Développeur
lbl_license = Licence
theme_system = 💻 Système
theme_dark = 🌙 Sombre
theme_light = ☀ Clair
ct_title = Temps perso
ct_min = Minutes
ct_sec = Secondes
ct_ok = OK
ct_cancel = Annuler
about_desc = Un minuteur léger, toujours au premier plan, pour présentateurs.
btn_add = ➕ Ajouter
btn_del = ➖ Suppr.
btn_save = Enregistrer
btn_cancel = Annuler
btn_pick_color = Choisir
editor_title = Éditeur de paramètres
about_title = À propos de PPT Timer
about_msg = PPT Timer\\nVersion : {}\\n\\nUn minuteur léger et toujours visible\\nconçu pour les présentateurs.\\n\\nLicense: MIT

[de_DE]
name = Deutsch
start = Start
pause = Pause
reset = Reset
custom_time = Zeit wählen...
settings = Einstellungen...
reload = Neu laden
quit = Beenden
position = Position
pos_tl = ↖ Oben-Links (TL)
pos_tr = ↗ Oben-Rechts (TR)
pos_bl = ↙ Unten-Links (BL)
pos_br = ↘ Unten-Rechts (BR)
profile_main = Main (Standard)
input_profile_name = Profilname (z.B. 5 Min Talk):
confirm_delete = Profil [{}] löschen?
cannot_delete_main = Das Main-Profil kann nicht gelöscht werden.
saved_success = Einstellungen gespeichert!
save_error = Fehler: {}
tab_general = Allgemein
tab_appearance = Aussehen
tab_alert = Alarm
tab_hotkey = Hotkeys
tab_interface = Oberfläche
tab_about = Über
lbl_lang_select = Sprache (Language)
lbl_lang_note = * Speichern zum Anwenden.
lbl_profile_name = Profilname
lbl_duration = Dauer (Sek)
lbl_width = Breite
lbl_height = Höhe
lbl_opacity = Deckkraft (0-255)
lbl_margin = Randabstand
lbl_fontsize = Schriftgröße
lbl_fontface = Schriftart
lbl_fontweight = Schriftstärke
lbl_theme_mode = Editor-Design
lbl_show_indicator = Statusanzeige (►/∥/■)
lbl_color_settings = --- Timer-Farben ---
lbl_bg_color = Hintergrund
lbl_text_color = Textfarbe
lbl_ahead = Warnzeit (Sek vor Ende)
lbl_ahead_color = Warnfarbe
lbl_timeout_color = Endfarbe
lbl_sound_action = --- Ton & Aktionen ---
lbl_play_warn = Warnton abspielen
lbl_warn_file = Warnton-Datei
lbl_play_finish = Endton abspielen
lbl_finish_file = Endton-Datei
lbl_key_start = Start-Taste
lbl_key_pause = Pause-Taste
lbl_key_reset = Reset-Taste
lbl_key_quit = Beenden-Taste
lbl_version = Version
lbl_author = Entwickler
lbl_license = Lizenz
theme_system = 💻 Systemstandard
theme_dark = 🌙 Dunkel
theme_light = ☀ Hell
ct_title = Zeit wählen
ct_min = Minuten
ct_sec = Sekunden
ct_ok = OK
ct_cancel = Abbrechen
about_desc = Ein leichter "Always-on-Top" Timer für Präsentationen.
btn_add = ➕ Neu
btn_del = ➖ Löschen
btn_save = Speichern
btn_cancel = Abbrechen
btn_pick_color = Farbe
editor_title = Einstellungen
about_title = Über PPT Timer
about_msg = PPT Timer\\nVersion: {}\\n\\nEin leichter Timer für Präsentatoren,\\nder immer im Vordergrund bleibt.\\n\\nLicense: MIT
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
        except configparser.ParsingError as e:
            print(f"Language file parsing error: {e}")
        except Exception as e:
            print(f"Language load error: {e}")

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
        if not filepath:
            return
        
        # 取得程式所在目錄
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            
        # 如果路徑不是絕對路徑，則加上程式目錄
        target_path = filepath
        if not os.path.isabs(filepath):
            target_path = os.path.join(base_dir, filepath)
            
        if not os.path.exists(target_path):
            return
            
        alias = "timer_sound"
        try:
            ctypes.windll.winmm.mciSendStringW(f"close {alias}", None, 0, 0)
            cmd_open = f'open "{target_path}" type mpegvideo alias {alias}'
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

class CustomTimeDialog(tk.Toplevel):
    def __init__(self, parent, colors, lang_helper):
        super().__init__(parent.root)
        self.parent = parent
        self.colors = colors
        self.lang = lang_helper
        self.result = None
        
        self.title(self.lang.get("ct_title"))
        self.geometry("300x160")
        self.configure(bg=colors["bg"])
        self.attributes('-topmost', True)
        self.grab_set()
        
        try:
            self.update_idletasks() 
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            get_parent = ctypes.windll.user32.GetParent
            hwnd = get_parent(self.winfo_id())
            is_dark = True if colors["bg"].startswith("#2") else False
            value = ctypes.c_int(1 if is_dark else 0)
            set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value))
        except: pass

        self.setup_ui()
        
        self.bind('<Return>', lambda e: self.on_ok())
        self.bind('<Escape>', lambda e: self.destroy())

    def setup_ui(self):
        content = tk.Frame(self, bg=self.colors["bg"], padx=20, pady=20)
        content.pack(fill="both", expand=True)

        tk.Label(content, text=self.lang.get("ct_min"), bg=self.colors["bg"], fg=self.colors["fg"]).grid(row=0, column=0, padx=5, sticky="w")
        self.var_min = tk.StringVar(value="5")
        e_min = tk.Entry(content, textvariable=self.var_min, width=10, bg=self.colors["input_bg"], fg=self.colors["input_fg"], insertbackground=self.colors["fg"])
        e_min.grid(row=0, column=1, padx=5, pady=5)
        e_min.focus_set()
        e_min.select_range(0, tk.END)

        tk.Label(content, text=self.lang.get("ct_sec"), bg=self.colors["bg"], fg=self.colors["fg"]).grid(row=1, column=0, padx=5, sticky="w")
        self.var_sec = tk.StringVar(value="0")
        tk.Entry(content, textvariable=self.var_sec, width=10, bg=self.colors["input_bg"], fg=self.colors["input_fg"], insertbackground=self.colors["fg"]).grid(row=1, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self, bg=self.colors["bg"], pady=15)
        btn_frame.pack(fill="x")
        
        btn_opts = {"bg": self.colors["btn_bg"], "fg": self.colors["btn_fg"], "relief": "flat", "width": 8}
        
        tk.Button(btn_frame, text=self.lang.get("ct_ok"), command=self.on_ok, bg="#4CAF50", fg="white", relief="flat", width=8).pack(side="right", padx=10)
        tk.Button(btn_frame, text=self.lang.get("ct_cancel"), command=self.destroy, **btn_opts).pack(side="right", padx=10)

    def on_ok(self):
        try:
            m = int(self.var_min.get() or 0)
            s = int(self.var_sec.get() or 0)
            if m < 0: m = 0
            if s < 0: s = 0
            self.result = m * 60 + s
            self.destroy()
        except ValueError:
            pass

class SettingsEditor(tk.Toplevel):
    def __init__(self, parent, config, current_profile_section, lang_helper):
        super().__init__(parent.root)
        self.parent = parent
        self.config = config
        self.editing_section = current_profile_section
        self.lang = lang_helper
        
        self.title(self.lang.get("editor_title"))
        self.geometry("520x680")
        
        self.ui_vars = {} 
        self.theme_map = {
            self.lang.get("theme_system"): "system",
            self.lang.get("theme_dark"): "dark",
            self.lang.get("theme_light"): "light"
        }
        
        self.determine_theme_colors()
        
        self.configure(bg=self.colors["bg"])
        self.attributes('-topmost', True)
        self.grab_set()
        
        self.apply_title_bar_theme()

        self.setup_ui()
        self.load_section_to_ui(self.editing_section)

    def determine_theme_colors(self):
        mode = self.config.get("Main", "thememode", fallback="system")
        self.is_dark = False

        if mode == "system":
            self.is_dark = (self.parent.get_system_theme() == "dark")
        elif mode == "dark":
            self.is_dark = True
        else:
            self.is_dark = False

        if self.is_dark:
            self.colors = {
                "bg": "#2b2b2b",         
                "fg": "#ffffff",         
                "input_bg": "#3c3c3c",   
                "input_fg": "#ffffff",   
                "btn_bg": "#444444",     
                "btn_fg": "#ffffff",     
                "highlight": "#555555"   
            }
        else:
            self.colors = {
                "bg": "#f0f0f0",
                "fg": "#000000",
                "input_bg": "#ffffff",
                "input_fg": "#000000",
                "btn_bg": "#e1e1e1",
                "btn_fg": "#000000",
                "highlight": "#d0d0d0"
            }

    def apply_title_bar_theme(self):
        try:
            self.update_idletasks() 
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            get_parent = ctypes.windll.user32.GetParent
            hwnd = get_parent(self.winfo_id())
            value = ctypes.c_int(1 if self.is_dark else 0)
            set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value))
        except Exception as e:
            pass

    def setup_ui(self):
        style = ttk.Style(self)
        try:
            style.theme_use('clam')
        except: pass
        
        style.configure("TFrame", background=self.colors["bg"])
        style.configure("TLabel", background=self.colors["bg"], foreground=self.colors["fg"])
        style.configure("TNotebook", background=self.colors["bg"], borderwidth=0)
        style.configure("TNotebook.Tab", 
                        background=self.colors["btn_bg"], 
                        foreground=self.colors["fg"], 
                        padding=[10, 5])
        style.map("TNotebook.Tab", 
                  background=[("selected", self.colors["highlight"])],
                  foreground=[("selected", self.colors["fg"])])

        top_frame = tk.Frame(self, bg=self.colors["bg"], pady=5)
        top_frame.pack(fill='x')

        self.profile_combo = ttk.Combobox(top_frame, state="readonly", width=25)
        self.profile_combo.pack(side='left', padx=10)
        self.profile_combo.bind("<<ComboboxSelected>>", self.on_profile_change)
        
        self.refresh_profile_list()

        btn_opts = {"bg": self.colors["btn_bg"], "fg": self.colors["btn_fg"], "activebackground": self.colors["highlight"], "activeforeground": self.colors["btn_fg"], "relief": "flat"}

        tk.Button(top_frame, text=self.lang.get("btn_add"), command=self.add_profile, width=6, **btn_opts).pack(side='left', padx=2)
        tk.Button(top_frame, text=self.lang.get("btn_del"), command=self.delete_profile, width=6, **btn_opts).pack(side='left', padx=2)

        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.create_general_tab(notebook)
        self.create_appearance_tab(notebook)
        self.create_alert_tab(notebook)
        self.create_hotkey_tab(notebook)
        self.create_interface_tab(notebook) 
        self.create_about_tab(notebook)

        btn_frame = tk.Frame(self, bg=self.colors["bg"])
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(btn_frame, text=self.lang.get("btn_save"), command=self.save_and_close, bg="#4CAF50", fg="white", width=15, relief="flat").pack(side='right', padx=5)
        tk.Button(btn_frame, text=self.lang.get("btn_cancel"), command=self.destroy, width=10, **btn_opts).pack(side='right', padx=5)

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

            if key == "thememode":
                val = self.config.get(section, key, fallback=None)
                if val is None and section != "Main":
                    val = self.config.get("Main", key, fallback="system")
                if val is None: val = "system"
                display = next((k for k, v in self.theme_map.items() if v == val), self.lang.get("theme_system"))
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
            elif key == "thememode":
                code = self.theme_map.get(val, "system")
                self.config.set(section, key, code)
            else:
                self.config.set(section, key, val)

    def add_entry(self, parent, row, label_text, key):
        tk.Label(parent, text=label_text, bg=self.colors["bg"], fg=self.colors["fg"]).grid(row=row, column=0, sticky='w', padx=10, pady=5)
        var = tk.StringVar()
        self.ui_vars[key] = var
        tk.Entry(parent, textvariable=var, width=20, bg=self.colors["input_bg"], fg=self.colors["input_fg"], insertbackground=self.colors["fg"]).grid(row=row, column=1, padx=10, pady=5)

    def add_scale(self, parent, row, label_text, key, min_val, max_val):
        tk.Label(parent, text=label_text, bg=self.colors["bg"], fg=self.colors["fg"]).grid(row=row, column=0, sticky='w', padx=10, pady=5)
        proxy_var = tk.IntVar()
        def on_scale_change(*args):
            self.ui_vars[key].set(str(proxy_var.get()))
        proxy_var.trace("w", on_scale_change)
        self.ui_vars[key] = tk.StringVar()
        def on_str_change(*args):
            try: proxy_var.set(int(float(self.ui_vars[key].get())))
            except: proxy_var.set(max_val)
        self.ui_vars[key].trace("w", on_str_change)
        tk.Scale(parent, from_=min_val, to=max_val, orient='horizontal', variable=proxy_var, 
                 bg=self.colors["bg"], fg=self.colors["fg"], highlightthickness=0).grid(row=row, column=1, sticky='ew', padx=10)

    def add_checkbox(self, parent, row, label_text, key):
        var = tk.StringVar()
        self.ui_vars[key] = var
        select_col = self.colors["input_bg"]
        tk.Checkbutton(parent, text=label_text, variable=var, onvalue="1", offvalue="0", 
                       bg=self.colors["bg"], fg=self.colors["fg"], selectcolor=select_col, activebackground=self.colors["bg"], activeforeground=self.colors["fg"]).grid(row=row, column=0, columnspan=2, sticky='w', padx=10, pady=2)

    def add_color_picker(self, parent, row, label_text, key):
        tk.Label(parent, text=label_text, bg=self.colors["bg"], fg=self.colors["fg"]).grid(row=row, column=0, sticky='w', padx=10, pady=5)
        var = tk.StringVar()
        self.ui_vars[key] = var
        frame = tk.Frame(parent, bg=self.colors["bg"])
        frame.grid(row=row, column=1, sticky='w', padx=10)
        
        entry = tk.Entry(frame, textvariable=var, width=10, bg=self.colors["input_bg"], fg=self.colors["input_fg"], insertbackground=self.colors["fg"])
        entry.pack(side='left')
        
        btn = tk.Button(frame, text=self.lang.get("btn_pick_color"), width=5, bg=self.colors["btn_bg"], fg=self.colors["btn_fg"])
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
        tk.Label(parent, text=label_text, bg=self.colors["bg"], fg=self.colors["fg"]).grid(row=row, column=0, sticky='w', padx=10, pady=5)
        var = tk.StringVar()
        self.ui_vars[key] = var
        frame = tk.Frame(parent, bg=self.colors["bg"])
        frame.grid(row=row, column=1, sticky='ew', padx=10)
        
        entry = tk.Entry(frame, textvariable=var, width=15, bg=self.colors["input_bg"], fg=self.colors["input_fg"], insertbackground=self.colors["fg"])
        entry.pack(side='left', fill='x', expand=True)
        
        def pick_file():
            filename = filedialog.askopenfilename(parent=self, filetypes=[("Audio Files", "*.mp3 *.wav *.mid")])
            if filename:
                # 嘗試轉為相對路徑
                try:
                    if getattr(sys, 'frozen', False):
                        base_dir = os.path.dirname(sys.executable)
                    else:
                        base_dir = os.path.dirname(os.path.abspath(__file__))
                    
                    rel_path = os.path.relpath(filename, base_dir)
                    
                    if rel_path.startswith(".."):
                        var.set(filename)
                    else:
                        var.set(rel_path)
                except:
                    var.set(filename)

        tk.Button(frame, text="...", command=pick_file, width=3, bg=self.colors["btn_bg"], fg=self.colors["btn_fg"]).pack(side='right')
    
    def add_combo(self, parent, row, label_text, key, values):
        tk.Label(parent, text=label_text, bg=self.colors["bg"], fg=self.colors["fg"]).grid(row=row, column=0, sticky='w', padx=10, pady=5)
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
        
        all_fonts = sorted(font.families())
        self.add_combo(frame, 1, self.lang.get("lbl_fontface"), "fontface", all_fonts)
        self.add_combo(frame, 2, self.lang.get("lbl_fontweight"), "fontweight", ["bold", "normal"])
        
        self.add_checkbox(frame, 3, self.lang.get("lbl_show_indicator"), "showstatusindicator")

        ttk.Separator(frame, orient='horizontal').grid(row=4, column=0, columnspan=2, sticky="ew", pady=10)
        tk.Label(frame, text=self.lang.get("lbl_color_settings"), bg=self.colors["bg"], fg=self.colors["fg"]).grid(row=5, column=0, columnspan=3, pady=5)
        
        self.add_color_picker(frame, 6, self.lang.get("lbl_bg_color"), "backgroundColor")
        self.add_color_picker(frame, 7, self.lang.get("lbl_text_color"), "textcolor")

    def create_alert_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=self.lang.get("tab_alert"))
        self.add_entry(frame, 0, self.lang.get("lbl_ahead"), "Ahead")
        self.add_color_picker(frame, 1, self.lang.get("lbl_ahead_color"), "AheadColor")
        self.add_color_picker(frame, 2, self.lang.get("lbl_timeout_color"), "timeoutColor")
        tk.Label(frame, text=self.lang.get("lbl_sound_action"), bg=self.colors["bg"], fg=self.colors["fg"]).grid(row=3, column=0, columnspan=3, pady=10)
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

    def create_interface_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=self.lang.get("tab_interface"))
        
        langs = self.lang.get_available_languages()
        lang_names = [name for code, name in langs]
        self.add_combo(frame, 0, self.lang.get("lbl_lang_select"), "language", lang_names)
        
        theme_names = list(self.theme_map.keys())
        self.add_combo(frame, 1, self.lang.get("lbl_theme_mode"), "thememode", theme_names)
        
        tk.Label(frame, text=self.lang.get("lbl_lang_note"), fg="gray", bg=self.colors["bg"]).grid(row=2, column=0, columnspan=2, padx=10, pady=20)

    def create_about_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=self.lang.get("tab_about"))
        
        tk.Label(frame, text="PPT Timer", font=("Helvetica", 16, "bold"), pady=10, bg=self.colors["bg"], fg=self.colors["fg"]).pack()
        tk.Label(frame, text=f"{self.lang.get('lbl_version')} {__version__}", font=("Helvetica", 10), bg=self.colors["bg"], fg=self.colors["fg"]).pack()
        ttk.Separator(frame, orient='horizontal').pack(fill='x', padx=20, pady=10)
        desc_text = self.lang.get("about_desc").replace("\\n", "\n")
        tk.Label(frame, text=desc_text, justify="center", wraplength=400, bg=self.colors["bg"], fg=self.colors["fg"]).pack(pady=10)
        tk.Label(frame, text="License: MIT", fg="gray", bg=self.colors["bg"]).pack(side="bottom", pady=20)

    def save_and_close(self):
        self.save_ui_to_virtual_config()
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                self.config.write(f)
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
        self.update_state_icon()
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
                'stopResetsTimer': 0, 'sendOnTimeout': 0,
                'thememode': 'system', 'showstatusindicator': 1
            }
            val = defaults.get(key, 0)

        try:
            if dtype == int: return int(val)
            elif dtype == bool: return str(val) == "1"
            return str(val)
        except:
            return 0 if dtype == int else str(val)

    def get_system_theme(self):
        try:
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return "light" if value == 1 else "dark"
        except Exception:
            return "light"
    
    # 抽取顏色邏輯供自訂對話框使用
    def get_theme_colors(self):
        mode = self.get_conf("thememode")
        if not mode: mode = "system"
        is_dark = False
        if mode == "system":
            is_dark = (self.get_system_theme() == "dark")
        elif mode == "dark":
            is_dark = True
        
        if is_dark:
            return {
                "bg": "#2b2b2b", "fg": "#ffffff", "input_bg": "#3c3c3c", 
                "input_fg": "#ffffff", "btn_bg": "#444444", "btn_fg": "#ffffff", "highlight": "#555555"
            }
        else:
            return {
                "bg": "#f0f0f0", "fg": "#000000", "input_bg": "#ffffff", 
                "input_fg": "#000000", "btn_bg": "#e1e1e1", "btn_fg": "#000000", "highlight": "#d0d0d0"
            }

    def apply_profile(self, profile_name):
        self.current_profile = profile_name
        self.custom_duration = None 
        
        raw_bg = self.get_conf("backgroundColor")
        bg_color = "#" + raw_bg.replace("#", "") if raw_bg and raw_bg != "0" else "#FFFFFF"
        
        raw_fg = self.get_conf("textcolor")
        fg_color = "#" + raw_fg.replace("#", "") if raw_fg and raw_fg != "0" else "#000000"
        
        self.current_bg = bg_color
        self.current_fg = fg_color

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
        self.update_state_icon()

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
        # 使用新的自訂時間對話框
        dialog = CustomTimeDialog(self, self.get_theme_colors(), self.lang_helper)
        self.root.wait_window(dialog)
        
        if dialog.result is not None:
            self.custom_duration = dialog.result
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
        self.update_state_icon()

    def pause_timer(self):
        if self.state == "RUNNING":
            self.state = "PAUSED"
            self.paused_time = self.target_timestamp - time.time()
            self.update_state_icon()

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
        self.update_state_icon()

    def update_state_icon(self):
        if not self.get_conf("showstatusindicator", dtype=bool):
            self.hint_label.config(text="")
            return

        icon = ""
        if self.state == "RUNNING":
            icon = "▶️"
        elif self.state == "PAUSED":
            icon = "⏸️"
        elif self.state == "STOPPED":
            icon = "⏹️"
        self.hint_label.config(text=icon)

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
        color = self.current_fg if hasattr(self, 'current_fg') else "#E0E0E0"
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
        # 獲取主題顏色
        colors = self.get_theme_colors()
        
        # 建立選單並設定顏色
        menu = tk.Menu(self.root, tearoff=0, 
                       bg=colors["bg"], 
                       fg=colors["fg"], 
                       activebackground=colors["highlight"], 
                       activeforeground=colors["fg"],
                       relief="flat",
                       bd=1)
        
        s = "shortcuts"
        start_key = self.config.get(s, "startKey", fallback="F9").upper()
        pause_key = self.config.get(s, "pauseKey", fallback="F11").upper()
        reset_key = self.config.get(s, "resetKey", fallback="F12").upper()
        quit_key = self.config.get(s, "quitKey", fallback="Ctrl+Shift+K").upper()


        # --- 功能區 ---
        menu.add_command(label=f"►{self.lang_helper.get('start')} ({start_key})", command=self.start_timer)
        menu.add_command(label=f"∥ {self.lang_helper.get('pause')} ({pause_key})", command=self.pause_timer)
        menu.add_command(label=f"↻{self.lang_helper.get('reset')} ({reset_key})", command=self.reset_timer)
        
        menu.add_separator()

        # --- 位置子選單 ---
        pos_menu = tk.Menu(menu, tearoff=0, 
                           bg=colors["bg"], 
                           fg=colors["fg"], 
                           activebackground=colors["highlight"], 
                           activeforeground=colors["fg"],
                           relief="flat",
                           bd=1)
                           
        positions = [
            (self.lang_helper.get("pos_tl"), "TL"), 
            (self.lang_helper.get("pos_tr"), "TR"), 
            (self.lang_helper.get("pos_bl"), "BL"), 
            (self.lang_helper.get("pos_br"), "BR")
        ]

        current_pos = self.position_var.get()
        for label, code in positions:
            prefix = "∨ " if current_pos == code else "    "
            pos_menu.add_command(
                label=f"{prefix}{label}",
                command=lambda c=code: self.set_position(c)
            )
        menu.add_cascade(label=f"    {self.lang_helper.get('position')}", menu=pos_menu)
        menu.add_separator()

        menu.add_command(label=f"    {self.lang_helper.get('custom_time')}", command=self.set_custom_time)
        # --- 設定檔區域 ---
        current_prof = self.profile_var.get()
        
        # Main 設定檔
        prefix = "∨ " if current_prof == "Main" else "    "
        menu.add_command(
            label=f"{prefix}{self.lang_helper.get('profile_main')}",
            command=lambda: self.change_profile("Main")
        )

        # 其他設定檔
        for section in self.config.sections():
            if section.startswith("Profile_"):
                name = self.config.get(section, "name", fallback=section)
                prefix = "∨ " if current_prof == section else "    "
                menu.add_command(
                    label=f"{prefix}{name}",
                    command=lambda s=section: self.change_profile(s)
                )
        
        menu.add_separator()
        menu.add_command(label=f"    {self.lang_helper.get('settings')}", command=self.open_settings)
        menu.add_command(label=f"    {self.lang_helper.get('reload')}", command=self.reload_config)
        menu.add_separator()
        menu.add_command(label=f"× {self.lang_helper.get('quit')} ({quit_key})", command=self.quit_app)
        
        menu.tk_popup(event.x_root, event.y_root)
        return "break"

    def create_default_ini(self):
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
thememode = system
backgroundcolor = #FFFFFF
textcolor = #000000
aheadcolor = #000000
timeoutcolor = #F87171
playwarningsound = 0
playfinishsound = 0
stopresetstimer = 0
sendontimeout = 0
showstatusindicator = 1
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