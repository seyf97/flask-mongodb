import datetime

class DevConfig:
    SECRET_KEY = "Screw you guys, i'm going home. I'm sorry I thought this was America. I didn't hear no bell." 
    
    JWT_SECRET_KEY = 'oh my goD the Killed keNny! You *******s!!!!!!'
    JWT_TOKEN_LOCATION = ['headers']
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=3600)
    JWT_ERROR_MESSAGE_KEY = "message"  # I don't like the default "msg" key

    MONGODB_SETTINGS = {'db': 'blog',
                        'host': "localhost",
                        "port": 27017}

