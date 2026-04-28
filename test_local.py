import traceback
from app import create_app

app = create_app()
app.config['TESTING'] = True

with app.test_client() as client:
    try:
        response = client.get('/')
        print(f"Status: {response.status_code}")
        print(response.data.decode('utf-8'))
    except Exception as e:
        print("EXCEPTION CAUGHT:")
        traceback.print_exc()
