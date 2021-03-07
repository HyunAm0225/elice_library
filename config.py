import os
import json
import pymysql


BASE_DIR = os.path.dirname(__file__)

db = {
    'user': 'elice',
    'password': 'admin1234',
    'host': 'elice-kdt-ai-track-vm-racer-49.koreacentral.cloudapp.azure.com',
    'port': '3306',
    'database': 'main'
}

SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
