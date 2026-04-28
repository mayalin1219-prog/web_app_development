# 路由設計文件 (Routes Design)

本文件根據產品需求文件 (PRD)、系統架構設計 (ARCHITECTURE) 與資料庫設計 (DB_DESIGN)，規劃「食譜收藏系統」的路由結構與頁面流程。

## 1. 路由總覽表格

| 功能模組 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 (食譜列表) | GET | `/` | `index.html` | 顯示所有食譜列表（可分頁或全部顯示） |
| 食譜詳情 | GET | `/recipes/<int:id>` | `detail.html` | 顯示單筆食譜詳細資訊（含步驟、食材、標籤） |
| 新增食譜頁面 | GET | `/recipes/new` | `form.html` | 顯示建立食譜表單 |
| 建立食譜 | POST | `/recipes` | — | 接收表單資料，存入 DB，完成後重導向至首頁或詳情頁 |
| 編輯食譜頁面 | GET | `/recipes/<int:id>/edit` | `form.html` | 顯示編輯食譜表單（預先填入舊資料） |
| 更新食譜 | POST | `/recipes/<int:id>/update` | — | 接收表單資料，更新 DB，完成後重導向至詳情頁 |
| 刪除食譜 | POST | `/recipes/<int:id>/delete` | — | 刪除指定食譜，完成後重導向至首頁 |
| 搜尋與推薦頁面 | GET | `/search` | `search.html` | 顯示關鍵字搜尋或食材推薦的表單與結果 |
| 標籤列表 | GET | `/tags` | `tags.html` | 顯示所有標籤列表 |
| 新增標籤 | POST | `/tags` | — | 接收表單建立新標籤 |
| 刪除標籤 | POST | `/tags/<int:id>/delete` | — | 刪除指定標籤 |
| 採購清單 | GET | `/shopping-list` | `shopping_list.html` | 根據使用者加入的食譜，自動生成並顯示所需食材採購清單 |

## 2. 每個路由的詳細說明

### 首頁 (食譜列表)
- **輸入**: 無 (可選的 `page` 查詢參數)
- **處理邏輯**: 呼叫 `Recipe` Model 獲取食譜清單，若有分頁需求則進行分頁處理。
- **輸出**: 渲染 `index.html`
- **錯誤處理**: 若無資料，於畫面顯示「目前尚無食譜，請新增第一筆」。

### 新增/編輯/刪除食譜 (Recipe CRUD)
- **輸入**: 
  - 表單欄位：`title`, `description`, `steps`, `image` (檔案上傳), `ingredients` (動態欄位), `tags`。
  - URL 參數：`id` (編輯/刪除時)。
- **處理邏輯**: 
  - 新增/更新：驗證必填欄位 (title, steps)，處理圖片上傳並儲存至 `static/uploads/`，建立或更新 `Recipe`, `Ingredient`, `Tag` 以及關聯表。
  - 刪除：從 `Recipe` 表刪除該筆資料，並刪除對應關聯與實體圖片檔案。
- **輸出**:
  - GET: 渲染 `form.html`
  - POST: 重導向至 `/` 或 `/recipes/<id>`
- **錯誤處理**: 表單驗證失敗時，附帶錯誤訊息並重新渲染 `form.html`。若請求不存在的 `id`，回傳 404 頁面。

### 搜尋與推薦
- **輸入**: URL Query String 包含 `keyword` (搜尋菜名/描述) 或 `ingredients` (逗號分隔的食材名)。
- **處理邏輯**: 根據提供的參數查詢 `Recipe` 與 `Ingredient` 關聯。若是食材反查，則找出包含目標食材的食譜。
- **輸出**: 渲染 `search.html` 顯示結果。
- **錯誤處理**: 未提供參數則顯示空表單；查無結果則顯示提示訊息。

### 標籤管理
- **輸入**: 表單欄位 `name`。
- **處理邏輯**: 新增或刪除 `Tag`，刪除時同時清除 `RECIPE_TAGS` 中的關聯。
- **輸出**: GET 渲染 `tags.html`，POST 重導向至 `/tags`。

### 採購清單
- **輸入**: 使用者在 Session 或 DB 中儲存的「待採買食譜清單」。
- **處理邏輯**: 查詢所有選定食譜的食材與用量，將相同食材的用量加總（若單位可換算）。
- **輸出**: 渲染 `shopping_list.html`。

## 3. Jinja2 模板清單

- `templates/base.html`: 共用版型（包含 Header、Footer、導覽列）。
- `templates/index.html`: 繼承 `base.html`，食譜列表首頁。
- `templates/detail.html`: 繼承 `base.html`，單筆食譜詳情頁。
- `templates/form.html`: 繼承 `base.html`，食譜的新增與編輯共用表單。
- `templates/search.html`: 繼承 `base.html`，搜尋表單與結果呈現。
- `templates/tags.html`: 繼承 `base.html`，標籤管理介面。
- `templates/shopping_list.html`: 繼承 `base.html`，採購清單顯示頁。

## 4. 路由骨架程式碼結構

已經在 `app/routes/` 目錄建立對應模組的 Python 檔案骨架：
- `app/routes/recipes.py` (處理食譜 CRUD)
- `app/routes/search.py` (處理搜尋與推薦)
- `app/routes/tags.py` (處理標籤管理)
- `app/routes/shopping_list.py` (處理採購清單)
- `app/routes/main.py` (處理首頁)
