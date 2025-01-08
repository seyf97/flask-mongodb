import mongoengine as me

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