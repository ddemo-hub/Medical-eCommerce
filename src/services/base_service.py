from flask import render_template, session

class BaseService:
    def __init__(self):
        try:
            self.logged_in = session["logged_in"]
            self.name = session["name"]
            self.uid = session["uid"]
        except KeyError:
            self.logged_in = False
            self.name = None
            self.uid = None

    def authorization_error(self):
        return render_template("authorization_error.html")
    
    @staticmethod
    def login_required(method):
        def wrapper(self, *args, **kwargs):
            if self.logged_in == True:
                return method(self, *args, **kwargs)
            else:
                return self.authorization_error()
            
        return wrapper