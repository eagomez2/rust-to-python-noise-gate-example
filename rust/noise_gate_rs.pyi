import numpy as np
from typing import Tuple


def noise_gate(
        samples: np.ndarray,
        gc: float,
        gs: float,
        sustain_count: int,
        threshold: float,
        attack: int,
        sustain: int,
        release: int
) -> Tuple[np.ndarray, float, float, int]:
    ...
