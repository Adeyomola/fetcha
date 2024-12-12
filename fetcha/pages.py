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
    insights_table = md.tables['insights']

        # checks if insights has identifier and inserts if it doesn't
    if not connection.execute(select(insights_table.c.identifier)).fetchone():
        connection.execute((insert(insights_table).values(identifier=identifier)))
        connection.commit()
    
    select_countries = text("SELECT GROUP_CONCAT(`column_name` separator ',') FROM information_schema.columns WHERE table_name = 'insights';")
    countries = connection.execute(select_countries).fetchall()

    count = connection.execute(text(f"SELECT {location} FROM 'insights' WHERE identifier = '{identifier}'")).fetchone()

    if location not in countries[0][0]:
        print ('True')
        query = f'ALTER TABLE insights ADD {location} varchar(10) DEFAULT 1;'
        connection.execute(text(query))
    elif location in countries[0][0]:
        # count = count + 1
        query = f'UPDATE insights SET {location} = + 1 WHERE identifier = "{identifier}";'
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
    return render_template('pages.html', links=links, identifier=identifier, count=count) #available_days = available_days[2]