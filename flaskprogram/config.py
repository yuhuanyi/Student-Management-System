import os

# 基础配置
SECRET_KEY = 'key'
DEBUG = True

# 数据库配置
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'xxq.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False