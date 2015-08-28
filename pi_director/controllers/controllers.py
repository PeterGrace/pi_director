from pi_director.models.models import (
    DBSession,
    MyModel,
    )

def get_pis():
    PiList=DBSession.query(MyModel).filter(MyModel.uuid!="default").all()
    return PiList

