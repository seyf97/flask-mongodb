from mongoengine import Document, StringField, ReferenceField, CASCADE


class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=100)
    last_name = StringField(max_length=100)

class Post(Document):
    title = StringField(max_length=250, required=True)
    author = ReferenceField(User, reverse_delete_rule=CASCADE)

    meta = {"allow_inheritance": True}

