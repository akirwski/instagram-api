# test_api.py
import pytest
from fastapi.testclient import TestClient
from main import app, get_db  # あなたのFastAPIアプリのファイル名が main.py の場合
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base, InstagramData


# 既存の SQLite DB を指定
SQLALCHEMY_DATABASE_URL = "sqlite:///./instagram.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# ---- テストデータ ----
@pytest.fixture(scope="function")
def test_db():
    db = TestingSessionLocal()
    yield db
    # テスト後は削除
    db.query(InstagramData).delete()
    db.commit()

# ---- テストケース ----
# 本来であれば、引数として入り値の想定範囲を見極め、最小最大値などのテストケースを作成するべきだが、今回はシンプルにした。)
def test_get_average(test_db):
    response = client.get("/average?influencer_id=1")
    assert response.status_code == 200
    data = response.json()
    assert data["influencer_id"] == "1"
    assert data["avg_likes"] == 119515.75
    assert data["avg_comments"] == 1586.0833333333333

def test_top_likes(test_db):
    response = client.get("/top-likes?n=3")
    assert response.status_code == 200
    data = response.json()
    assert data[2]["influencer_id"] == "57"
    assert data[2]["avg_likes"] == 66156.91666666667

def test_top_comments(test_db):
    response = client.get("/top-comments?n=5")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["influencer_id"] == "1"
    assert data[0]["avg_comments"] == 1586.0833333333333
    
def test_top_words():
    response = client.get("/top-words", params={"influencer_id": "1", "n": 5})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    for word, count in data.items():
        assert isinstance(word, str)
        assert isinstance(count, int)