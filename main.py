from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_qrcode import QRcode
from os import path
import random
import string

app = Flask(__name__)
db = SQLAlchemy()
DB_NAME = 'database.db'
app.config['SECRET_KEY'] = 'hdugf/,ifjthshtp\jfjfbns.,djjf'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)
QRcode(app)


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main_url = db.Column(db.String())
    short_url = db.Column(db.String())

    def __init__(self, url) -> None:
        super().__init__()
        self.main_url = url
        self.short_url = self.create_short_url()

    def create_short_url(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(random.randrange(1, 9)))


with app.app_context():
    if not path.exists('website/' + DB_NAME):
        db.create_all()


@app.route('/')
def Home():
    if 'url' not in request.args:
        return render_template('home.html')

    main_url = request.args['url']
    url = Url.query.filter_by(main_url=main_url).first()
    if not url:
        url = Url(main_url)
        db.session.add(url)
        db.session.commit()

    return render_template('home.html', main_url=url.main_url, short_url=url.short_url)


@app.route('/<short_url>')
def Redirect(short_url):
    url = Url.query.filter_by(short_url=short_url).first()
    if not url:
        return redirect("/")
    return redirect(url.main_url)


if __name__ == '__main__':
    app.run(debug=True)
