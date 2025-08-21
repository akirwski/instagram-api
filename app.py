from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from collections import Counter
from janome.tokenizer import Tokenizer
from db import SessionLocal, InstagramData

app = FastAPI()

# DBセッション取得
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ① influencer_idで平均いいね数・コメント数を返す
@app.get("/average")
def get_average(influencer_id: str, db: Session = Depends(get_db)):
    data = db.query(InstagramData).filter(InstagramData.influencer_id == influencer_id).all()
    if not data:
        return {"error": "データが見つかりません"}
    avg_likes = sum([d.likes for d in data]) / len(data)
    avg_comments = sum([d.comments for d in data]) / len(data)
    return {
        "influencer_id": influencer_id,
        "avg_likes": avg_likes,
        "avg_comments": avg_comments
    }

# ② 平均いいね数が多い上位N件
@app.get("/top-likes")
def top_likes(n: int = Query(5), db: Session = Depends(get_db)):
    results = db.query(InstagramData.influencer_id).all()
    influencer_stats = {}
    for influencer_id, in results:
        rows = db.query(InstagramData).filter(InstagramData.influencer_id == influencer_id).all()
        avg = sum([r.likes for r in rows]) / len(rows)
        influencer_stats[influencer_id] = avg
    sorted_list = sorted(influencer_stats.items(), key=lambda x: x[1], reverse=True)[:n]
    return [{"influencer_id": i, "avg_likes": l} for i, l in sorted_list]

# ③ 平均コメント数が多い上位N件
@app.get("/top-comments")
def top_comments(n: int = Query(5), db: Session = Depends(get_db)):
    results = db.query(InstagramData.influencer_id).all()
    influencer_stats = {}
    for influencer_id, in results:
        rows = db.query(InstagramData).filter(InstagramData.influencer_id == influencer_id).all()
        avg = sum([r.comments for r in rows]) / len(rows)
        influencer_stats[influencer_id] = avg
    sorted_list = sorted(influencer_stats.items(), key=lambda x: x[1], reverse=True)[:n]
    return [{"influencer_id": i, "avg_comments": c} for i, c in sorted_list]

# ④ influencer_idごとに名詞出現頻度上位N件
@app.get("/top-words")
def top_words(influencer_id: str, n: int = Query(5), db: Session = Depends(get_db)):
    data = db.query(InstagramData).filter(InstagramData.influencer_id == influencer_id).all()
    if not data:
        return {"error": "データが見つかりません"}
    texts = " ".join([d.text for d in data if d.text])
    tokenizer = Tokenizer()
    nouns = [token.base_form for token in tokenizer.tokenize(texts) if token.part_of_speech.startswith("名詞")]
    counter = Counter(nouns)
    return dict(counter.most_common(n))