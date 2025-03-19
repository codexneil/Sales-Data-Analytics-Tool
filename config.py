import os
import urllib.parse

class Config:
    # Database connection details
    DB_SERVER = os.environ.get("DB_SERVER")
    DB_DATABASE = os.environ.get("DB_DATABASE")
    DB_USERNAME = os.environ.get("DB_USERNAME")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")

    # Connection string
    if DB_SERVER and DB_DATABASE and DB_USERNAME and DB_PASSWORD:
        DB_PASSWORD_ENCODED = urllib.parse.quote_plus(DB_PASSWORD)
        SQLALCHEMY_DATABASE_URI = (
            f"mssql+pyodbc://{DB_USERNAME}:{DB_PASSWORD_ENCODED}@{DB_SERVER}/{DB_DATABASE}"
            "?driver=ODBC+Driver+17+for+SQL+Server"
        )
    else:
        # Fallback to SQLite
        basedir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")