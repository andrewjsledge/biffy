from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
app_admin = Admin(app)
toolbar = DebugToolbarExtension(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from application import admin






###
# Modules
###



# users
from application.users import config as user_config
app.config.from_object(user_config)
from application.users.views import mod as usersModule
app.register_blueprint(usersModule)

# admin
#import timetracker.admin
#from timetracker.admin import config as admin_config
#app.config.from_object(admin_config)

# Later on you'll import the other blueprints the same way:
#from app.comments.views import mod as commentsModule
#from app.posts.views import mod as postsModule
#app.register_blueprint(commentsModule)
#app.register_blueprint(postsModule)