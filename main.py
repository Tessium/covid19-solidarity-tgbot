from app import app
from models import db, Demo


if __name__ == '__main__':

    # Create the tables.
    db.connect()
    print(db.create_tables([Demo]))
    db.close()
    app.run(debug=True)
