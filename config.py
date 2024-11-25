import os
import json

from dotenv import load_dotenv
import boto3

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


def get_creds(secret_id: str) -> dict:
    client = boto3.client("secretsmanager", region_name="us-west-2")
    response = client.get_secret_value(SecretId=secret_id)
    raw_secret_value = response["SecretString"]
    try:
        value = json.loads(raw_secret_value)
    except json.decoder.JSONDecodeError:
        value = raw_secret_value
    return value


def create_database_uri() -> str:
    if os.environ.get("ENV") == "PROD":
        creds = get_creds("prod/db-admin-creds")
        uri = (
            f"mysql+pymysql://{creds['username']}:{creds['password']}@{creds['host']}/"
        )
    else:
        uri = "sqlite:///" + os.path.join(basedir, "app.db")
    return uri


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = create_database_uri()
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMINS = ["ed.a.nunes@gmail.com"]
    POSTS_PER_PAGE = 25
    LANGUAGES = ["en", "es"]
    MS_TRANSLATOR_KEY = os.environ.get("MS_TRANSLATOR_KEY")


from sqlalchemy import create_engine
from sqlalchemy import text

creds = {
    "username": "admin",
    "password": "s$E}WxHfDfD%iZ5jX3ExPXbT#5Zz",
    "host": "db-prod-1.czgieuo4ido7.us-west-2.rds.amazonaws.com",
}

uri = f"mysql+pymysql://{creds['username']}:{creds['password']}@{creds['host']}:3306/"
engine = create_engine(uri)
conn = engine.connect()
result = conn.execute(text("select 1"))
