from datetime import datetime, timedelta

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from uuid import uuid4

from flaskr import login_manager, db

@login_manager.user_loader
def login_user(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128), default=generate_password_hash('userpass'))
    picture_path = db.Column(db.Text)
    is_active = db.Column(db.Boolean, unique=False, default=False)
    create_at = db.Column(db.DateTime, default=datetime.now())
    update_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, username, email):
        self.username = username
        self.email = email
    
    @classmethod
    def select_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def select_user_by_id(cls, id):
        return cls.query.get(id)

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    def create_new_user(self):
        db.session.add(self)
    
    def save_new_password(self, new_password):
        self.password = generate_password_hash(new_password)
        self.is_active = True
    

class UserPasswordResetToken(db.Model):
    __tablename__ = 'user_password_reset_token'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(64), unique=True, index=True, default=str(uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    expire_at = db.Column(db.DateTime, default=datetime.now())
    create_at = db.Column(db.DateTime, default=datetime.now())
    update_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, token, user_id, expire_at):
        self.token = token
        self.user_id = user_id
        self.expire_at = expire_at

    @classmethod
    def publish_token(cls, user):
        token = str(uuid4())
        new_token = cls(
            token,
            user.id,
            datetime.now() + timedelta(days=1)
        )
        db.session.add(new_token)
        return token
    
    @classmethod
    def get_user_id_by_token(cls, token):
        now = datetime.now()
        record = cls.query.filter_by(token=str(token)).filter(cls.expire_at > now).first()
        if record:
            return record.user_id
        else:
            return None
    
    @classmethod
    def delete_token(cls, token):
        cls.query.filter_by(token=str(token)).delete()


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    type = db.Column(db.Integer, db.ForeignKey('project_types.id'))
    price = db.Column(db.Integer)
    time = db.Column(db.Float)

    def __init__(self, name, type, price, time):
        self.name = name
        self.type = type
        self.price = price
        self.time = time

    @classmethod
    def select_project_all(cls):
        return cls.query.all()
    
    @classmethod
    def select_project_by_id(cls, id):
        return cls.query.get(id)
    
    @classmethod
    def select_project_by_type(cls, type_id):
        return cls.query.filter_by(type=type_id).all()
    
    def create_project(self):
        db.session.add(self)
    

class ProjectType(db.Model):
    __tablename__ = 'project_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(8), unique=True)

    def __init__(self, name):
        self.name = name


class ManHour(db.Model):
    __tablename__ = 'man_hours'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    project = db.Column(db.Integer, db.ForeignKey('projects.id'))
    date = db.Column(db.Date, index=True)
    hour = db.Column(db.Float)

    def __init__(self, user_id, project_id, date, hour):
        self.user = user_id
        self.project = project_id
        self.date = date
        self.hour = hour

    @classmethod
    def select_manhours_by_user_id(cls, user_id):
        return cls.query.filter_by(user=user_id)

    @classmethod
    def select_manhours_by_project_id(cls, project_id):
        return cls.query.filter_by(project=project_id)

    @classmethod
    def select_manhours_by_date(cls, date):
        return cls.query.filter_by(date=fate)
    
    def create_manhour(self):
        db.session.add(self)