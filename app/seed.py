from sqlalchemy import select
from sqlalchemy.orm import Session, scoped_session
from flask_security.models import sqla

from datetime import datetime

# from app.models import Assistido
import app.models as models
from app.database import db
import json


def seed_db_from_json(db_session: scoped_session[Session]):
    for model in db.__subclasses__():
        if issubclass(model, sqla.FsRoleMixin) or issubclass(model, sqla.FsUserMixin):
            continue
        name = model.__name__
        filename = f"mock_data/{name}.json"
        with open(filename) as f:
            data = json.load(f)
            # print(data)
        for line in data:
            # print(line, type(line))
            if "data_hora" in line.keys():
                line["data_hora"] = datetime.fromisoformat(line["data_hora"])
                # print(line, line["data_hora"])

            # print(line)
            row = model(**line)
            db_session.add(row)
        db_session.commit()
        print(db_session.execute(select(model)).all())


    # # if filename is None:
    # filename = "mock_data.json"
    # with open(filename) as f:
    #     data = json.load(f)
    # # print(data)
    # for line in data:
    #     # print(line, type(line))
    #     assistido = Assistido(**line)
    #     db_session.add(assistido)

    # print(*db_session.execute(select(Assistido)).all())
    # db_session.commit()
