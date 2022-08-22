from typing import List,Dict
from sqlalchemy.orm import Session
from cake_bake_app.models import CakeResponsibilities

def get_bakers_for_employees(names:List[str], session:Session)->Dict[str,str]:
    """Shifting the employees names by one to get bakers"""
    # removing all existing assigned bakers already
    resp = session.query(CakeResponsibilities.baker_name).all()
    existing_bakers = [r for (r,) in resp]
    for exst_bkr in existing_bakers:
        names.remove(exst_bkr)
    # assigning new bakers
    bakers = names[1:]
    bakers.append(names[0])
    return {baker:receiver for baker,receiver in zip(bakers,names)}