from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# 创建数据库和登录管理扩展对象
# 这些对象会在应用工厂函数中与具体的Flask应用实例关联
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """应用工厂函数，用于创建和配置Flask应用实例"""
    app = Flask(__name__)

    # 从配置文件加载应用配置
    # 配置文件通常包含数据库连接信息、密钥等敏感信息
    app.config.from_pyfile('../config.py')

    # 初始化关联
    db.init_app(app)

    # 初始化登录管理扩展
    login_manager.init_app(app)

    # 设置登录视图的端点
    # 当用户需要登录时，Flask-Login会重定向到这个端点对应的视图函数
    login_manager.login_view = 'main.login'

    # 确保在应用上下文环境中注册用户加载回调函数
    # 应用上下文提供了访问应用全局变量和配置的环境
    with app.app_context():
        # 用户加载回调函数，用于从会话中存储的用户ID加载实际的用户对象
        # 这是Flask-Login扩展必需的回调函数
        @login_manager.user_loader
        def load_user(user_id):
            # 延迟导入User模型，避免循环导入问题
            from app.models import User

            # 通过用户ID查询用户对象
            # 返回None表示用户不存在，Flask-Login会处理相应的认证逻辑
            return User.query.get(int(user_id))

    # 注册路由蓝图
    # 蓝图用于组织和模块化应用的路由
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    # 在应用上下文中创建所有数据库表
    # 这会根据模型定义生成数据库模式
    # 注意：这只会创建不存在的表，不会更新已有的表结构
    with app.app_context():
        db.create_all()

    # 返回配置好的Flask应用实例
    return app