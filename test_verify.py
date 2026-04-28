import traceback
from app import create_app
from app.models import db, Recipe

app = create_app()
app.config['TESTING'] = True

with app.app_context():
    # 重新建立資料庫
    db.drop_all()
    db.create_all()
    print('Database rebuilt')

    with app.test_client() as client:
        try:
            # 1. Home page
            resp = client.get('/')
            assert resp.status_code == 200, f'Home page load failed: {resp.status_code}'
            print('STEP 1: Home page OK')

            # 2. Create recipe
            new = {
                'title': 'Test Recipe',
                'description': 'desc',
                'steps': 'step1\nstep2',
                'image_path': ''
            }
            resp = client.post('/recipes', data=new, follow_redirects=True)
            assert resp.status_code == 200, f'Create recipe failed: {resp.status_code}'
            print('STEP 2: Create recipe OK')

            # Get recipe ID
            recipe = Recipe.query.filter_by(title='Test Recipe').first()
            assert recipe is not None, 'Created recipe not found'

            # 3. Detail page
            resp = client.get(f'/recipes/{recipe.id}')
            assert resp.status_code == 200, f'Detail page failed: {resp.status_code}'
            print('STEP 3: Detail page OK')

            # 4. Edit recipe
            edit = {
                'title': 'Updated Recipe',
                'description': recipe.description,
                'steps': recipe.steps,
                'image_path': recipe.image_path
            }
            resp = client.post(f'/recipes/{recipe.id}/update', data=edit, follow_redirects=True)
            assert resp.status_code == 200, f'Edit recipe failed: {resp.status_code}'
            updated = Recipe.query.get(recipe.id)
            assert updated.title == 'Updated Recipe', 'Title not updated'
            print('STEP 4: Edit recipe OK')

            # 5. Delete recipe
            resp = client.post(f'/recipes/{recipe.id}/delete', follow_redirects=True)
            assert resp.status_code == 200, f'Delete recipe failed: {resp.status_code}'
            assert Recipe.query.get(recipe.id) is None, 'Recipe still exists after delete'
            print('STEP 5: Delete recipe OK')

            print('ALL TESTS PASSED')
        except Exception as e:
            print('TEST FAILED')
            traceback.print_exc()
