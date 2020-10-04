import yaml

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flaskr.config import BaseConfig, TestConfig

# import boto3


login_manager = LoginManager()
login_manager.login_view = 'app.login'
login_manager.login_message = 'ログインしてください'

mail = Mail()
migrate = Migrate()
db = SQLAlchemy()
with open('/var/www/flask_on_ec2/flaskr/config.yml', encoding='utf-8') as file:
    conf = yaml.safe_load(file)
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
    mail.init_app(app)

    return app