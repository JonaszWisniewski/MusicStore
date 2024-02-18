from django.contrib.sessions.backends.db import SessionStore as DbSessionStore

class SessionStore(DbSessionStore):
    def cycle_key(self): # ensures the session key isn't cleared upon logging in
        pass

    