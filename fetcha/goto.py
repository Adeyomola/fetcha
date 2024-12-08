from flask import render_template, Blueprint, g
from .metadata import metadata
from .db import get_db
from sqlalchemy import select
from werkzeug.exceptions import abort


bp = Blueprint('goto', __name__)
md = metadata()

@bp.route('/<identifier>')
def goto(identifier):
    table = md.tables['links']
    image_table = md.tables['images']
    connection = get_db()

    statement = (select(table).where(table.c.identifier == identifier))
    links = connection.execute(statement).fetchone()

    statement = (select(image_table).where(image_table.c.identifier == identifier))
    images = connection.execute(statement).fetchone()

    schedule_table = md.tables['schedule']
    get_available_days = (select(schedule_table).join_from(md.tables['users'], schedule_table))
    available_days = connection.execute(get_available_days).fetchone()
    
    if links is None:
        abort (404, f'Link does not exist')
    else:
        identifier = links[2].replace("-", " ")
    return render_template('pages.html', links=links, identifier=identifier, images=images, available_days = available_days[2])