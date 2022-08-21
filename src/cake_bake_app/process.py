from typing import List,Dict

def get_bakers_for_employees(names:List[str])->Dict[str,str]:
    """Shifting the employees names by one to get bakers"""
    bakers = names[1:]
    bakers.append(names[0])
    return {baker:receiver for baker,receiver in zip(bakers,names)}