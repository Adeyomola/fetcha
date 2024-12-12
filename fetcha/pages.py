from flask import render_template, Blueprint, g
from .metadata import metadata
from .db import get_db
from sqlalchemy import select, insert, text
from werkzeug.exceptions import abort
from .getlocation import GetLocation


bp = Blueprint('pages', __name__)
md = metadata()

@bp.route('/<identifier>')
def pages(identifier):
    
    connection = get_db()

    # location stuff
    location = GetLocation.get_location()
    insights_table = md.tables['insights']

    if not connection.execute(select(insights_table.c.identifier)).fetchone():
        statement = (insert(insights_table).values(identifier=identifier))
        connection.execute(statement)
    else:
        return

    select_countries = (select(insights_table).where(insights_table.c.identifier == identifier))
    countries = connection.execute(select_countries).fetchone()

    print(connection.execute(select(insights_table.c.identifier)).fetchone())
    print(countries)
    
    if location in countries:
        query = f'UPDATE insights SET {location} = {location} + 1 WHERE identifier = {identifier};'
        connection.execute(text(query))
        connection.commit()
    else:
        query = f'ALTER TABLE insights ADD {location} varchar(10) SET DEFAULT 1;'
        connection.execute(text(query))
        connection.commit()
        connection.close()

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
    return render_template('pages.html', links=links, identifier=identifier, location=location) #available_days = available_days[2]