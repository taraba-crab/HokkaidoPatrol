from dataclasses import dataclass
import MySQLdb
from typing import List, Tuple
from itertools import combinations
from .cities import cities

@dataclass
class DistanceAndTime:
    departure: str
    arrival: str
    distance: float
    time: str

    def __str__(self):
        return f"('{self.departure}','{self.arrival}', {self.distance}, '{self.time}')"

    def pretty(self):
        return f"('{cities[self.departure]}','{cities[self.arrival]}', {self.distance}, '{self.time}')"

def insert(models: List[DistanceAndTime]):
    con = MySQLdb.connect(
        user="root",
        passwd="",
        host="localhost",
        db="hokkaido_patrol",
        charset="utf8"
    )
    cur = con.cursor()

    query = """
        insert into distance_and_time (
            departure,
            arrival,
            distance,
            time
        ) values """
    values = ",".join(map(str, models))
    query += values
    cur.execute(query)
    print(f"{len(models)}件insertした。")

    con.commit()
    cur.close()
    con.close()

def select(departure: str, arrival: str) -> Tuple[str, str, float, str]:
    con = MySQLdb.connect(
        user="root",
        passwd="",
        host="localhost",
        db="hokkaido_patrol",
        charset="utf8"
    )
    cur = con.cursor()
    query = """
        select * 
        from distance_and_time 
        where (departure = %s 
                and arrival = %s)
        or (departure = %s
                and arrival = %s)
        """
    cur.execute(query, (departure, arrival, arrival, departure))

    row = next(iter(cur))

    cur.close()
    con.close()

    return row

def select_list(data: List[str]) -> List[Tuple[str, str, float, str]]:
    con = MySQLdb.connect(
        user="root",
        passwd="",
        host="localhost",
        db="hokkaido_patrol",
        charset="utf8"
    )
    cur = con.cursor()
    query = """
            select * 
            from distance_and_time 
            where (departure = %s 
                    and arrival = %s)
            or (departure = %s
                    and arrival = %s)
            """

    ls = []
    for comb in combinations(data, 2):
        u, v = comb
        cur.execute(query, (u, v, v, u))
        row = next(iter(cur))
        ls.append(row)

    cur.close()
    con.close()

    return ls

