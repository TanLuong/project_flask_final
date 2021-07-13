from  flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BaseData:
    created_date = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_date = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False)

class Role(db.Model, BaseData):
    __tablename__ = 'role'
    role_id = db.Column('role_id', db.Integer, primary_key=True)
    role_name = db.Column('role_name', db.String(255), nullable=False)
    description = db.Column('description', db.Text())
    children = db.relationship('User')


class Mst_group(db.Model, BaseData):
    __tablename__ = 'mst_group'
    group_id = db.Column('group_id', db.Integer, primary_key=True)
    group_name = db.Column('group_name', db.String(255), nullable=False)
    description = db.Column('description', db.Text())
    children = db.relationship('User')


class Mst_devices(db.Model, BaseData):
    __tablename__ = 'mst_devices'
    device_id = db.Column('device_id', db.Integer, primary_key=True)
    device_code = db.Column('device_code', db.String(255), nullable=False)
    device_name = db.Column('device_name', db.String(255), nullable=False)
    type =db.Column('type', db.Integer, nullable=False)
    description = db.Column('description', db.Text())
    device_status = db.Column('device_status', db.Integer(), nullable=False)
    children = db.relationship('User_device_history')


class User(db.Model, BaseData):
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user_scure.user_id'), nullable=False, unique=True)
    group_id = db.Column('group_id', db.Integer, db.ForeignKey('mst_group.group_id'), nullable=False)
    email = db.Column('email', db.String(255), nullable=False, unique=True)
    persional_email = db.Column('persional_email', db.String(255), nullable=False)
    full_name = db.Column('full_name', db.String(255), nullable=False)
    fullname_kana = db.Column('fullname_kana', db.String(255))
    gender = db.Column('gender', db.Integer(), nullable=False)
    tel = db.Column('tel', db.String(20), nullable=False)
    skype = db.Column('skype', db.String(20), nullable=False)
    birthday = db.Column('birthday', db.Date(), nullable=False)
    onboard_date = db.Column('onboard_date', db.Date(), nullable=False)
    avatar_url = db.Column('avatar', db.String(15))
    role_id = db.Column('role_id', db.Integer, db.ForeignKey('role.role_id'))
    children = db.relationship('User_device_history')

class User_device_history(db.Model, BaseData):
    __tablename__ = 'user_device_history'
    his_id = db.Column('his_id', db.Integer, primary_key=True)
    id = db.Column('id', db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_date = db.Column('start_date', db.DateTime, nullable=False)
    end_date = db.Column('end_date', db.DateTime)
    is_deleted = db.Column('is_deleted',db.Boolean(), nullable=False)
    device_id = db.Column('device_id', db.Integer, db.ForeignKey('mst_devices.device_id'), nullable=False)


class UserScure(db.Model, BaseData):
    __tablename__ = 'user_scure'
    user_id = db.Column('user_id', db.Integer, primary_key=True)
    user_name = db.Column('user_name', db.String(20), unique=True, nullable=False)
    password = db.Column('password', db.String(255), nullable=False)
    child = db.relationship('User', backref=db.backref('user_scure'),
                             lazy='joined')
