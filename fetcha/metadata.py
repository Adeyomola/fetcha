from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, Text, ForeignKey, NVARCHAR, Boolean, VARCHAR
import datetime

def metadata():
    md = MetaData()

    users = Table(
    'users', md, 
    Column('id', Integer, primary_key = True, autoincrement=True),
    Column('username', String(255), unique=True),
    Column('firstname', String(255)),
    Column('lastname', String(255)),
    Column('password', String(255)),
    Column('email', String(255), unique=True)
        )
    links = Table(
    'links', md,
    Column('id', Integer, primary_key = True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('identifier', String(255), unique=True),
    Column('qr_code', String(1500)),
    Column('tagline', String(150)),
    Column('whatsapp', String(255)),
    Column('instagram', String(255)),
    Column('x', String(255)),
    Column('pinterest', String(255)),
    Column('snapchat', String(255)),
    Column('facebook', String(255)),
    Column('website', String(255)),
    Column('linkedin', String(255)),
    Column('bg_color', String(20)),
    Column('fg_color', String(20)),
    )
    schedule = Table(
    'schedule', md,
    Column('id', Integer, primary_key = True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('available_days', VARCHAR(355), unique=True, default="Monday, Tuesday, Wednesday, Thursday, Friday"),
    )
    images = Table(
    'images', md,
    Column('id', Integer, primary_key = True, autoincrement=True),
    Column('identifier', String(255), unique=True),
    Column('image', String(3000)),
    )
    return md