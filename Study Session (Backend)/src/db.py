from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

participant_association_table = db.Table('participant_association', db.Model.metadata,
    db.Column('study_group_id', db.Integer, db.ForeignKey('study_group.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class StudyGroup(db.Model):
    __tablename__ = 'study_group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    participants = db.relation('User', secondary=participant_association_table, back_populates='study_groups')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'Unnamed Study Group')
        # TODO change this to allow users to set a date and time
        self.date = kwargs.get('date', '')
        self.time = kwargs.get('time', '')
        self.duration = kwargs.get('duration', 1)
        self.location = kwargs.get('location', 'Nowhere')
        self.description = kwargs.get('description', '')
        self.image = kwargs.get('image')
        self.likes = 0
        self.participants = []
    
    def serialize(self):
        return {
            # 'id': self.id,
            'name': self.name,
            'date': self.date,
            'time': self.time,
            'duration': self.duration,
            'description': self.description,
            'image': self.image,
            'location': self.location,
            # 'likes': self.likes,
            # 'participants': [p.serialize() for p in self.participants]
        }

    def add_like(self):
        self.likes += 1

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)
    study_groups = db.relationship('StudyGroup', secondary=participant_association_table)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'Anonymous')
        self.netid = kwargs.get('netid', 'None')
        self.study_groups = []

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'netid': self.netid
        }

class PartnerPost(db.Model):
    __tablename__ = 'partner_post'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)
    course = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'Anonymous')
        self.netid = kwargs.get('netid', '')
        self.course = kwargs.get('course', '')
        self.description = kwargs.get('description', '')
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'netid': self.netid,
            'course': self.course,
            'description': self.description
        }

