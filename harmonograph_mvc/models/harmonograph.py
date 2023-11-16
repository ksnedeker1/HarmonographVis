import numpy as np

class HarmonographParams:
    """A class for managing Harmonograph parameters."""
    def __init__(self, pendulums, t_start, t_end, t_samples):
        self.pendulums = pendulums
        self.t_start = int(t_start)
        self.t_end = int(t_end)
        self.t_samples = int(t_samples)

    def to_dict(self):
        """Converts the parameters to a dictionary."""
        return {
            **{f"pendulum_{i+1}": pendulum for i, pendulum in enumerate(self.pendulums)},
            "t_start": self.t_start,
            "t_end": self.t_end,
            "t_samples": self.t_samples
        }


class Harmonograph:
    """A parametric representation of a multi-pendulum harmonograph expressed with an arbitrary number of dimensions"""
    def __init__(self, init_conditions: HarmonographParams):
        self.__dict__.update(init_conditions.to_dict())
        self.t = np.linspace(self.t_start, self.t_end, self.t_samples)
        self.dim = len(self.pendulum_1)  # now accessing the first pendulum attribute directly

    def _get_pendulums(self):
        """Helper method to iterate over pendulums in the object"""
        return (self.__dict__[key] for key in self.__dict__ if key.startswith('pendulum'))

    def _compute_coords(self, pendulum_params: list, size: int) -> list:
        """Helper method to compute pendulum coordinates given its parameters"""
        coords = [np.zeros(self.t_samples) for _ in range(self.dim)]
        for axis, (A, d, f, p) in enumerate(pendulum_params):
            coords[axis] = A * np.sin(self.t * f + p) * np.exp(-d * self.t)
        return self._normalize(coords, size)

    @staticmethod
    def _normalize(coords: list[np.ndarray], size: int) -> np.ndarray:
        """Normalizes the provided coordinates array to fit the provided size dimensions."""
        min_val = min(coord.min() for coord in coords)
        max_val = max(coord.max() for coord in coords)
        return [(coord - min_val) / (max_val - min_val) * size for coord in coords]

    def get_coords(self, size) -> np.ndarray:
        """Calculates and returns the coordinates of the harmonograph across the array of time points (self.t)."""
        coords = [np.zeros(self.t_samples) for _ in range(self.dim)]
        for pendulum_params in self._get_pendulums():
            for axis, pendulum_coord in enumerate(self._compute_coords(pendulum_params, size)):
                coords[axis] += pendulum_coord
        return self._normalize(coords, size)

    def get_pendulum_coords(self, size) -> list:
        """Calculates and returns the coordinates of each pendulum independently across the array of time points (self.t)."""
        return [self._compute_coords(pendulum_params, size) for pendulum_params in self._get_pendulums()]


if __name__=='__main__':
    tst = HarmonographParams(
        [
            ((1, 2, 3, 4),
             (4, 3, 2, 1),
             (1, 2, 3, 4)),
            ((2, 3, 4, 1),
             (3, 4, 1, 2),
             (1, 2, 3, 4)),
        ], 0, 100, 10000
    )
    tst2 = Harmonograph(tst)
    print(tst2.get_coords(200))


