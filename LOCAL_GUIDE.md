# 🦝 SDGs 永續小遊戲平台：本地端（Local）運行與配置教學

本專案是一個基於 **Flask (Python)** 的全端網頁應用程式。本指南將一步步引導您在本地端電腦（Windows / macOS）配置並流暢運行本專案！

---

## 🛠️ 運行前準備步驟

請確保您的電腦上已安裝以下基礎工具：
1. **Python 3.11 或以上版本**（請前往 [Python 官網](https://www.python.org/downloads/) 下載並安裝，安裝時務必勾選 **「Add Python to PATH」**）。
2. **Git**（用於代碼管理與推送）。

---

## 🚀 本地端運行五步指南

### 第一步：進入專案資料夾
開啟您的終端機（Windows 請使用 **PowerShell** 或 **CMD**；macOS 請使用 **Terminal**），切換到本專案所在的根目錄資料夾（路徑請替換為您電腦上的實際專案路徑）：
```bash
# 請將下方路徑替換成您電腦上專案資料夾的真實路徑
cd <您的專案實際資料夾路徑>
```
*   **範例路徑**（若放在 Windows 桌面）：
    ```bash
    cd c:\Users\brian\Desktop\網頁期末PROJECT\project
    ```

### 第二步：建立並啟用 Python 虛擬環境 (venv)
為了避免 Python 套件版本與您電腦上的其他專案產生衝突，強烈建議建立一個獨立的虛擬環境：

*   **Windows 系統 (PowerShell)**：
    ```powershell
    # 建立虛擬環境
    python -m venv venv
    # 啟用虛擬環境
    .\venv\Scripts\Activate.ps1
    ```
    *(如果出現權限錯誤，可先執行 `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` 後再啟用。)*

*   **macOS / Linux 系統**：
    ```bash
    # 建立虛擬環境
    python3 -m venv venv
    # 啟用虛擬環境
    source venv/bin/activate
    ```

> [!NOTE]
> 啟用成功後，您的終端機提示字元最前方會出現 `(venv)` 的標記，代表您已成功進入獨立沙盒環境！

### 第三步：安裝專案依賴套件
在虛擬環境啟用狀態下，一鍵安裝專案所需的所有第三方套件（如 Flask、SQLAlchemy、Argon2 等）：
```bash
pip install -r requirements.txt
```
*(若遇到 pip 版本提示，可依照提示執行 `pip install --upgrade pip` 進行更新。)*

### 第四步：配置環境變數檔案 (`.env`)
專案根目錄下已為您準備好了 **`.env`** 配置文件（已自動被 `.gitignore` 排除，不會上傳至 GitHub，保障安全性）：

1.  用文字編輯器開啟根目錄下的 `.env`。
2.  找到 `GEMINI_API_KEY` 欄位：
    ```ini
    GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
    ```
3.  前往 [Google AI Studio](https://aistudio.google.com/) 免費申請一個 Gemini API Key，並將其替換掉 `YOUR_GEMINI_API_KEY_HERE`。這將會完美開通吉祥物「小灰」的 AI 聊天對話功能！
4.  `DATABASE_URL` 本地預設使用 SQLite，您**不需要做任何變更**。系統在啟動時會自動在本地端建立一個輕量化的 `local.db` 檔案，非常簡便！

### 第五步：啟動本地伺服器
在虛擬環境中，直接執行以下指令啟動 Flask 服務：
```bash
python main.py
```
*(或者，您也可以直接在專案目錄下雙擊執行內建的 **`run.bat`** 批次檔，它會自動為您完成虛擬環境啟用與專案啟動！)*

*   當終端機印出：
    `* Running on http://127.0.0.1:5000`
*   代表本地端伺服器已成功運行！此時打開瀏覽器，訪問 **`http://127.0.0.1:5000`** 即可完美體驗您的網頁與所有小遊戲囉！🎉

---

## ❓ 常見問題排除 (FAQ)

### Q1：點擊小遊戲或排行榜時跳出「500 系統錯誤」？
*   **原因**：這通常代表資料庫連線初始化失敗。
*   **排除方式**：本地端預設會使用 SQLite（`local.db`）。請確保您的 `.env` 檔案中 `DATABASE_URL` 設定為 `sqlite:///local.db`，且專案資料夾沒有權限唯讀的問題。程式在啟動時會自動完成資料庫 Table 的建置與初始遊戲數據注入。

### Q2：如何將本地的修改發布到 Render 雲端？
本專案已在 Render 上配置了 Git 連動自動部署，只要您在本地完成修改，在終端機依序輸入：
```bash
git add .
git commit -m "您的修改描述"
git push
```
Render 就會自動抓取您的最新 commit，並在 1~2 分鐘內自動將修改發布上線！

---

祝您期末專案順利拿到 100 分滿分！如有任何問題，小灰隨時在後台支援您！🦝🌱🐾🌲
