import math
import numpy as np
from noise_gate_rs import noise_gate


class NoiseGateRs:
    def __init__(
            self,
            fs: int,
            threshold_db: float = -40.0,
            attack_ms: float = 20,
            sustain_ms: float = 30,
            release_ms: float = 30
    ) -> None:
        super().__init__()

        # Params
        self.fs = fs
        self.threshold_db = threshold_db
        self.attack_ms = attack_ms
        self.sustain_ms = sustain_ms
        self.release_ms = release_ms
        self._gc = 0.0
        self._gs = 0.0
        self._sustain_count = 0
    
    @property
    def threshold(self) -> float:
        return NoiseGateRs.db_to_amp(self.threshold_db, min=-80.0)
    
    @property
    def attack(self) -> int:
        return self.ms_to_samples(self.attack_ms)
    
    @property
    def sustain(self) -> int:
        return self.ms_to_samples(self.sustain_ms)
    
    @property
    def release(self) -> int:
        return self.ms_to_samples(self.release_ms)
    
    @staticmethod
    def db_to_amp(x: float, min: float) -> float:
        return 10.0 ** (x * 0.05) if x > min else 0.0
    
    def ms_to_samples(self, ms: float) -> int:
        return int((ms * self.fs) * 0.001)

    def __call__(self, x: np.ndarray) -> np.ndarray:
        y, self._gc, self._gs, self._sustain_count = noise_gate(
            samples=x,
            gc=self._gc,
            gs=self._gs,
            sustain_count=self._sustain_count,
            threshold=self.threshold,
            attack=self.attack,
            sustain=self.sustain,
            release=self.release
        )
        return y


class NoiseGatePy:
    def __init__(
            self,
            fs: int,
            threshold_db: float = -40.0,
            attack_ms: float = 20,
            sustain_ms: float = 30,
            release_ms: float = 30
    ) -> None:
        super().__init__()

        # Params
        self.fs = fs
        self.threshold_db = threshold_db
        self.attack_ms = attack_ms
        self.sustain_ms = sustain_ms
        self.release_ms = release_ms
        self._gc = 0.0
        self._gs = 0.0
        self._sustain_count = 0
    
    @property
    def threshold(self) -> float:
        return NoiseGateRs.db_to_amp(self.threshold_db, min=-80.0)
    
    @property
    def attack(self) -> int:
        return self.ms_to_samples(self.attack_ms)
    
    @property
    def sustain(self) -> int:
        return self.ms_to_samples(self.sustain_ms)
    
    @property
    def release(self) -> int:
        return self.ms_to_samples(self.release_ms)
    
    @property
    def attack_factor(self) -> float:
        return math.exp(-2.1972246 * (1 / self.attack))
    
    @property
    def release_factor(self) -> float:
        return math.exp(-2.1972246 * (1 / self.release))
    
    @staticmethod
    def db_to_amp(x: float, min: float) -> float:
        return 10.0 ** (x * 0.05) if x > min else 0.0
    
    def ms_to_samples(self, ms: float) -> int:
        return int((ms * self.fs) * 0.001)

    def __call__(self, x: np.ndarray) -> np.ndarray:
        for idx in range(len(x)):
            # Check if gate control is 0, reset sustain cound
            if abs(x[idx]) >= self.threshold:
                if self._gc == 0.0:
                    self._sustain_count = 0
                
                self._gc = 1.0
            
            else:
                # Increment sustain count and set gate control to 0
                self._sustain_count += 1
                self._gc = 0.0
            
            # Adjust gate state based on sustain count, gc and attack/release
            # factors
            if self._sustain_count > self.sustain and self._gc <= self._gs:
                self._gs = (
                    self.attack_factor * self._gs
                    + (1.0 - self.attack_factor) * self._gc
                )
            
            elif self._sustain_count <= self.sustain and self._gc > self._gs:
                self._gs = (
                    self.release_factor * self._gs
                    + (1.0 - self.release_factor) * self._gc
                )
            
            x[idx] *= self._gs

        return x
