from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import InstagramData, Base

# 旧SQLite接続
sqlite_engine = create_engine("sqlite:///./instagram.db")
SQLiteSession = sessionmaker(bind=sqlite_engine)
sqlite_session = SQLiteSession()

# 新PostgreSQL接続
postgres_engine = create_engine("postgresql+psycopg2://user:pass@localhost:5432/instagram")
PostgresSession = sessionmaker(bind=postgres_engine)
postgres_session = PostgresSession()

# PostgreSQLにテーブル作成
Base.metadata.create_all(bind=postgres_engine)

# データを移行
for row in sqlite_session.query(InstagramData).all():
    new_row = InstagramData(
        influencer_id=row.influencer_id,
        likes=row.likes,
        comments=row.comments,
        text=row.text
    )
    postgres_session.add(new_row)

postgres_session.commit()
sqlite_session.close()
postgres_session.close()