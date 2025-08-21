from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLiteファイルを使用
DATABASE_URL = "sqlite:///./instagram.db"

# エンジン作成
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# セッション作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデルベース
Base = declarative_base()

# Instagramデータのテーブル定義
class InstagramData(Base):
    __tablename__ = "instagram_data"

    id = Column(Integer, primary_key=True, index=True)
    influencer_id = Column(String, index=True)
    likes = Column(Integer)
    comments = Column(Integer)
    text = Column(String)

# テーブルを作成
Base.metadata.create_all(bind=engine)
