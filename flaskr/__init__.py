from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flaskr.config import BaseConfig, TestConfig


login_manager = LoginManager()
login_manager.login_view = 'app.login'
login_manager.login_message = 'ログインしてください'

db = SQLAlchemy()
migrate = Migrate()
s3 = boto3.cilent('s3', 
    aws_access_key_id=BaseConfig.AWS_ACCESS_KEY,
    aws_secret_access_key=BaseConfig.AWS_SECRET_ACCESS_KEY)

def create_app():
    app = Flask(__name__)
    app.config.from_object(BaseConfig)
    # app.config.from_object(TestConfig)
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    from flaskr.views import bp
    app.register_blueprint(bp)
    
    return app