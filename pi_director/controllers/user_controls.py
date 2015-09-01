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

