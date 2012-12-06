# import the User object
from fanmento.users.models import User, FacebookToken
from passlib.hash import sha256_crypt

import logging

class GaeAuthBackend:
    def authenticate(self, username=None, password=None):
        # Try to find a user matching your username
        q = User.all()
        q.filter("email =", username)

        user = q.get()
        if not user:
            return None

        for t in user.facebooktoken_set:
            logging.info(t.token)
            if sha256_crypt.verify(password, t.token):
                return user

        if user.password:
            if sha256_crypt.verify(password, user.password):
                return user

        return None

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        q = User.all()
        q.filter("email =", user_id)

        return q.get()
