import shlex
import logging
from pi_director.models.models import (
    DBSession,
    RasPi,
    Tags
    )
from sqlalchemy import desc, and_

def get_pis():
    PiList=DBSession.query(RasPi).filter(RasPi.uuid!="default").order_by(desc(RasPi.lastseen)).all()
    return PiList


def get_tagged_pis(tags):
    splitter = shlex.shlex(tags)
    splitter.whitespace += ','
    splitter.whitespace += ';'
    splitter.whitespace_split = True
    taglist = list(splitter)

    taglist_str = ""
    for tag in taglist:
        taglist_str += "\'{tag}\',".format(tag=tag)
    taglist_str = taglist_str.rstrip(taglist_str[-1:])

    tagged_pis = []

    if (len(taglist) > 1):
        query_str = """
    SELECT t1.uuid,count(*) AS ct
      FROM Tags t1
      JOIN Tags t2 ON t1.tag!=t2.tag AND t1.uuid==t2.uuid
     WHERE 1
       AND t1.tag IN ({taglist})
       AND t2.tag IN ({taglist})
  GROUP BY t1.uuid
    HAVING ct >= {args}
        """.format(taglist=taglist_str, args=len(taglist))

        result = DBSession.get_bind().execute(query_str)

        for row in result:
            tagged_pis.append(row[0])
    else:
        PisWithTags = DBSession.query(Tags).filter(Tags.tag.in_(taglist)).all()
        for pi in PisWithTags:
            tagged_pis.append(pi.uuid)

    PiList = DBSession.query(MyModel).filter(MyModel.uuid.in_(tagged_pis)).order_by(desc(MyModel.lastseen)).all()
    return PiList


def get_pi_info(uid):
    tags = []
    row = DBSession.query(RasPi).filter(RasPi.uuid==uid).first()
    if row == None:
        row = RasPi()
        row.uuid = uid
        row.url = "http://www.stackexchange.com"
        row.landscape = True
        row.lastseen = datetime.now()
        row.description = ""
        DBSession.add(row)
        DBSession.flush()
    else:
        try:
            tagset = DBSession.query(Tags).filter(Tags.uuid==uid).all()
            for tag in tagset:
                tags.append(tag.tag)
        except Exception:
            pass

    rowdict = row.get_dict()
    return rowdict


def get_pi_cmd_info(uid):
    tags = []
    row = DBSession.query(RasPi).filter(RasPi.uuid == uid).first()
    if row == None:
        return []
    else:
        try:
            tagset = DBSession.query(Tags).filter(Tags.uuid==uid).all()
            for tag in tagset:
                tags.append(tag.tag)
        except Exception:
            pass

    rowdict = row.get_dict()
    return rowdict
