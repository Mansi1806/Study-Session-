# maybe use this to convert between JSON and Python when dealing with datetime 
# https://stackoverflow.com/questions/10805589/convert-json-date-string-to-python-datetime

import json
from db import db, StudyGroup, User, PartnerPost
from flask import Flask, request
import datetime

app = Flask(__name__)
# TODO make a more creative database name
db_filename = 'study.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/api/study_groups/')
def get_all_groups():
    groups = StudyGroup.query.all()
    res = {'success': True, 'data': {'sessions': [g.serialize() for g in groups]}}
    return json.dumps(res), 200

@app.route('/api/study_groups/', methods=['POST'])
def create_group():
    post_body = json.loads(request.data)
    name = post_body.get('name', '')
    date = post_body.get('date')
    time = post_body.get('time')
    duration = post_body.get('duration', 1)
    location = post_body.get('location', 'Nowhere')
    description = post_body.get('description', '')
    image = post_body.get('image')

    group = StudyGroup(
        name=name,
        date=date,
        time=time,
        duration=duration,
        location=location,
        description=description,
        image=image
    )

    db.session.add(group)
    db.session.commit()
    data = group.serialize()
    # data['participants'] = []
    return json.dumps({'success': True, 'data': {'sessions': data}}), 201

@app.route('/api/study_group/<int:group_id>/', methods=['DELETE'])
def delete_group(group_id):
    group = StudyGroup.query.filter_by(id=group_id).first()
    if not group:
        return json.dumps({'success': False, 'error': 'Study group not found'}), 404
    db.session.delete(group)
    db.session.commit()
    return json.dumps({'success': True, 'data': group.serialize()}), 200

@app.route('/api/likes/<int:group_id>/', methods=['POST'])
def add_like(group_id):
    group = StudyGroup.query.filter_by(id=group_id).first()
    if not group:
        return json.dumps({'success': False, 'error': 'Study group not found. You should get some sleep.'}), 404
    group.add_like()
    db.session.commit()
    return json.dumps({'success': True, 'data': group.serialize()}), 201

@app.route('/api/users/')
def get_users():
    users = User.query.all()
    res = {'success': True, 'data': [u.serialize() for u in users]}
    return json.dumps(res), 200

@app.route('/api/users/', methods=['POST'])
def create_user():
    post_body = json.loads(request.data)
    name = post_body.get('name', 'Anonymous')
    netid = post_body.get('netid', 'None')
    user = User(
        name=name,
        netid=netid
    )
    db.session.add(user)
    db.session.commit()
    data = user.serialize()
    data['study_groups'] = []
    return json.dumps({'success': True, 'data': data}), 201

@app.route('/api/user/<int:user_id>/')
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found.'}), 404
    data = user.serialize()
    data['study_groups'] = [g.serialize() for g in user.study_groups]
    return json.dumps({'success': True, 'data': data}), 200

@app.route('/api/study_group/<int:group_id>/add/', methods=['POST'])
def add_user_to_group(group_id):
    group = StudyGroup.query.filter_by(id=group_id).first()
    if not group:
        return json.dumps({'success': False, 'error': 'Study group not found. You should get some sleep.'}), 404
    post_body = json.loads(request.data)
    user_id = post_body.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    group.participants.append(user)
    db.session.commit()
    return json.dumps({'success': True, 'data': group.serialize()}), 200

@app.route('/api/partners/')
def get_all_partner_posts():
    posts = PartnerPost.query.all()
    res = {'success': True, 'data': {'posts': [p.serialize() for p in posts]}}
    return json.dumps(res), 200

@app.route('/api/partners/', methods=['POST'])
def create_partner_post():
    post_body = json.loads(request.data)
    name = post_body.get('name', 'Anonymous')
    netid = post_body.get('netid', '')
    course = post_body.get('course', '')
    description = post_body.get('description', '')

    post = PartnerPost(
        name=name,
        netid=netid,
        course=course,
        description=description
    )

    db.session.add(post)
    db.session.commit()

    return json.dumps({'success': True, 'data': post.serialize()}), 200

@app.route('/api/partner/<int:id>/', methods=['DELETE'])
def delete_partner_post(id):
    post = PartnerPost.query.filter_by(id=id).first()
    if not post:
        return json.dumps({'success': False, 'error': 'Post not found'}), 404
    db.session.delete(post)
    db.session.commit()
    return json.dumps({'success': True, 'data': post.serialize()}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)