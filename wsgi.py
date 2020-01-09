from app import app as application
if __name__ == '__main__':
    from database.models import db
    db.init_app(application)
    with application.app_context():
        db.create_all()
    application.run(threaded=True)