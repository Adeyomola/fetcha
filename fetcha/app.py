from flask import Flask, redirect, render_template, session, g
from .db import init_app, get_db
from .metadata import metadata
from sqlalchemy import select, create_engine
import os
import urllib.parse as up

md = metadata()
db_path = "./data"

secret_key=os.environ.get('SECRET_KEY')

db_password=up.quote_plus(os.environ.get('DB_PASSWORD'))
db_user=os.environ.get('DB_USER')
host=os.environ.get('DB_HOST')
db_name=os.environ.get('DATABASE')

def create_app():
    app=Flask(__name__)
    app.config.from_mapping(
        ENGINE= create_engine(f"mysql://{db_user}:{db_password}@{host}/{db_name}"),
        SECRET_KEY=secret_key
    )

    from . import auth
    app.register_blueprint(auth.bp)

    from . import create
    app.register_blueprint(create.bp)

    from . import pages
    app.register_blueprint(pages.bp)

    from . import insights
    app.register_blueprint(insights.bp)

    from . import schedule
    app.register_blueprint(schedule.bp)

    @app.route('/', methods=['GET', 'POST'])
    def home():
        if 'user_id' in session:
            table = md.tables['links']
            connection = get_db()

            statement = (select(table).where(table.c.user_id == g.get('user')[0]))
            links = connection.execute(statement).fetchall()

            return render_template('index.html', links=links)
        else:
            session.clear()
            return render_template('index.html')
    
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect('/login')
    
    
    init_app(app)
    return app