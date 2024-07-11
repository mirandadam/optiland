"""Optiland Distribution Module

This module provides a set of classes that represent different types of
variables within an optical system, such as radius, conic, and thickness of
optical surfaces. Each variable type is defined as a class that inherits from
the VariableBehavior base class, which provides a common interface for getting
and updating the value of the variable.

Kramer Harrison, 2024
"""
from abc import ABC, abstractmethod


class VariableBehavior(ABC):
    """
    Represents the behavior of a variable in an optic system.

    Args:
        optic (Optic): The optic system to which the variable belongs.
        surface_number (int): The surface number of the variable.
        **kwargs: Additional keyword arguments.

    Attributes:
        optic (Optic): The optic system to which the variable belongs.
        _surfaces (SurfaceGroup): The group of surfaces in the optic system.
        surface_number (int): The surface number of the variable.
    """

    def __init__(self, optic, surface_number, **kwargs):
        self.optic = optic
        self._surfaces = self.optic.surface_group
        self.surface_number = surface_number

    @abstractmethod
    def get_value(self):
        """
        Get the value of the variable.

        Returns:
            The value of the variable.
        """
        pass

    @abstractmethod
    def update_value(self, new_value):
        """
        Update the value of the variable.

        Args:
            new_value: The new value of the variable.
        """
        pass


class RadiusVariable(VariableBehavior):
    """
    Represents a variable for the radius of a surface in an optic.

    Args:
        optic (Optic): The optic object that contains the surface.
        surface_number (int): The index of the surface in the optic.
        **kwargs: Additional keyword arguments.

    Attributes:
        optic (Optic): The optic object that contains the surface.
        surface_number (int): The index of the surface in the optic.

    Methods:
        get_value(): Returns the current value of the radius.
        update_value(new_value): Updates the value of the radius.
    """

    def __init__(self, optic, surface_number, **kwargs):
        super().__init__(optic, surface_number, **kwargs)

    def get_value(self):
        """
        Returns the current value of the radius.

        Returns:
            float: The current value of the radius.
        """
        return self._surfaces.radii[self.surface_number]

    def update_value(self, new_value):
        """
        Updates the value of the radius.

        Args:
            new_value (float): The new value of the radius.
        """
        self.optic.set_radius(new_value, self.surface_number)


class ConicVariable(VariableBehavior):
    """
    Represents a variable for the conic constant of a surface in an optic.

    Args:
        optic (Optic): The optic object to which the surface belongs.
        surface_number (int): The index of the surface in the optic.
        **kwargs: Additional keyword arguments.

    Attributes:
        optic (Optic): The optic object to which the surface belongs.
        surface_number (int): The index of the surface in the optic.

    Methods:
        get_value: Returns the current conic constant of the surface.
        update_value: Updates the conic value of the surface.
    """

    def __init__(self, optic, surface_number, **kwargs):
        super().__init__(optic, surface_number, **kwargs)

    def get_value(self):
        """
        Returns the current conic constant of the surface.

        Returns:
            float: The conic constant of the surface.
        """
        return self._surfaces.conic[self.surface_number]

    def update_value(self, new_value):
        """
        Updates the conic value of the surface.

        Args:
            new_value (float): The new conic constant to set.

        """
        self.optic.set_conic(new_value, self.surface_number)


class ThicknessVariable(VariableBehavior):
    """
    Represents a variable for the thickness of an optic surface.

    Args:
        optic (Optic): The optic object to which the surface belongs.
        surface_number (int): The number of the surface.
        **kwargs: Additional keyword arguments.

    Attributes:
        optic (Optic): The optic object to which the surface belongs.
        surface_number (int): The number of the surface.

    Methods:
        get_value(): Returns the current thickness value of the surface.
        update_value(new_value): Updates the thickness value of the surface.
    """

    def __init__(self, optic, surface_number, **kwargs):
        super().__init__(optic, surface_number, **kwargs)

    def get_value(self):
        """
        Returns the current thickness value of the surface.

        Returns:
            float: The current thickness value.
        """
        return self._surfaces.get_thickness(self.surface_number)[0]

    def update_value(self, new_value):
        """
        Updates the thickness value of the surface.

        Args:
            new_value (float): The new thickness value.
        """
        self.optic.set_thickness(new_value, self.surface_number)


class IndexVariable(VariableBehavior):
    """
    Represents a variable for the index of refraction at a specific surface
    and wavelength.

    Args:
        optic (Optic): The optic object associated with the variable.
        surface_number (int): The surface number where the variable is applied.
        wavelength (float): The wavelength at which the index of refraction is
            calculated.
        **kwargs: Additional keyword arguments.

    Attributes:
        optic (Optic): The optic object to which the surface belongs.
        surface_number (int): The number of the surface.
        wavelength (float): The wavelength at which the index of refraction is
            calculated.

    Methods:
        get_value(): Returns the value of the index of refraction at the
            specified surface and wavelength.
        update_value(new_value): Updates the value of the index of refraction
            at the specified surface.
    """

    def __init__(self, optic, surface_number, wavelength, **kwargs):
        super().__init__(optic, surface_number, **kwargs)
        self.wavelength = wavelength

    def get_value(self):
        """
        Returns the value of the index of refraction at the specified surface
        and wavelength.

        Returns:
            float: The value of the index of refraction.
        """
        n = self.optic.n(self.wavelength)
        return n[self.surface_number]

    def update_value(self, new_value):
        """
        Updates the value of the index of refraction at the specified surface.

        Args:
            new_value (float): The new value of the index of refraction.
        """
        self.optic.set_index(new_value, self.surface_number)


class AsphereCoeffVariable(VariableBehavior):
    """
    Represents a variable for an aspheric coefficient in an optical system.

    Args:
        optic (Optic): The optic object associated with the variable.
        surface_number (int): The index of the surface in the optical system.
        coeff_number (int): The index of the aspheric coefficient.
        **kwargs: Additional keyword arguments.

    Attributes:
        coeff_number (int): The index of the aspheric coefficient.
    """

    def __init__(self, optic, surface_number, coeff_number, **kwargs):
        super().__init__(optic, surface_number, **kwargs)
        self.coeff_number = coeff_number

    def get_value(self):
        """
        Get the current value of the aspheric coefficient.

        Returns:
            float: The current value of the aspheric coefficient.
        """
        surf = self._surfaces.surfaces[self.surface_number]
        return surf.geometry.c[self.coeff_number]

    def update_value(self, new_value):
        """
        Update the value of the aspheric coefficient.

        Args:
            new_value (float): The new value of the aspheric coefficient.
        """
        self.optic.set_asphere_coeff(new_value, self.surface_number,
                                     self.coeff_number)


class Variable:
    """
    Represents a variable in an optical system.

    Args:
        optic (OpticalSystem): The optical system to which the variable
            belongs.
        type (str): The type of the variable. Valid types are 'radius',
            'conic', 'thickness', 'index' and 'asphere_coeff'.
        **kwargs: Additional keyword arguments to be stored as attributes of
            the variable.

    Attributes:
        optic (OpticalSystem): The optical system to which the variable
            belongs.
        type_name (str): The type of the variable.
        min_val (float or None): The minimum value allowed for the variable.
            Defaults to None.
        max_val (float or None): The maximum value allowed for the variable.
            Defaults to None.

    Properties:
        value: The current value of the variable.
        bounds: The bounds of the variable.

    Methods:
        update(new_value): Updates the variable to a new value.

    Raises:
        ValueError: If an invalid variable type is provided.
    """

    def __init__(self, optic, type_name, min_val=None, max_val=None, **kwargs):
        self.optic = optic
        self.type = type_name
        self.min_val = min_val
        self.max_val = max_val
        self.kwargs = kwargs

        for key, value in kwargs.items():
            if key in self.allowed_attributes():
                setattr(self, key, value)
            else:
                # Handle unexpected attributes or raise a warning/error
                print(f"Warning: {key} is not a recognized attribute")

        self.variable_behavior = self._get_variable_behavior()

    @staticmethod
    def allowed_attributes():
        """
        This method returns a set of strings that are the names of allowed
        attributes.
        """
        return {'surface_number', 'coeff_number', 'wavelength'}

    def _get_variable_behavior(self):
        """
        Get the behavior of the variable.

        Returns:
            The behavior of the variable, or None if an error occurs.
        """
        behavior_kwargs = {
            'type_name': self.type,
            'optic': self.optic,
            **self.kwargs
        }

        variable_types = {
            'radius': RadiusVariable,
            'conic': ConicVariable,
            'thickness': ThicknessVariable,
            'index': IndexVariable,
            'asphere_coeff': AsphereCoeffVariable
        }

        variable_class = variable_types.get(self.type)

        # Instantiate the class if it exists
        if variable_class:
            return variable_class(**behavior_kwargs)
        else:
            return None

    @property
    def value(self):
        """Return the value of the variable.

        Returns:
            float: The value of the variable.

        Raises:
            ValueError: If the variable type is invalid.
        """
        if self.variable_behavior:
            return self.variable_behavior.get_value()
        else:
            raise ValueError(f'Invalid variable type "{self.type}"')

    @property
    def bounds(self):
        """Returns the bounds of the variable as a tuple.

        Returns:
            tuple: the bounds of the variable
        """
        return (self.min_val, self.max_val)

    def update(self, new_value):
        """Update variable to a new value.

        Args:
            new_value (float): The new value with which to update the variable.

        Raises:
            ValueError: If the variable type is invalid.
        """
        if self.variable_behavior:
            self.variable_behavior.update_value(new_value)
        else:
            raise ValueError(f'Invalid variable type "{self.type}"')
