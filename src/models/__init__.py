from flask_sqlalchemy import SQLAlchemy

# initialize our db
db = SQLAlchemy()


from flask_bcrypt import Bcrypt
#######
# existing code remains #
#######
bcrypt = Bcrypt()
