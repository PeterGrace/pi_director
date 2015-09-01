from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    )

from pi_director.models.models import Base

class UserModel(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    email = Column(Text,unique=True)
    AccessLevel = Column(Integer)

Index('EmailIndex', UserModel.email, unique=True, mysql_length=255)

