import mongoengine as me
import datetime

class User(me.Document):
    email = me.EmailField(required=True, unique=True)
    image = me.URLField()

    password = me.StringField(required=True)
    salt = me.StringField()

    def to_dict(self) -> dict:
        return {
            "_id": str(self.pk),
            "email": self.email,
            "image": self.image
        }

class Article(me.Document):
    title = me.StringField(required=True)
    content = me.StringField(required=True)
    created_at = me.DateTimeField(default=datetime.datetime.now(datetime.UTC))
    author = me.ReferenceField(User, reverse_delete_rule=me.CASCADE)
    category = me.StringField()
    last_edited = me.DateTimeField()

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
