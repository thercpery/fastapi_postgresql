import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm
from dotenv import load_dotenv
import os as _os

load_dotenv(".env")
DB_HOST = _os.environ.get("DB_HOST")
DB_NAME = _os.environ.get("DB_NAME")
DB_USER = _os.environ.get("DB_USER")
DB_PASS = _os.environ.get("DB_PASS")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine = _sql.create_engine(DATABASE_URL)
SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _declarative.declarative_base()
