from datetime import datetime, timedelta

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from sqlalchemy import and_
from uuid import uuid4

from flaskr import login_manager, db

@login_manager.user_loader
def login_user(user_id):
    return User.query.get(user_id)

# ユーザー
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128), default=generate_password_hash('userpass'))
    picture_path = db.Column(db.Text)
    is_active = db.Column(db.Boolean, unique=False, default=False)
    is_admin = db.Column(db.Boolean, unique=False, default=False)
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
    
# パスワード初期化
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

# プロジェクト
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
    def select_project_by_id(cls, id):
        return cls.query.get(id)
    
    @classmethod
    def select_project_by_type(cls, type_id):
        return cls.query.filter_by(type=type_id).all()
    
    def create_project(self):
        db.session.add(self)
    
# プロジェクトの種類(開発・運用・保守等)
class ProjectType(db.Model):
    __tablename__ = 'project_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(8), unique=True)

    def __init__(self, name):
        self.name = name

# プロジェクトにおけるユーザの工数割り当て
class ProjectAssigned(db.Model):
    __tablename__ = 'project_assigned'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    project = db.Column(db.Integer, db.ForeignKey('projects.id'))
    hour = db.Column(db.Float)

    def __init__(self, user_id, project_id, hour):
        self.user = user_id
        self.project = project_id
        self.hour = hour
    
    @classmethod
    def select_project_assigned_by_user_id(cls, user_id):
        return cls.query.filter_by(user=user_id)
    
    @classmethod
    def select_project_assigned_by_project_id(cls, project_id):
        return cls.query.filter_by(project=project_id)

    def create_project_assigned(self):
        db.session.add(self)

# ユーザの工数
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

class TimeCard(db.Model):
    __tablename__ = 'timecards'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.Date, default=None)
    start = db.Column(db.DateTime, default=None)
    end = db.Column(db.DateTime, default=None)
    working_hours = db.Column(db.Float, default=0)

    def __init__(self, user_id, date=datetime.today()):
        self.user = user_id
        self.date = date
    
    def punch_in(self, punch_time=None):
        self.start = self._make_fix_punch_time(punch_time)
        self.calc_working_hours()

    def punch_out(self, punch_time=None):
        self.end = self._make_fix_punch_time(punch_time)
        self.calc_working_hours()
    
    def _make_fix_punch_time(self, punch_time):
        if punch_time:
            punch_time = punch_time
        else:
            punch_time = datetime.now()
        hour = punch_time.hour
        minute = punch_time.minute

        if 1 <= minute <= 15:
            minute = 15
        elif 16 <= minute <= 30:
            minute = 30
        elif 31 <= minute <= 45:
            minute = 45
        elif 46 <= minute <= 59:
            minute = 0
            hour += 1 
        punch_time = datetime(punch_time.year, punch_time.month, punch_time.day, hour, minute)
        return punch_time
    
    def calc_working_hours(self):
        try:
            hours = ((self.end - self.start).seconds / 60) / 60
            self.working_hours = hours - 1 if hours >= 4.5 else hours
        except Exception as e:
            print(e)
        finally:
            db.session.add(self)


    @classmethod
    def select_today_timecard_by_user_id(cls, user_id):
        return cls.query.filter_by(user=user_id, date=datetime.today().strftime('%Y-%m-%d')).first()
    
    @classmethod
    def select_monthly_timecards_by_user_id(cls, user_id, year, month):
        target = f'{year}-{month}%'
        return cls.query.filter(
            and_(
            cls.user==user_id,
            cls.date.like(target)
            )
        ).order_by(cls.date).all()
    
    @classmethod
    def select_target_timecard_by_date(cls, user_id, date):
        return cls.query.filter_by(user=user_id, date=date).first()
