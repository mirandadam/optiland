"""Distribution Module

This module provides various classes representing 2D pupil distributions.

Kramer Harrison, 2024
"""

from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
import numpy as np


class BaseDistribution(ABC):
    """Base class for distributions.

    This class provides a base implementation for generating points and
        visualizing the distribution.

    Attributes:
        dx (float): The step size in x calculated as the difference between
            two adjacent x points.
        dy (float): The step size in y calculated as the difference between
            two adjacent y points.

    """

    @abstractmethod
    def generate_points(self, num_points: int):
        """Generate points based on the distribution.

        Args:
            num_points (int): The number of points to generate.

        """
        # pragma: no cover

    @property
    def dx(self):
        """The difference between the x-coordinates of two adjacent points.

        Returns:
            float: The step size in x.

        """
        return self.x[1] - self.x[0]

    @property
    def dy(self):
        """The difference between the y-coordinates of two adjacent points.

        Returns:
            float: The step size in y.

        """
        return self.y[1] - self.y[0]

    def view(self):
        """Visualize the distribution.

        This method plots the distribution points and a unit circle for
            reference.
        """
        plt.plot(self.x, self.y, "k*")
        t = np.linspace(0, 2 * np.pi, 256)
        x, y = np.cos(t), np.sin(t)
        plt.plot(x, y, "r")
        plt.xlabel("Normalized Pupil Coordinate X")
        plt.ylabel("Normalized Pupil Coordinate Y")
        plt.axis("equal")
        plt.show()


class LineXDistribution(BaseDistribution):
    """A class representing a line distribution along the x-axis.

    Attributes:
        positive_only (bool): Flag indicating whether the distribution should
            be limited to positive values only.

    """

    def __init__(self, positive_only: bool = False):
        self.positive_only = positive_only

    def generate_points(self, num_points: int):
        """Generates points along the x-axis based on the specified parameters.

        Args:
            num_points (int): The number of points to generate.

        """
        if self.positive_only:
            self.x = np.linspace(0, 1, num_points)
        else:
            self.x = np.linspace(-1, 1, num_points)
        self.y = np.zeros(num_points)


class LineYDistribution(BaseDistribution):
    """A class representing a line distribution along the y-axis.

    Attributes:
        positive_only (bool): Flag indicating whether the distribution should
            be positive-only.

    """

    def __init__(self, positive_only: bool = False):
        self.positive_only = positive_only

    def generate_points(self, num_points: int):
        """Generates points along the line distribution.

        Args:
            num_points (int): The number of points to generate.

        """
        self.x = np.zeros(num_points)
        if self.positive_only:
            self.y = np.linspace(0, 1, num_points)
        else:
            self.y = np.linspace(-1, 1, num_points)


class RandomDistribution(BaseDistribution):
    """A class representing a random distribution.

    Attributes:
        rng (numpy.random.Generator): The random number generator.
        x (numpy.ndarray): The x-coordinates of the generated points.
        y (numpy.ndarray): The y-coordinates of the generated points.

    """

    def __init__(self, seed=None):
        self.rng = np.random.default_rng(seed)

    def generate_points(self, num_points: int):
        """Generates random points.

        Args:
            num_points (int): The number of points to generate.

        """
        r = self.rng.uniform(size=num_points)
        theta = self.rng.uniform(0, 2 * np.pi, size=num_points)

        self.x = np.sqrt(r) * np.cos(theta)
        self.y = np.sqrt(r) * np.sin(theta)


class UniformDistribution(BaseDistribution):
    """Represents a uniform distribution of points within a square, which is
        masked to the unit disk.

    Attributes:
        x (ndarray): The x-coordinates of the generated points.
        y (ndarray): The y-coordinates of the generated points.

    """

    def generate_points(self, num_points: int):
        """Generates a grid of points within the unit disk.

        Args:
            num_points (int): The number of points along each axis to generate.

        """
        x = np.linspace(-1, 1, num_points)
        x, y = np.meshgrid(x, x)
        r2 = x**2 + y**2
        self.x = x[r2 <= 1]
        self.y = y[r2 <= 1]


class HexagonalDistribution(BaseDistribution):
    """A class representing a hexagonal distribution.

    Attributes:
        x (ndarray): Array of x-coordinates of the generated points.
        y (ndarray): Array of y-coordinates of the generated points.

    """

    def generate_points(self, num_rings: int = 6):
        """Generate points in a hexagonal distribution.

        Args:
            num_rings (int): Number of rings in the hexagonal distribution.
                Defaults to 6.

        """
        x = np.zeros(1)
        y = np.zeros(1)
        r = np.linspace(0, 1, num_rings + 1)

        for i in range(num_rings):
            num_theta = 6 * (i + 1)
            theta = np.linspace(0, 2 * np.pi, num_theta + 1)[:-1]
            x = np.concatenate([x, r[i + 1] * np.cos(theta)])
            y = np.concatenate([y, r[i + 1] * np.sin(theta)])

        self.x = x
        self.y = y


class CrossDistribution(BaseDistribution):
    """A class representing a cross-shaped distribution.

    This distribution generates points in the shape of a cross,
        with the x-axis and y-axis as the arms of the cross.

    Attributes:
        x (ndarray): Array of x-coordinates of the generated points.
        y (ndarray): Array of y-coordinates of the generated points.

    """

    def generate_points(self, num_points: int):
        """Generate points in the shape of a cross.

        Args:
            num_points (int): The number of points to generate in each axis.

        """
        x1 = np.zeros(num_points)
        x2 = np.linspace(-1, 1, num_points)
        y1 = np.linspace(-1, 1, num_points)
        y2 = np.zeros(num_points)
        self.x = np.concatenate((x1, x2))
        self.y = np.concatenate((y1, y2))


class GaussianQuadrature(BaseDistribution):
    """GaussianQuadrature class for generating points and weights for Gaussian
    quadrature distribution.

    Attributes:
        is_symmetric (bool, optional): Indicates whether the distribution is
            symmetric about y. Defaults to False.

    Reference:
        G. W. Forbes, "Optical system assessment for design: numerical ray
        tracing in the Gaussian pupil," J. Opt. Soc. Am. A 5, 1943-1956 (1988)

    """

    def __init__(self, is_symmetric=False):
        self.is_symmetric = is_symmetric

    def generate_points(self, num_rings: int):
        """Generate points for Gaussian quadrature distribution.

        Args:
            num_rings (int): Number of rings for Gaussian quadrature.

        """
        radius = self._get_radius(num_rings)

        if self.is_symmetric:
            theta = np.array([0.0])
        else:
            theta = np.array([-1.04719755, 0.0, 1.04719755])

        self.x = np.outer(radius, np.cos(theta)).flatten()
        self.y = np.outer(radius, np.sin(theta)).flatten()

    def _get_radius(self, num_rings: int) -> np.ndarray:
        """Get the radius values for the given number of rings.

        Args:
            num_rings (int): Number of rings for Gaussian quadrature.

        Returns:
            np.ndarray: Radius values for the given number of rings.

        Raises:
            ValueError: If the number of rings is not between 1 and 6.

        """
        radius_dict = {
            1: np.array([0.70711]),
            2: np.array([0.45970, 0.88807]),
            3: np.array([0.33571, 0.70711, 0.94196]),
            4: np.array([0.26350, 0.57446, 0.81853, 0.96466]),
            5: np.array([0.21659, 0.48038, 0.70711, 0.87706, 0.97626]),
            6: np.array([0.18375, 0.41158, 0.61700, 0.78696, 0.91138, 0.98300]),
        }
        if num_rings not in radius_dict:
            raise ValueError("Gaussian quadrature must have between 1 and 6 rings.")
        return radius_dict[num_rings]

    def get_weights(self, num_rings):
        """Get weights for Gaussian quadrature distribution.

        Args:
            num_rings (int): Number of rings for Gaussian quadrature.

        Returns:
            numpy.ndarray: Array of weights.

        """
        weights_dict = {
            1: np.array([0.5]),
            2: np.array([0.25, 0.25]),
            3: np.array([0.13889, 0.22222, 0.13889]),
            4: np.array([0.08696, 0.16304, 0.16304, 0.08696]),
            5: np.array([0.059231, 0.11966, 0.14222, 0.11966, 0.059231]),
            6: np.array([0.04283, 0.09019, 0.11698, 0.11698, 0.09019, 0.04283]),
        }
        if num_rings not in weights_dict:
            raise ValueError("Gaussian quadrature must have between 1 and 6 rings.")

        weights = weights_dict[num_rings]

        if self.is_symmetric:
            weights *= 6.0
        else:
            weights *= 2.0

        return weights


class RingDistribution(BaseDistribution):
    """RingDistribution class for generating points along a single ring."""

    def generate_points(self, num_points: int):
        """Generate points along a ring at the maximum aperture value.

        Args:
            num_points (int): The number of points to generate in each ring.

        """
        theta = np.linspace(0, 2 * np.pi, num_points + 1)[:-1]

        self.x = np.cos(theta)
        self.y = np.sin(theta)


def create_distribution(distribution_type):
    """Create a distribution based on the given distribution type.

    Args:
        distribution_type (str): The type of distribution to create.

    Returns:
        Distribution: An instance of the specified distribution type.

    Raises:
        ValueError: If an invalid distribution type is provided.

    """
    distribution_classes = {
        "line_x": LineXDistribution,
        "line_y": LineYDistribution,
        "positive_line_x": lambda: LineXDistribution(positive_only=True),
        "positive_line_y": lambda: LineYDistribution(positive_only=True),
        "random": RandomDistribution,
        "uniform": UniformDistribution,
        "hexapolar": HexagonalDistribution,
        "cross": CrossDistribution,
        "ring": RingDistribution,
    }

    if distribution_type not in distribution_classes:
        raise ValueError("Invalid distribution type.")

    return distribution_classes[distribution_type]()
