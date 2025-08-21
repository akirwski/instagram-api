import pandas as pd
from sqlalchemy.orm import Session
from db import SessionLocal, InstagramData
import const as const


def load_csv_to_db():
    file_path = const.FILENAME
    df = pd.read_csv(file_path)
    session = SessionLocal()

    for _, row in df.iterrows():
        record = InstagramData(
            influencer_id=row["influencer_id"],
            likes=row["likes"],
            comments=row["comments"],
            text=row["text"]
        )
        session.add(record)
    session.commit()
    session.close()
    print("Successfully loaded the csv file to the DB")