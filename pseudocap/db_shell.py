import IPython

def dbshell():
  from server import app
  with app.app_context():
    from database import db
    import models
    print "models and db modules are available"
    IPython.embed()

if __name__ == '__main__':
    dbshell()
