# import the User object
from fanmento.users.models import User, FacebookToken
from passlib.hash import sha256_crypt

import logging

class GaeAuthBackend:
    # Create an authentication method
    # This is called by the standard Django login procedure
    def authenticate(self, username=None, password=None):
        # Try to find a user matching your username
        q = User.all()
        q.filter("email =", username)

        user = q.get()
        if not user:
            return None

        #  Check the password is the reverse of the username
        if user.password:
            logging.info("Verifying password") 
            if sha256_crypt.verify(password, user.password):
                # Yes? return the Django user object
                return user
        else:
            logging.info("Verifying token") 
            for t in user.facebooktoken_set:
                logging.info(t.token)
                if sha256_crypt.verify(password, t.token):
                    return user

        # No? return None - triggers default login failed
        return None

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        q = User.all()
        q.filter("email =", user_id)

        return q.get()
