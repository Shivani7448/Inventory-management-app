from flask  import Flask
from application.database import db #step 3
app = None

def create_app():
  app = Flask(__name__) #step 1
  app.debug=True #step 1
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.sqlite3'#step3
  db.init_app(app)#step3
  app.app_context().push()#step 1
  return app

app = create_app()
from application.controllers import * #step 2
# from application.models import * not required

if __name__ == '__main__': #run this app only when invoked.
  with app.app_context():
    db.create_all()
    Manager=User.query.filter_by(type="manager").first()
    if Manager is None:
      Manager=User(username="Manager1",email="manager@user.com",password="1234",type="manager")
      db.session.add(Manager)
      db.session.commit()
  app.run()

#Note: when we run this app module, it will create a proxy object as current_app which we can use later in other files and it will also avoid circular import error.mapping happens at this place.