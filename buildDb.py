from main import create_app, db

#this will just create the DB tables
#run as below:
# (venv) c:\PythonWorkspace\MyFlaskAPI>python buildDb.py

app = create_app('flask.cfg')
with app.app_context():
    db.drop_all()
    db.create_all()