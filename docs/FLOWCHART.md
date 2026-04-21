# 食譜收藏系統 - 流程圖與路由設計

這份文件介紹了使用者在「食譜收藏系統」裡的操作路徑，系統的內部資料流，以及基礎的路由設計規劃。

## 1. 使用者流程圖 (User Flow)

這張圖描述了使用者進入網站後，如何尋找、新增以及管理自己的食譜庫：

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B[首頁 - 現有食譜列表]
    B --> C{你想做什麼？}
    
    C -->|新增| D[點擊新增按鈕]
    D --> E[填寫表單：名稱、食材、步驟、標籤與上傳圖片]
    E --> F[儲存並返回首頁]

    C -->|搜尋 / 尋找靈感| G[進入搜尋區塊]
    G --> H{依據何種方式尋找？}
    H -->|輸入菜名關鍵字| I[搜尋結果列表]
    H -->|輸入現有食材或標籤| J[系統推薦食譜列表]
    I --> K[查看詳細食譜頁面]
    J --> K

    C -->|直接從清單選擇| K
    
    K --> L{查看食譜時的操作}
    L -->|編輯| M[進入編輯模式，修改內容後儲存]
    M --> K
    L -->|刪除| N[確認刪除]
    N --> B
    L -->|生成清單| O[點選自動生成採購清單]
    O --> P[顯示缺少的食材採買清單]
```

---

## 2. 系統序列圖 (Sequence Diagram)

這張序列圖描述了「使用者新增一個新食譜並上傳圖片」時，各個系統元件之間完整的資料流動過程：

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (View)
    participant Route as Flask路由 (Controller)
    participant Model as SQLAlchemy (Model)
    participant FS as 檔案系統 (uploads/)
    participant DB as SQLite資料庫

    User->>Browser: 填寫食譜內容與選擇圖片並送出
    Browser->>Route: 發送 POST /recipes/create 請求
    
    Note over Route, FS: 處理圖片上傳
    Route->>FS: 儲存圖片至 static/uploads/
    FS-->>Route: 圖片儲存成功，回傳路徑
    
    Note over Route, DB: 將資料與圖片路徑寫入 DB
    Route->>Model: 建立 Recipe, Ingredient, Tag 物件
    Model->>DB: 執行 INSERT INTO 寫入資料庫
    DB-->>Model: 寫入成功
    Model-->>Route: 回報資料層處理完成
    
    Route-->>Browser: 回傳 HTTP 302 (Redirect) 重導向到首頁
    Browser->>User: 顯示包含新菜色的食譜列表
```

---

## 3. 功能清單與路由對照表

根據架構與 MVP 需求，初步規劃出前端需要對接的 Flask 路由，涵蓋 GET 與 POST 等基礎操作：

| 系統功能 | URL 路徑 (路由) | HTTP 方法 | 描述與動作 |
| --- | --- | --- | --- |
| **首頁與列表** | `/` | `GET` | 首頁，顯示所有食譜列表（預設以最新建立排序） |
| **新增食譜頁面** | `/recipes/create` | `GET` | 顯示提供使用者填寫食譜資料的表單介面 |
| **處理新增食譜** | `/recipes/create` | `POST` | 處理表單送出事件，儲存圖片與寫入資料庫 |
| **單一食譜細節** | `/recipes/<id>` | `GET` | 顯示該食譜的詳細步驟、圖文說明與現有食材 |
| **編輯食譜頁面** | `/recipes/<id>/edit` | `GET` | 顯示編輯介面，並代入該食譜既有的資料 |
| **處理編輯食譜** | `/recipes/<id>/edit` | `POST` | 處理覆蓋或更新資料庫中的食譜資料 |
| **刪除食譜** | `/recipes/<id>/delete` | `POST` | 要求從資料庫中將指定的食譜徹底刪除 |
| **搜尋/推薦 API** | `/search` | `GET` | 使用者透過查詢字串 (`?q=...` 或 `?ingredients=...`) 進行菜色與食材的關鍵字反查 |
| **產生採購清單** | `/recipes/<id>/shopping-list` | `GET` | 系統計算並回傳該食譜推薦的採購清單細節頁面 |
