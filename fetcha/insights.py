from flask import render_template, Blueprint, g
from .metadata import metadata
from .db import get_db
from sqlalchemy import select, insert, text
from werkzeug.exceptions import abort
from .getlocation import GetLocation


bp = Blueprint('insights', __name__)
md = metadata()

@bp.route('/insights', methods=['GET', 'POST'])
def insights(identifier='third'):    
    connection = get_db()
    
    select_countries = text("SELECT GROUP_CONCAT(`column_name` separator ',') FROM information_schema.columns WHERE table_name = 'insights';")
    # select_countries = text("SELECT name FROM pragma_table_info('insights')")
    countries = connection.execute(select_countries).fetchall()[1:]


    # select_counts = text(f"SELECT {countries} FROM insights WHERE identifier='{identifier}'")
    # counts = connection.execute(select_counts).fetchall()


    return render_template('insights.html', identifier=identifier,  countries=countries) #available_days = available_days[2]