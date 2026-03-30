import json
from pathlib import Path
from flask import Flask
from sqlalchemy_utils import database_exists
# from flask import render_template_string, render_template
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
from app.seed import seed_mock_from_json, seed_mock_users_roles
from app.config import Config
from app.routes.home import homes
from app.routes.registro import registro_blueprint
from app.routes.doacao import doacao_blueprint
from app.routes.cadastro import cadastro_blueprint
# from app.routes.tabela import tabelas


app = Flask(__name__)
app.config.from_object(Config)

# manage sessions per request - make sure connections are closed and returned
app.teardown_appcontext(lambda exc: db_session.close())

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)

@app.cli.command("seed_mock")
def seed_mock():
    db_file = Path(Config.DATABASE_FILENAME)
    if database_exists(Config.SQLALCHEMY_DATABASE_URI):
        raise(FileExistsError(f'Arquivo do banco de dados existe em {db_file.absolute()}'))
    with app.app_context():
        init_db()
        seed_mock_users_roles(db_session, security)
        seed_mock_from_json(db_session)
        print("populando banco de dados a partir do json")

app.register_blueprint(homes)
app.register_blueprint(registro_blueprint)
app.register_blueprint(cadastro_blueprint)
app.register_blueprint(doacao_blueprint)
# app.register_blueprint(tabelas)

if __name__ == "__main__":
    # run application (can also use flask run)
    app.run()

