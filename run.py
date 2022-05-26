from main import create_app

# Call the Application Factory function to construct a Flask application instance
# using the standard configuration defined in /instance/flask.cfg
## Run as python run.py

if __name__ == '__main__':
    app = create_app('flask.cfg')
    app.run(host='0.0.0.0')
