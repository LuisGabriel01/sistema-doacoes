from datetime import datetime
from flask import Flask, render_template_string, render_template
# from flask_security import (
#     current_user,
#     auth_required,
#     permissions_accepted,
# )
from flask_security.core import Security
from flask_security.utils import hash_password
from flask_security.datastore import SQLAlchemySessionUserDatastore

from app.database import db_session, init_db
from app.models import User, Role
from app.seed import seed_db_from_json
from app.config import Config
from app.routes.home import homes


app = Flask(__name__)
app.config.from_object(Config)

# manage sessions per request - make sure connections are closed and returned
app.teardown_appcontext(lambda exc: db_session.close())

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)


@app.cli.command("seed_db")
def seed_db():
    with app.app_context():
        init_db()
        # Create a user and role to test with
        security.datastore.find_or_create_role(
            name="user", 
            permissions={"user-read", "user-write"}
        )
        db_session.commit()

        if not security.datastore.find_user(email="test@me.com"):
            security.datastore.create_user(
                email="test@me.com", 
                password=hash_password("password"), 
                roles=["user"],
            )
        db_session.commit()

        seed_db_from_json(db_session)
        print("populando banco de dados a partir do json")


app.register_blueprint(homes)

if __name__ == "__main__":
    # run application (can also use flask run)
    app.run()

