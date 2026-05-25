# 專案 Git Commit 歷史紀錄分析

## 程式介紹區

本專案是一個基於 **Flask** 開發的互動式網頁應用程式，主要結合了 **AI 聊天**、**聯合國永續發展目標 (SDGs)** 介紹以及**互動小遊戲**（如 Clicking Earth 與問答測驗）。

專案的主要目錄與檔案結構如下：

*   **`main.py`**: 應用程式的主要進入點，負責路由設定、API 串接與後端核心邏輯。
*   **`models.py`**: 定義資料庫模型結構，負責儲存玩家分數 (`PlayerScore`) 與小遊戲紀錄 (`MiniGame`)。
*   **`static/`**: 存放前端相關的靜態資源檔案，包含網頁的 CSS 樣式表、JavaScript 互動腳本、遊戲的視覺素材與圖片，以及存放 HTML 模板的 `templates` 資料夾。
*   **`utils/`**: 存放輔助工具與腳本檔案。
*   **`instance/`**: 通常用於存放本機開發用的 SQLite 資料庫檔案 (`.db`)。
*   **`run.bat`**: Windows 環境下使用的自動化批次腳本，便於快速設定環境並啟動伺服器。
*   **`requirements.txt`**: 列出專案所需的 Python 第三方針對套件與版本資訊。

---

根據目前的 Git 歷史紀錄，本專案的開發歷程可以分為以下幾個主要階段：

## 開發歷程摘要

### 1. 專案初始化與首頁建置 (2026-03-27 ~ 2026-03-30)
*   **初始建置**：建立了專案基礎結構 (`first commit`)。
*   **首頁實作**：完成了包含導覽列、主要內容區塊、以及 **AI 聊天視窗** (AI Chat) 的初始 `index.html` 首頁佈局。
*   **程式碼重構**：更新了 `main.py` 的邏輯流程與結構，並加入了錯誤日誌與 API 測試工具以確保系統穩定性。

### 2. SDG 永續發展目標功能實作 (2026-04-27 ~ 2026-04-29)
*   **目標頁面**：完成了 17 個聯合國永續發展目標 (SDGs) 的個別詳細介紹頁面模板 (`templates`)。
*   **介面完善**：加入了共用的頁首 (header) 與頁尾 (footer)，並更新了主導覽列的邏輯以正確連結各個目標頁面。

### 3. 互動遊戲與資料庫整合 (2026-04-27 ~ 2026-04-29)
*   **資料庫模型**：新增了玩家分數 (`PlayerScore`) 與小遊戲 (`MiniGame`) 的資料庫模型 (Models)。
*   **遊戲與測驗**：實作了問答測驗 (Quiz) 的模板以及第一個小遊戲。
*   **部署準備**：隱藏了敏感的金鑰與密碼，並整理出 `requirements.txt` 為後續部署做準備。

### 4. 環境優化與 Clicking Earth 小遊戲 (2026-05-04 ~ 2026-05-07)
*   **環境一致性**：新增了 `.gitignore`、自動化設定腳本 (如 `run.bat`)，以及確保 UTF-8 編碼的 `requirements.txt`。
*   **資料庫初始化**：實作了包含 AI 聊天整合的首頁佈局，並初始化了本機端的資料庫。
*   **Clicking Earth**：新增了「點擊地球 (Clicking Earth)」小遊戲，包含了互動式的使用者介面 (UI) 與相關的遊戲素材 (Assets)。

---

## 詳細 Commit 紀錄

| Commit Hash | 日期 | 描述 (Commit Message) |
| :--- | :--- | :--- |
| `9cb1242` | 2026-05-07 | feat: add Clicking Earth mini-game with interactive UI and assets |
| `2ce0df3` | 2026-05-04 | feat: implement main index page layout with AI chat integration and initialize local database |
| `95aee49` | 2026-05-04 | TO PHONE SCREEN |
| `244db83` | 2026-05-04 | chore: add UTF-8 encoded requirements file for environment consistency |
| `939c258` | 2026-05-04 | chore: add .gitignore and automated setup script for project environment |
| `efef6a7` | 2026-05-04 | docs: add markdown file to document git history analysis process |
| `6fe826b` | 2026-04-29 | 部署準備：隱藏金鑰與密碼並加入 requirements.txt |
| `47a6f57` | 2026-04-29 | feat: add individual goal detail templates for all 17 SDGs and update main navigation logic |
| `16c081f` | 2026-04-29 | refactor: cleanup scratch scripts, integrate quiz template, and update model schema |
| `fd61e3a` | 2026-04-29 | feat: add PlayerScore and MiniGame models and implement quiz template |
| `c860f75` | 2026-04-27 | 1st game |
| `98f6df3` | 2026-04-27 | feat: implement 17 static goal detail templates and add footer and header |
| `6f9c40d` | 2026-04-27 | feat: implement 17 SDG goal templates, index page layout, and supportive automation scripts |
| `a7b5f67` | 2026-04-27 | complete 17 goals wesute frame |
| `6d88054` | 2026-03-30 | refactor: update main.py to improve code structure and logic flow |
| `7632af1` | 2026-03-30 | feat: add error logging and API testing utility files to project structure |
| `09a4d09` | 2026-03-29 | refactor: update main entry point logic to improve execution flow |
| `a85996a` | 2026-03-27 | feat: Add initial homepage with navigation, AI chat, SDG goals, and interactive sections. |
| `d3995b5` | 2026-03-27 | feat: Add initial index.html page with navigation, content sections, and an AI chat window. |
| `d3fbae8` | 2026-03-27 | feat: Add initial `index.html` page with header, navigation, main content sections, and an AI chat window. |
| `a580d0e` | 2026-03-27 | first commit |
