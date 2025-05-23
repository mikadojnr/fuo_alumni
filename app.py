from flask import Flask
from flask_login import current_user
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['FLASK_DEBUG'] = os.environ.get('FLASK_DEBUG', 'True')
app.config['FLASK_ENV'] = os.environ.get('FLASK_ENV', 'development')


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'img')

from extensions import db, migrate, csrf, login_manager

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
csrf.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

# Import models
from models import User, Alumni, Admin, Event, Contribution, Announcement

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
from blueprints.main import main
from blueprints.auth import auth
from blueprints.alumni import alumni
from blueprints.admin import admin
from blueprints.events import events
from blueprints.contributions import contributions

app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(alumni)
app.register_blueprint(admin)
app.register_blueprint(events)
app.register_blueprint(contributions)

# Context processors
@app.context_processor
def utility_processor():
    def current_year():
        return datetime.now().year
    
    return dict(current_year=current_year)

if __name__ == '__main__':
    app.run(debug=True)
