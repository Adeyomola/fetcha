from flask import request, Blueprint, render_template, g, flash, redirect
import qrcode
import io
import base64
from .metadata import metadata
from .db import get_db
from sqlalchemy import insert, delete, select
import re
from sqlalchemy.exc import IntegrityError
from .auth import login_required
from .uploads import Upload

bp = Blueprint('create', __name__)
md = metadata()

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        error = None
        identifier = request.form['identifier'].replace(" ", "-")
        tagline = request.form.get('tagline', "")
        whatsapp = request.form['whatsapp']
        instagram = request.form['instagram']
        x = request.form['x']
        pinterest = request.form['pinterest']
        snapchat = request.form['snapchat']
        facebook = request.form['facebook']
        website = request.form['website']
        linkedin = request.form['linkedin']
        background_color = request.form['background-color']
        foreground_color = request.form['foreground-color']
        image_url = Upload.upload_file(Upload)

        if identifier == "":
            error = "Enter a custom name for your link"
        elif whatsapp == "" and instagram == "" and x == "" and pinterest == "" and \
            snapchat == "" and facebook == "" and website == "" and linkedin == "":
            error = "Enter at least one link"

        # create QR code
        qr_code = qrcode.make(f'https://fetcha.link/{identifier}')
        qr_code_byte = io.BytesIO()
        qr_code.save(qr_code_byte)
        qr_code = qr_code_byte.getvalue()
        qr_code = base64.b64encode(qr_code).decode()

        table = md.tables['links']
        connection = get_db()

        if error is None:
            try:
                statement = (insert(table).values(user_id=g.get('user')[0], identifier=identifier, qr_code=qr_code, tagline=tagline,
                                                    whatsapp=whatsapp, instagram=instagram, x=x,
                                                    pinterest=pinterest, snapchat=snapchat,facebook=facebook,
                                                    website=website, linkedin=linkedin, bg_color=background_color,
                                                    fg_color=foreground_color, image=image_url))
                connection.execute(statement)
                connection.commit()
                return render_template('create.html', custom_link=f"https://fetcha.link/{identifier}")
            except IntegrityError as ie:
                error = ie._message()
                connection.rollback()
                if re.search('qr_code', error):
                    error = "Link already exists! Choose a different custom name"
                elif re.search('identifier', error):
                    error = "Link already exists! Choose a different custom name"
            finally:
                connection.close()
        flash(error)
    return render_template('create.html')


@bp.route('/delete/<identifier>', methods=['GET', 'POST'])
@login_required
def delete_link(identifier):
    if request.method == 'GET':
        return redirect('/')
    
    connection = get_db()
    table = md.tables['links']

    connection.execute(delete(table).where(table.c.identifier == identifier))
    connection.commit()
    connection.close()

    return redirect("/")