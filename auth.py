from flask_login import LoginManager, current_user, login_user, logout_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# from linuxtools import WORKING_DIR
WORKING_DIR ='/srv/time-station-server'


class CustomLoginManager(LoginManager):
    def init(self, app):
        self.login_view = "login"
        self.login_message = u"Please log in to access this page."
        self.refresh_view = "reauth"
        self.init_app(app)


class User(UserMixin):
    def __init__(self, id, name, active=True):
        self.id = id
        self.name = name
        self.password_hash = self.get_hash_from_file()
        self.active = active

    def login(self):
        login_user(self)

    def logout(self):
        logout_user()

    def is_authenticated(self):
        return current_user.is_authenticated

    def is_active(self):
        return self.active

    def set_password(self, password):
        # self.password_hash = generate_password_hash(password)
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.get_hash_from_file(), password)

    def get_hash_from_file(self):
        try:
            with open("%s/hashsum" % WORKING_DIR, 'r') as file:
                return file.readline()
        except Exception:
            with open("%s/hashsum" % WORKING_DIR, 'w') as file:
                hash = 'pbkdf2:sha256:150000$E2I3Cw3z$8ecc8767638927252cc68cfe91cdb0f2cd3f000b612ca02f04fe4003414a8889'
                # hash = 'pbkdf2:sha256:150000$a43rWzb7$565cd4f7a19685b637cdb99f39f2e4b85b9b7180bfb5e4f07318516570b59519'
                file.write(hash)
                return hash

    def change_password(self, new_password):
        hash = generate_password_hash(new_password)
        with open("%s/hashsum" % WORKING_DIR, 'w') as file:
            # print("WIRTING HASH TO FILE: "+hash)
            file.write(hash)
            return
