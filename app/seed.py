import json
from datetime import datetime
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session, scoped_session
from flask_security.models import sqla

from app.database import Base
from app.config import Config



def seed_mock_from_json(db_session: scoped_session[Session]):

    for model in Base.__subclasses__():
        if issubclass(model, sqla.FsRoleMixin) or issubclass(model, sqla.FsUserMixin):
            continue
        filename = Path(Config.MOCK_DIR, model.__name__).with_suffix('.json')
        with open(filename) as f:
            data = json.load(f)
        for row in data:
            if "data_hora" in row.keys():
                row["data_hora"] = datetime.fromisoformat(row["data_hora"])

            row = model(**row)
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
