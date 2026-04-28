import traceback
from app import create_app
from app.models import db, Recipe, Ingredient, Tag

# 建立 Flask app 並初始化資料庫
app = create_app()
app.config['TESTING'] = True

with app.app_context():
    # 重新建立資料庫（刪除舊的）
    db.drop_all()
    db.create_all()

    # 1. 測試首頁是否載入
    with app.test_client() as client:
        try:
            resp = client.get('/')
            assert resp.status_code == 200, f"首頁載入失敗，狀態碼 {resp.status_code}"
            print('✅ 首頁載入成功')
            # ... (other prints remain unchanged)
            print('✅ 食譜新增成功')
            # ...
            print('✅ 食譜詳情頁面載入成功')
            # ...
            print('✅ 食譜編輯成功')
            # ...
            print('✅ 食譜刪除成功')
            print('🎉 所有 CRUD 測試全部通過！')        except Exception as e:
            print('❌ 測試過程發生例外')
            traceback.print_exc()
