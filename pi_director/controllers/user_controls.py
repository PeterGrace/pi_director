from pyramid.response import Response
from pi_director.models.models import (
    DBSession,
    MyModel,
    )
from pi_director.models.UserModel import UserModel


def authorize_user(email):
    user=DBSession.query(UserModel).filter(UserModel.email==email).one()
    user.AccessLevel=2
    DBSession.flush()

def delete_user(email):
    DBSession.query(UserModel).filter(UserModel.email==email).delete()

def get_users():
    UserList=DBSession.query(UserModel).all()
    return UserList


def make_an_admin(request):
    email=request.matchdict['email']

    '''First, make sure there aren't already admins in the system'''
    res=DBSession.query(UserModel).filter(UserModel.AccessLevel==2).first()
    if res != None:
        msg="User already an admin: {user}".format(user=res.email)
        return False
    user=DBSession.query(UserModel).filter(UserModel.email==email).first()
    user.AccessLevel=2
    DBSession.flush()    
    return True


