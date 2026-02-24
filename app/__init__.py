import os

from flask import Flask, render_template_string
from flask_security import Security, current_user, auth_required, hash_password, \
    SQLAlchemySessionUserDatastore, permissions_accepted
from app.database import db_session, init_db
from app.models import User, Role
from app.seed import seed_db_from_json

app = Flask(__name__)
app.config['DEBUG'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

# db.init_app(app)
# fsqla.FsModels.set_db_info(db)
#
# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"


# Create app
app = Flask(__name__)
app.config['DEBUG'] = True

# Generate a nice key using secrets.token_urlsafe()
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
# Generate a good salt for password hashing using: secrets.SystemRandom().getrandbits(128)
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')
# Don't worry if email has findable domain
app.config["SECURITY_EMAIL_VALIDATOR_ARGS"] = {"check_deliverability": False}

# manage sessions per request - make sure connections are closed and returned
app.teardown_appcontext(lambda exc: db_session.close())

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)

@app.cli.command('seed_db')
def seed_db():
    if User.query.first() is None:
        seed_db_from_json(db_session)
        print('populando banco de dados a partir do json')
    else:
        print('banco ja contem dados, para começar do zero apague o arquivo test.db')

# Views
@app.route("/")
@auth_required()
def home():
    return render_template_string('Hello {{current_user.email}}!')

@app.route("/user")
@auth_required()
@permissions_accepted("user-read")
def user_home():
    return render_template_string("Hello {{ current_user.email }} you are a user!")

# one time setup
with app.app_context():
    init_db()
    # Create a user and role to test with
    security.datastore.find_or_create_role(
        name="user", permissions={"user-read", "user-write"}
    )
    db_session.commit()
    if not security.datastore.find_user(email="test@me.com"):
        security.datastore.create_user(email="test@me.com",
        password=hash_password("password"), roles=["user"])
    db_session.commit()

if __name__ == '__main__':
    # run application (can also use flask run)
    app.run()