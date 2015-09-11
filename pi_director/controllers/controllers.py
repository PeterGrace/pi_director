from pi_director.models.models import (
    DBSession,
    MyModel,
    Tags
    )
from sqlalchemy import desc

def get_pis():
    PiList=DBSession.query(MyModel).filter(MyModel.uuid!="default").order_by(desc(MyModel.lastseen)).all()
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

