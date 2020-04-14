from random import choices
from distance import get_distance_and_time
from hokkaidopatrol import db
from hokkaidopatrol import cities
from itertools import islice, combinations

def random_choice(k, delta=5):
    if delta < 1:
        print("1秒以上の間隔を空けましょう。")
        return

    for i in range(k):
        u, v = choices(list(cities.keys()), k=2)
        print(cities[u], "から", cities[v], f"({u} -> {v})")
        km, t = get_distance_and_time(u, v, delta)
        print("距離:", km, "時間", t)
        print("-"*10)
        yield u, v, km, t

def confirm_and_make_model(u: str, v: str, delta=5):
    if delta < 1:
        print("1秒以上の間隔を空けましょう。")
        return

    print(cities[u], "から", cities[v], f"({u} -> {v})")
    km, t = get_distance_and_time(u, v, delta)
    print("距離:", km, "時間", t)
    print("-" * 10)
    return db.DistanceAndTime(u, v, km, t)


def register():
    print(cities)
    n = len(cities)
    print(n, "個の二つの組み合わせの数: ", n * (n - 1) // 2)

    # random_iter = random_choice(10, delta=2)
    combs = combinations(cities, 2)

    split = 100
    times = (n * (n - 1) // 2) // split + 1
    print(times, "回に分けてinsertします")

    total = 0
    for i in range(times):
        print(i + 1, "回目のinsert:")
        models = [confirm_and_make_model(u, v, 1) for u, v in islice(combs, split)]
        db.insert(models)
        print("-" * 10)
        total += len(models)

    print(f"合計: {total}件insertした。")

if __name__ == "__main__":
    pass
