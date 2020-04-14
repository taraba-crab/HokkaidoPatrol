from __future__ import annotations
from typing import TypeVar, Tuple, Type
from abc import ABC, abstractmethod

T = TypeVar("T", bound="Chromosome")


# 遺伝的アルゴリズムにおける染色体の4つの基本機能
#   適応度関数
#   ランダムに選んだ遺伝子でインスタンスを作る(第一世代で使う)
#   交差
#   変異
class Chromosome(ABC):
    @abstractmethod
    def fitness(self) -> float:
        ...

    @classmethod
    @abstractmethod
    def random_instance(cls: Type[T]) -> T:
        ...

    @abstractmethod
    def crossover(self: T, other: T) -> Tuple[T, T]:
        ...

    @abstractmethod
    def mutate(self) -> None:
        ...
