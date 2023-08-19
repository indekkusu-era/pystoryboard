from typing import Callable
from abc import ABC, abstractmethod
import numpy as np
from numpy import float16
from dataclasses import dataclass

@dataclass
class Sequence(ABC):
    f: Callable
    n_samples: int

    @property
    @abstractmethod
    def samples(self) -> np.ndarray:
        raise NotImplementedError()
    
    def render(self, precision=float16):
        return ",".join((value.render(precision) for value in self.f(self.samples)))

@dataclass
class RealSequence(Sequence):
    f: Callable
    n_samples: int

    @property
    def samples(self):
        return np.linspace(0, 1, self.n_samples) 

@dataclass
class IntegerSequence(Sequence):
    f: Callable
    n_samples: int

    @property
    def samples(self):
        return np.arange(0, self.n_samples)

__all__ = ['IntegerSequence', 'RealSequence', 'Sequence']
