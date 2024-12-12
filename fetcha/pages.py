from flask import render_template, Blueprint, g
from .metadata import metadata
from .db import get_db
from sqlalchemy import select, insert, text
from werkzeug.exceptions import abort
from .getlocation import GetLocation


bp = Blueprint('pages', __name__)
md = metadata()

@bp.route('/<identifier>', methods=['GET', 'POST'])
def pages(identifier):    
    connection = get_db()

    # location stuff
    location = GetLocation.get_location()
    
    select_countries = text("SELECT GROUP_CONCAT(`column_name` separator ',') FROM information_schema.columns WHERE table_name = 'insights';")
    countries = connection.execute(select_countries).fetchall()

    if location not in countries[0][0]:
        query = f'ALTER TABLE insights ADD {location} varchar(10) DEFAULT 1;'
        connection.execute(text(query))
    elif location in countries[0][0]:
        count = connection.execute(text(f"SELECT {location} FROM insights WHERE identifier = '{identifier}'")).fetchone()[0]
        count = int(count)
        count = count + 1

        query = f'UPDATE insights SET {location} = {count} WHERE identifier = "{identifier}";'
        connection.execute(text(query))
        connection.commit()


    # schedule_table = md.tables['schedule']
    # get_available_days = (select(schedule_table).join_from(md.tables['users'], schedule_table))
    # available_days = connection.execute(get_available_days).fetchone()

    table = md.tables['links']
    statement = (select(table).where(table.c.identifier == identifier))
    links = connection.execute(statement).fetchone()

    if links is None:
        abort (404, f'Link does not exist')
    else:
        identifier = links[2].replace("-", " ")
    return render_template('pages.html', links=links, identifier=identifier) #available_days = available_days[2]