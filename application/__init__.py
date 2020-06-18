from flask import Flask

from config import Config

from flask_mongoengine import MongoEngine

app=Flask(__name__)

app.config.from_object(Config)


db=MongoEngine()

db.init_app(app)


from application import routes

 # ws_source_id = SelectField("Source Account Id",coerce=int,validators=[InputRequired()])
    # ws_source_type = StringField("Source Account Type",validators=[DataRequired()])
    # ws_target_id = SelectField("Target Account Id",coerce=int,validators=[InputRequired()])
    # ws_target_type = StringField("Target Account Type",validators=[DataRequired()])