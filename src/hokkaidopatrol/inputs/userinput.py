from typing import List, Dict, Tuple
from .. import cities
from .distances import to_distance_dict

def user_input() -> List[str]:
    print("choose cities by number: ")
    print("\n".join(f"{k}: {v}" for k, v in cities.items()))
    data = []
    i = 1
    while True:
        city = input(f"{i}>>")
        if city == "":
            ans = input(f"ok?(Y/n): {[cities[d] for d in data]}\n>>")
            if ans in ["Y", "y"]:
                break
            else:
                continue

        if city in cities:
            print(cities[city])
            data.append(city)
            i += 1
        else:
            print("no such city", city)

    return [cities[city] for city in data], to_distance_dict(data)