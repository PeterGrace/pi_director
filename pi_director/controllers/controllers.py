from pi_director.models.models import (
    DBSession,
    MyModel,
    )
from sqlalchemy import desc

def get_pis():
    PiList=DBSession.query(MyModel).filter(MyModel.uuid!="default").order_by(desc(MyModel.lastseen)).all()
    return PiList

