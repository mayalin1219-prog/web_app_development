# 路由與頁面設計文件 (API Design)

本文件規劃了「食譜收藏系統」所有提供給使用者的頁面端點，包含路由定義、傳遞邏輯以及使用的 Jinja2 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| **首頁/列表** | `GET` | `/` | `index.html` | 顯示最新上架的系統內食譜列表。 |
| **搜尋/推薦** | `GET` | `/search` | `search.html` | 處理 query string `?q=` 或 `?ingredients=` 來進行菜單過濾。 |
| **新增頁面** | `GET` | `/recipes/create` | `recipes/create.html` | 顯示包含新增食譜資訊的表單。 |
| **建立食譜** | `POST` | `/recipes/create` | — | 接收並確認表單結果，加入 DB 後重導向至 `/`。 |
| **食譜詳情** | `GET` | `/recipes/<id>` | `recipes/detail.html` | 顯示特定食譜內容與所需食材清單。 |
| **採購清單** | `GET` | `/recipes/<id>/shopping-list`| `recipes/shopping_list.html`| 自動依據指定食譜產出所需採購的清單。 |
| **編輯頁面** | `GET` | `/recipes/<id>/edit` | `recipes/edit.html` | 送回並預填原始食譜資訊供使用者修改。 |
| **更新食譜** | `POST`| `/recipes/<id>/update` | — | 接收已修改的表單，寫入資料庫後導向到詳情頁。 |
| **刪除食譜** | `POST`| `/recipes/<id>/delete` | — | 刪除單個食譜後，重導向回到首頁。 |

---

## 2. 路由詳細說明 (Route Details)

### 2.1 主模組 (Main Blueprint)

#### `GET /`
- **處理邏輯**：呼叫 `Recipe.get_all()` 取得資料庫中按時間倒序排列的食譜。
- **輸出**：渲染 `index.html`。

#### `GET /search`
- **輸入**：URL 參數 `q` (菜名關鍵字) 或 `ingredients` (逗號分隔的現有食材)。
- **處理邏輯**：判斷若有 `ingredients` 就過濾出 `RecipeIngredient` 符合的食譜，按匹配度排序；若是 `q` 則單純做標題 `LIKE` 搜尋。
- **輸出**：渲染 `search.html`。

### 2.2 食譜模組 (Recipes Blueprint)

#### `GET /recipes/create` 與 `POST /recipes/create`
- **輸入 (POST)**：表單資料 `title`, `steps`, `description`, `image`, 及一組 `ingredients` (包含名稱、量、單位)。
- **處理邏輯**：驗證欄位是否空白。處置上傳圖片至 `static/uploads/` 取回檔名。呼叫 Model 將 `Recipe` 與 `Ingredient` 相關聯一併儲存。
- **輸出**：成功後重導向至 `url_for('main.index')`，若驗證失敗則重新渲染 `recipes/create.html` 並給予 Flash 錯誤訊息。

#### `GET /recipes/<id>`
- **輸入**：路徑參數 `<id>`。
- **處理邏輯**：呼叫 `Recipe.get_by_id(id)`，若找不到拋出 404，否則匯總資料傳送至模板。
- **輸出**：渲染 `recipes/detail.html`。

#### `GET /recipes/<id>/shopping-list`
- **輸入**：路徑參數 `<id>`。
- **處理邏輯**：藉由關聯查詢 `recipe.ingredients` 將配料轉換為購買清單格式。
- **輸出**：渲染 `recipes/shopping_list.html`。

#### `GET /recipes/<id>/edit` 與 `POST /recipes/<id>/update`
- **輸入**：修改過後的表單文字，原圖片或新圖片。
- **處理邏輯**：讀出原始料理，如為 POST 則覆蓋並寫入。
- **輸出**：重導向至 `url_for('recipes.detail', id=id)`。

#### `POST /recipes/<id>/delete`
- **處理邏輯**：確認收到發送的請求後從 DB 刪除對應 ID 的紀錄。
- **輸出**：重導向至 `url_for('main.index')`。

---

## 3. Jinja2 模板清單

將建立於 `app/templates/` 內：
1. `base.html` : 所有頁面的母版（Navbar、底圖、與 CSS/JS 引用）。
2. `index.html` : 繼承 `base.html`，首頁網格排列的食譜預覽卡片。
3. `search.html` : 繼承 `base.html`，類似於 `index.html` 但是會有查詢標頭。
4. `recipes/create.html` : 繼承 `base.html`，填詞新增表單。
5. `recipes/edit.html` : 繼承 `base.html`，覆用修改表單。
6. `recipes/detail.html` : 繼承 `base.html`，圖文並茂地展出料理步驟與圖片。
7. `recipes/shopping_list.html` : 繼承 `base.html`，單純的條列式待買清單。
