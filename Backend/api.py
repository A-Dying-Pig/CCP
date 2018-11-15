from .models import *


class DatabaseError(Exception):
    def __init__(self, msg):
        super(DatabaseError, self).__init__(msg)
        self.msg = msg


def create_user(username, password, email):
    '''
    check username and email
    both be unique
    return 0 if successful
    return some str if failed
    '''
    name_unique = CCPUser.objects.filter(username=username)
    email_unique = CCPUser.objects.filter(email=email)
    if name_unique:
        return 'name repeated'
    elif email_unique:
        return 'email repeated'
    else:
        CCPUser.objects.create(username=username, password=password, email=email)
        return 0

