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


class RasPi(Base):
    __tablename__ = 'PiUrl'
    uuid = Column(Text, primary_key=True)
    url = Column(Text)
    landscape = Column(Boolean)
    orientation = Column(Integer)
    description = Column(Text)
    lastseen = Column(DateTime)
    ip = Column(Text)
    requested_commands = Column(Text)
    tags = relationship("Tags")
    browser = Column(Boolean)
    logs = relationship("Logs")

    def get_dict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
            dict_[key] = getattr(self, key)

        dict_['lastseen'] = str(self.lastseen)
        return dict_


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


class Logs(Base):
    __tablename__ = 'Logs'
    id = Column(Integer, primary_key=True)
    filename = Column(Text)
    log = Column(Text)
    uuid = Column(Text, ForeignKey('PiUrl.uuid'))
