from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
db_url= "postgresql://postgres:BALAJi1234@localhost:5432/FastApi"
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind= engine)
