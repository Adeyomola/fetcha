from flask import request, Blueprint, render_template, g, flash
from .metadata import metadata
from .db import get_db
from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError

bp = Blueprint('schedule', __name__)
md = metadata()

@bp.route('/schedule', methods=['GET', 'POST'])
def schedule():
    table = md.tables['schedule']
    connection = get_db()
    statement = (select(table).where(table.c.user_id == g.get('user')[0]))

    if (connection.execute(statement).fetchone()) is not None:
        available_days = connection.execute(select(table).where(table.c.user_id == g.get('user')[0])).fetchone()[2]
    else:
        available_days = None
    
    if request.method == 'POST':
        error = None

        Monday = request.form.get('Monday', "")
        Tuesday = request.form.get('Tuesday', "")
        Wednesday = request.form.get('Wednesday', "")
        Thursday = request.form.get('Thursday', "")
        Friday = request.form.get('Friday', "")
        Saturday = request.form.get('Saturday', "")
        Sunday = request.form.get('Sunday', "")
        

        if Monday == "" and Tuesday == "" and Wednesday == "" and Thursday == "" and Friday == "" and Saturday == "" and Sunday == "":
            error = "Choose at least one day"
            flash(error)

        if error is None and available_days is None:
            available_days = f'{Monday}, {Tuesday}, {Wednesday}, {Thursday}, {Friday}, {Saturday}, {Sunday}'
            try:
                statement = (insert(table).values(user_id=g.get('user')[0], available_days = available_days))
                connection.execute(statement)
                connection.commit()
                return render_template('schedule.html') 
            except IntegrityError:
                connection.rollback()
        elif error is None:
                available_days = f'{Monday}, {Tuesday}, {Wednesday}, {Thursday}, {Friday}, {Saturday}, {Sunday}'
                connection.execute(update(table).where(table.c.user_id == g.get('user')[0]).values(user_id=g.get('user')[0], available_days = available_days))
                connection.commit()

    return render_template('schedule.html', available_days=available_days)