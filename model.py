from mongoengine import Document, StringField, ReferenceField, DateTimeField, CASCADE
import datetime

class User(Document):
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    salt = StringField()

    def to_dict(self) -> dict:
        return {
            "_id": str(self.pk),
            "email": self.email
        }

class Article(Document):
    title = StringField(required=True)
    content = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now(datetime.UTC))
    author = ReferenceField(User, reverse_delete_rule=CASCADE)
    category = StringField()
    last_edited = DateTimeField()

    def to_dict(self) -> dict:
        return {
            "_id": str(self.pk),
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "author": str(self.author.pk),
            "category": self.category,
            "last_edited": self.last_edited.isoformat() if self.last_edited else None
        }
