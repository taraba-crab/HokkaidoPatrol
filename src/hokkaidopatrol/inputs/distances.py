from typing import Dict, List, Tuple
from .. import cities
from .. import db

def to_distance_dict(data: Dict[str, Dict[str, float]]):
    ls: List[Tuple[str, str, float, str]] = db.select_list(data)
    d = {cities[city]: {} for city in data}
    for u_, v_, distance, _ in ls:
        u, v = cities[u_], cities[v_]
        d[u][v] = distance
        d[v][u] = distance

    return d