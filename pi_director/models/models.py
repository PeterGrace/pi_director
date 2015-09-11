from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Boolean,
    DateTime,
    Binary,
    ForeignKey
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'PiUrl'
    uuid = Column(Text, primary_key=True)
    url = Column(Text)
    landscape = Column(Boolean)
    description = Column(Text)
    lastseen = Column(DateTime)
    ip = Column(Text)
    tags = relationship("Tags")

class Tags(Base):
    __tablename__ = 'Tags'
    id = Column(Integer, primary_key=True)
    tag = Column(Text)
    uuid = Column(Text, ForeignKey('PiUrl.uuid'))
    __table_args__ = (Index('idx_taglist', "tag", "uuid", unique=True), )

class Screenshot(Base):
    __tablename__ = 'PiScreens'
    uuid = Column(Text, primary_key=True)
    image = Column(Binary)    
    

