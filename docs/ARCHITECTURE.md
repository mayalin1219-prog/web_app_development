# 食譜收藏系統 - 系統架構文件

## 1. 技術架構說明

根據 PRD 需求，本專案將採用輕量且高效的單體式架構 (Monolithic Architecture) 進行開發：

- **選用技術與原因**：
  - **後端框架：Python + Flask**  
    Flask 是一個輕量級的微框架 (Micro-framework)，具有極高的靈活性。對於個人使用的食譜收藏系統，不需要過多龐雜的內建功能，Flask 能讓我們用最直覺的程式碼快速建立應用程式。
  - **模板引擎：Jinja2**  
    因為我們的架構不使用前後端分離，Jinja2 能直接在伺服器端將後端的資料嵌入 HTML 中進行渲染，省去了前後端 API 串接與前端狀態管理的開發成本。
  - **資料庫：SQLite (搭配 SQLAlchemy ORM)**  
    對於個人級別的寫入與讀取，SQLite 的效能早已綽綽有餘，最大的好處是不必另外架設與維護資料庫伺服器。搭配 SQLAlchemy 可以用 Python 語法操作資料庫，且內建防護手段可避免 SQL Injection。

- **Flask MVC 模式說明**：
  - **Model (模型)**：由 SQLAlchemy 定義，負責定義與管理系統的資料結構（包含 `Recipe`, `Tag`, `Ingredient` 等資料表）以及與 SQLite 的讀寫互動。
  - **View (視圖)**：由 Jinja2 模板 (Templates) 和前端靜態資源組成，負責接收從 Controller 獲得的資料，渲染並顯示 UI 給使用者觀看。
  - **Controller (控制器)**：由 Flask 的路由 (Routes) 扮演，負責接收前端瀏覽器發送來的 HTTP 請求，判斷業務邏輯、調用 Model 獲取或更新系統資料，最後決定要交給哪一個 View 渲染回傳。

---

## 2. 專案資料夾結構

以下是本專案的資料夾與檔案結構規劃：

```text
recipe_collection_app/
├── app/                 # 應用程式的主體程式碼
│   ├── __init__.py      # Flask 應用程式初始化、綁定資料庫與設定檔
│   ├── models.py        # 資料庫模型 (DB Schema & SQLAlchemy Models)
│   ├── routes.py        # Flask 路由處理邏輯 (Controller)
│   ├── templates/       # Jinja2 HTML 模板 (View)
│   │   ├── base.html    # 網頁共用版型 (包含 Header, Footer 等)
│   │   ├── index.html   # 首頁 / 現有食譜列表
│   │   ├── form.html    # 新增與編輯食譜的表單頁面
│   │   └── search.html  # 搜尋與推薦結果頁面
│   └── static/          # 靜態資源檔案
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   └── main.js
│       └── uploads/     # 系統運行時使用者上傳的食譜圖片存放區
├── instance/
│   └── database.db      # SQLite 資料庫實體檔案 (由程式自動生成)
├── config.py            # 系統環境與相關組態設定變數
├── requirements.txt     # Python 開發與部署套件依賴清單
└── app.py               # 專案啟動入口
```

---

## 3. 元件關係圖

以下展示各元件在一個典型使用者請求（例如瀏覽菜單列表）中的互動關係：

```mermaid
graph TD
    Browser[瀏覽器 / 使用者] -->|1. 發送 HTTP 請求 (GET/POST)| Route[Flask Route <br> (Controller)]
    Route -->|2. 讀寫資料請求| Model[Model <br> (SQLAlchemy -> SQLite)]
    Model -->|3. 回傳查詢結果 / 確認儲存| Route
    Route -->|4. 傳遞資料與上下文| Template[Jinja2 Template <br> (View)]
    Template -->|5. 根據資料渲染出 HTML| Route
    Route -->|6. 回傳完整的 HTML 頁面| Browser
```

---

## 4. 關鍵設計決策

1. **不採用前後端分離架構 (Server-Side Rendering)**  
   為了達成 MVP 並確保快速上線，我們將採用 Server-side rendering 而非現代常見的 React/Vue 前後端分離開發。這決定可以幫助我們專注在核心的食譜邏輯，且維護上只需單一的程式碼庫即可運作。

2. **採用 SQLAlchemy 處理資料存取**  
   在專案中不直接撰寫原生的 SQL 語法，以 SQLAlchemy 作為對象關聯對映 (ORM)，不僅使程式碼更加物件導向且易讀，在未來若有需要轉移資料庫供應商時也能無痛移轉。

3. **使用者上傳圖片存放於 File System 而非資料庫**  
   針對食譜圖片，我們選擇將實體檔案放在 `app/static/uploads/`，且資料庫僅存儲檔案的路徑或檔名。這可以避免將圖片轉成長二進位資料 (Blob) 塞進 SQLite 中而導致檔案龐大與存取緩慢的問題。

4. **抽離設定檔與機密資訊**  
   將環境變數與安全設定統一放到 `config.py` 或 `.env` 檔案中，並利用 `.gitignore` 排除 SQLite `instance/` 資料庫擋與使用者上傳的 `uploads/`。這樣能保證程式碼在上傳到 GitHub 時，不會附帶使用者的私密資料。
