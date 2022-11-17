import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if __name__ == "__main__":
    with SessionLocal() as db:
        print(
            db.execute(
                """
            SELECT * FROM information_schema.tables
            WHERE table_schema = 'public'
            """
            ).fetchall()
        )
