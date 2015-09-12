import shlex
import logging
from pi_director.models.models import (
    DBSession,
    MyModel,
    Tags
    )
from sqlalchemy import desc, and_

def get_pis():
    PiList=DBSession.query(MyModel).filter(MyModel.uuid!="default").order_by(desc(MyModel.lastseen)).all()
    return PiList

def get_tagged_pis(tags):
    splitter=shlex.shlex(tags)
    splitter.whitespace+=','
    splitter.whitespace+=';'
    splitter.whitespace_split=True
    taglist = list(splitter)

    taglist_str=""
    for tag in taglist:
        taglist_str+="\'{tag}\',".format(tag=tag)
    taglist_str=taglist_str.rstrip(taglist_str[-1:])    


    tagged_pis=[]

    if (len(taglist) > 1):
        query_str="""select t1.uuid,count(*) as ct 
                     from Tags t1 
                     join Tags t2 on t1.tag!=t2.tag and t1.uuid==t2.uuid
                     where 1
                     and t1.tag in ({taglist})
                     and t2.tag in ({taglist})
                     group by t1.uuid having ct >= {args};
                  """.format(taglist=taglist_str,args=len(taglist))

        result=DBSession.get_bind().execute(query_str)          

        for row in result:
            tagged_pis.append(row[0])
    else:
        PisWithTags=DBSession.query(Tags).filter(Tags.tag.in_(taglist)).all()
        for pi in PisWithTags:
            tagged_pis.append(pi.uuid)


    PiList=DBSession.query(MyModel).filter(MyModel.uuid.in_(tagged_pis)).order_by(desc(MyModel.lastseen)).all()
    return PiList

def get_pi_info(uid):
    tags=[]
    uid=request.matchdict['uid']
    row=DBSession.query(MyModel).filter(MyModel.uuid==uid).first()
    if row==None:
        row=MyModel()
        row.uuid=uid
        row.url="http://www.stackexchange.com"
        row.landscape=True
        row.lastseen=datetime.now()
        row.description=""
        DBSession.add(row)
        DBSession.flush()
    else:
        try:
            tagset=DBSession.query(Tags).filter(Tags.uuid==uid).all()
            for tag in tagset:
                tags.append(tag.tag)
        except Exception:
            pass
    rowdict={}
    rowdict['uuid']=row.uuid
    rowdict['url']=row.url
    rowdict['description']=row.description
    rowdict['landscape']=row.landscape
    rowdict['lastseen']=str(row.lastseen)
    rowdict['tags']=tags
    return rowdict

