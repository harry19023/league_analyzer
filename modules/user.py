from app import app, db
from flask_login import UserMixin, LoginManager
from werkzeug.security import check_password_hash, generate_password_hash

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(user_name):
    return User.query.filter_by(username=user_name).first()


def create_user(newUsername, newPassword):
    newUser = User(username=newUsername, password_hash=generate_password_hash(newPassword))
    db.session.add(newUser)
    db.session.commit()
    return newUser

def usernameExists(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return False
    return True
