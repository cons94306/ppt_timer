# ⏱️ PPT Timer

**Overlay Timer** 是一個專為演講者、簡報者與直播主設計的**輕量級、透明置頂**倒數計時器。

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Build](https://img.shields.io/badge/Built%20with-PyInstaller-orange)

## ✨ 主要特色 (Features)

* **🛡️ 永遠置頂 (Always On Top)**：穿透 PPT 全螢幕模式，始終懸浮在視覺最上層。
* **🎨 高度客製化**：可調整字體、大小、顏色、透明度、背景色。
* **♾️ 無停止邏輯**：僅提供 `開始`、`暫停`、`重置`，符合演講者的心流狀態。
* **💾 多組設定檔 (Profiles)**：快速切換不同情境（例如：5分鐘簡報、20分鐘演講）。
* **🌍 多語系支援**：內建繁體中文與英文，可透過 `language.ini` 擴充任何語言。
* **⚙️ 視覺化設定**：內建 GUI 設定編輯器，免去手動修改文字檔的麻煩。
* **🚀 綠色軟體 (Portable)**：
    * **不寫入註冊表 (No Registry)**。
    * 設定儲存於同目錄下的 `.ini` 檔。
    * 單一執行檔即可運作，隨身碟帶著走。

## 📥 安裝與執行 (Installation)

### 方法 1：直接執行 (原始碼)
確保您已安裝 Python 3.x，並安裝相依套件：

```bash
pip install keyboard screeninfo pillow
```

然後執行主程式：

```Bash
python timer.py
```

方法 2：打包成 EXE
如果您希望製作成獨立的執行檔分享給朋友：

```Bash
pyinstaller --onefile --noconsole --icon="app_icon.ico" --name="ppt_timer" --version-file="version_info.txt" ppt_timer.py
```

(請確保目錄下有名為 timer.ico 的圖示檔，否則請移除 --icon 參數)
## 🎮 操作說明 (Controls)

### 🖱️ 滑鼠操作
- **左鍵拖曳**：移動計時器位置  
  （若設定為固定位置，移動後會自動切換為手動模式）
- **左鍵雙擊**：關閉程式
- **右鍵點擊**：開啟功能選單  
  （開始 / 暫停 / 重置 / 設定 / 切換設定檔）


### ⌨️ 全域快捷鍵 (Hotkeys)

即使視窗沒有焦點（例如正在操作 PPT），快捷鍵依然有效。

| 功能 | 預設按鍵 | 說明 |
|---|---|---|
| 開始 (Start) | F9 | 開始倒數計時 |
| 暫停 (Pause) | F10 | 暫停計時（再次按下不會恢復，需按開始） |
| 重置 (Reset) | F12 | 重置回初始時間 |
| 離開 (Quit) | Ctrl + Shift + K | 完全關閉程式 |

> ⚙️ 快捷鍵可在設定選單中自定義

## ⚙️ 設定說明 (Configuration)

本程式依賴目錄下的兩個設定檔，若檔案不存在，程式啟動時會自動生成預設值。

### 1️⃣ timer_config.ini（主設定檔）
- 儲存視窗外觀、時間長度、快捷鍵與所有 Profile 設定
- 可透過右鍵選單 > **「⚙ 設定...」** 進行圖形化編輯
- 支援新增 / 刪除不同的 Profile  
  （例如：10 分鐘、30 分鐘）

### 2️⃣ language.ini（語系檔）
- 儲存介面文字
- 程式啟動時會自動讀取此檔案
- 預設包含：
  - `[zh_TW]`（繁體中文）
  - `[en_US]`（English）

#### ➕ 如何新增語言？
1. 開啟 `language.ini`
2. 複製整個 `[en_US]` 區塊
3. 將 `[en_US]` 改為新的語言代碼（例如：`[ja_JP]`）
4. 翻譯等號右邊的文字
5. 重新啟動程式或重讀設定，即可在設定頁面切換語言


## ⚠️ 常見問題 (FAQ)

**Q: 防毒軟體報毒？**  
A: 因為程式使用了 `keyboard` 模組進行全域快捷鍵監聽（其底層原理與 Keylogger 類似），  
某些敏感的防毒軟體可能會誤判。這屬於正常現象，請將程式加入信任清單。

**Q: 快捷鍵失效？**  
A: 請嘗試右鍵選單中的 **「⟳ 重新讀取設定」**，  
此操作會重新註冊系統熱鍵。

**Q: 設定檔刪壞了怎麼辦？**  
A: 直接刪除 `timer_config.ini` 或 `language.ini`，  
重新開啟程式後，系統會自動建立全新的預設設定檔。

## 📝 License
MIT License. Free to use and modify.
