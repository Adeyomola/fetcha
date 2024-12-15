from flask import render_template, Blueprint, g
from .metadata import metadata
from .db import get_db
from sqlalchemy import text
from werkzeug.exceptions import abort
from .auth import login_required
from urllib.request import urlopen
import json

iso3166 = urlopen('https://gist.githubusercontent.com/ssskip/5a94bfcd2835bf1dea52/raw/59272a2d1c2122f0cedd83a76780a01d50726d98/ISO3166-1.alpha2.json')
iso3166 = json.loads(iso3166.read())

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
    # counts = ', '.join(counts)

    countries = [abbreviation.replace(abbreviation, iso3166[abbreviation]) for abbreviation in countries]
    # countries_in_full = ', '.join(countries)

    return  {"identifier": identifier, "counts": counts, "countries": countries}