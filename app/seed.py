import json
from datetime import datetime
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session, scoped_session
from flask_security.models import sqla
from flask_security.core import Security
from flask_security.utils import hash_password

from app.database import Base
from app.config import Config


def seed_mock_users_roles(db_session: scoped_session[Session], security: Security):
        with open(Path(Config.MOCK_DIR, 'roles', encoding='utf-8').with_suffix('.json')) as f:
             roles = json.load(f)
        for role in roles:
            security.datastore.find_or_create_role(**role)
        db_session.commit()

        with open(Path(Config.MOCK_DIR, 'users', encoding='utf-8').with_suffix('.json')) as f:
             users = json.load(f)
        for user in users:
            user['password'] = hash_password(user['password'])
            if not security.datastore.find_user(email=user['email']):
                security.datastore.create_user(**user)
        db_session.commit()

def seed_mock_from_json(db_session: scoped_session[Session]):
    for model in Base.__subclasses__():
        if issubclass(model, sqla.FsRoleMixin) or issubclass(model, sqla.FsUserMixin):
            continue
        filename = Path(Config.MOCK_DIR, model.__name__).with_suffix('.json')
        with open(filename, encoding='utf-8') as f:
            data = json.load(f)
        for row in data:
            if "data_hora" in row.keys():
                row["data_hora"] = datetime.fromisoformat(row["data_hora"])
            row = model(**row)
            db_session.add(row)
        db_session.commit()
        print(db_session.execute(select(model)).all())