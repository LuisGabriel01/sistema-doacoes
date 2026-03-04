from sqlalchemy import select
from sqlalchemy.orm import Session, scoped_session
from app.models import Assistido
import json


def seed_db_from_json(db_session: scoped_session[Session]):
    # if filename is None:
    filename = "mock_data.json"
    with open(filename) as f:
        data = json.load(f)
    # print(data)
    for line in data:
        # print(line, type(line))
        assistido = Assistido(**line)
        db_session.add(assistido)

    print(*db_session.execute(select(Assistido)).all())
    db_session.commit()
    
