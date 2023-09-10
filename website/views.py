from flask import Blueprint, request, render_template, redirect, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Url
import random
import string
import json


def create_short_url():
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(random.randrange(1, 9)))


views = Blueprint('views', __name__)


@views.route('/')
def home():
    if 'url' not in request.args:
        return render_template('home.html', user=current_user)

    main_url = request.args['url']

    if current_user.is_authenticated:
        url = Url.query.filter_by(
            main_url=main_url, user_id=current_user.id).first()
        if not url:
            url = Url(main_url=main_url, short_url=create_short_url(),
                      user_id=current_user.id)
            print(url.user_id)
            db.session.add(url)
            db.session.commit()
    else:
        url = Url.query.filter_by(main_url=main_url, user_id=0).first()
        if not url:
            url = Url(main_url=main_url, short_url=create_short_url(),
                      user_id=0)
            db.session.add(url)
            db.session.commit()

    return render_template('home.html', user=current_user, main_url=url.main_url, short_url=url.short_url)


@views.route('/<short_url>')
def redirect(short_url):
    url = Url.query.filter_by(short_url=short_url).first()
    if url:
        return render_template('redirect.html', user=current_user, url=url)

    return render_template('redirect.html', user=current_user)


@views.route('/delete-url', methods=['POST'])
def delete_url():
    url = json.loads(request.data)
    urlId = url['urlId']
    url = Url.query.get(urlId)
    if url:
        if url.user_id == current_user.id:
            db.session.delete(url)
            db.session.commit()
    return jsonify({})


@views.route('/clicks', methods=['POST'])
def clicks():
    url = json.loads(request.data)
    urlId = url['urlId']
    url = Url.query.get(urlId)
    if url:
        url.clicks = url.clicks + 1
        db.session.commit()
    return jsonify({})
