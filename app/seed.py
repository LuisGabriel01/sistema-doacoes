from sqlalchemy.orm import scoped_session

def seed_db_from_json(db_session: scoped_session, filename):
    if filename is None:
        filename = '../mock_data.json'
    with open(filename) as f:
        pass

