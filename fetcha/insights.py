from flask import render_template, Blueprint, g
from .metadata import metadata
from .db import get_db
from sqlalchemy import text
from werkzeug.exceptions import abort
from .auth import login_required


bp = Blueprint('insights', __name__)
md = metadata()

@bp.route('/insights/<identifier>', methods=['GET', 'POST'])
@login_required
def insights(identifier):    
    connection = get_db()
    
    select_countries = text("SELECT GROUP_CONCAT(`column_name` separator ', ') FROM information_schema.columns WHERE table_name = 'insights';")
    countries = connection.execute(select_countries).fetchall()[0]

    countries = list(countries)
    countries = ''.join(countries)
    countries = countries.replace(",", "")
    countries = countries.split()
    countries.remove('identifier')

    countries_string = ', '.join(countries)

    select_counts = text(f"SELECT {countries_string} FROM insights WHERE identifier='{identifier}'")
    counts = connection.execute(select_counts).fetchall()[0]
    counts = list(counts)
    counts = ', '.join(counts)


    return render_template('insights.html', identifier=identifier, counts=counts, countries=countries_string)