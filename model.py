from mongoengine import Document, StringField, ReferenceField, CASCADE, DateTimeField
import datetime

class User(Document):
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    salt = StringField()

class Article(Document):
    title = StringField(required=True)
    content = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now(datetime.UTC))
    author = ReferenceField(User, reverse_delete_rule=CASCADE)
    category = StringField()
    last_edited = DateTimeField()

    meta = {"allow_inheritance": True}

