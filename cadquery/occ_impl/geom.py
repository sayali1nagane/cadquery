"""Geometry primitives and transformations for CadQuery.

This module provides core geometric classes including vectors, matrices,
planes, and bounding boxes used throughout CadQuery.
"""

import math
from typing import Optional, Tuple, Union, overload

from OCC.Core.gp import (
    gp_Ax1,
    gp_Ax2,
    gp_Ax3,
    gp_Dir,
    gp_Pnt,
    gp_Trsf,
    gp_Vec,
    gp_XYZ,
)
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.Bnd import Bnd_Box


class Vector:
    """A 3D vector with common geometric operations."""

    def __init__(self, *args):
        """Create a Vector from various input types.

        Accepts:
            - Vector(x, y, z)
            - Vector((x, y, z))
            - Vector(gp_Vec)
            - Vector(gp_Pnt)
            - Vector(gp_Dir)
            - Vector(gp_XYZ)
        """
        if len(args) == 3:
            self._wrapped = gp_Vec(*args)
        elif len(args) == 1:
            arg = args[0]
            if isinstance(arg, (tuple, list)) and len(arg) == 3:
                self._wrapped = gp_Vec(*arg)
            elif isinstance(arg, gp_Vec):
                self._wrapped = arg
            elif isinstance(arg, gp_Pnt):
                self._wrapped = gp_Vec(arg.X(), arg.Y(), arg.Z())
            elif isinstance(arg, gp_Dir):
                self._wrapped = gp_Vec(arg)
            elif isinstance(arg, gp_XYZ):
                self._wrapped = gp_Vec(arg.X(), arg.Y(), arg.Z())
            else:
                raise TypeError(f"Cannot create Vector from {type(arg)}")
        else:
            raise TypeError("Vector requires 1 or 3 arguments")

    @property
    def x(self) -> float:
        return self._wrapped.X()

    @property
    def y(self) -> float:
        return self._wrapped.Y()

    @property
    def z(self) -> float:
        return self._wrapped.Z()

    def length(self) -> float:
        """Return the magnitude of the vector."""
        return self._wrapped.Magnitude()

    def normalized(self) -> "Vector":
        """Return a unit vector in the same direction."""
        return Vector(self._wrapped.Normalized())

    def cross(self, other: "Vector") -> "Vector":
        """Return the cross product of this vector and another."""
        return Vector(self._wrapped.Crossed(other._wrapped))

    def dot(self, other: "Vector") -> float:
        """Return the dot product of this vector and another."""
        return self._wrapped.Dot(other._wrapped)

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self._wrapped.Added(other._wrapped))

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self._wrapped.Subtracted(other._wrapped))

    def __mul__(self, scalar: float) -> "Vector":
        return Vector(self._wrapped.Multiplied(scalar))

    def __rmul__(self, scalar: float) -> "Vector":
        return self.__mul__(scalar)

    def __neg__(self) -> "Vector":
        return Vector(self._wrapped.Reversed())

    def __repr__(self) -> str:
        return f"Vector({self.x:.4f}, {self.y:.4f}, {self.z:.4f})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return False
        return self._wrapped.IsEqual(other._wrapped, 1e-9, 1e-9)

    def to_pnt(self) -> gp_Pnt:
        """Convert to an OCC gp_Pnt."""
        return gp_Pnt(self.x, self.y, self.z)

    def to_dir(self) -> gp_Dir:
        """Convert to an OCC gp_Dir (unit direction)."""
        return gp_Dir(self._wrapped)

    def angle_between(self, other: "Vector") -> float:
        """Return the angle in degrees between this vector and another."""
        return math.degrees(self._wrapped.Angle(other._wrapped))


class BoundingBox:
    """Axis-aligned bounding box."""

    def __init__(self, shape=None, optimal: bool = False):
        """Create a bounding box, optionally computed from a shape."""
        self._bnd = Bnd_Box()
        if shape is not None:
            brepbndlib_Add(shape, self._bnd, optimal)

    @property
    def xmin(self) -> float:
        return self._bnd.Get()[0]

    @property
    def ymin(self) -> float:
        return self._bnd.Get()[1]

    @property
    def zmin(self) -> float:
        return self._bnd.Get()[2]

    @property
    def xmax(self) -> float:
        return self._bnd.Get()[3]

    @property
    def ymax(self) -> float:
        return self._bnd.Get()[4]

    @property
    def zmax(self) -> float:
        return self._bnd.Get()[5]

    @property
    def xsize(self) -> float:
        return self.xmax - self.xmin

    @property
    def ysize(self) -> float:
        return self.ymax - self.ymin

    @property
    def zsize(self) -> float:
        return self.zmax - self.zmin

    def __repr__(self) -> str:
        return (
            f"BoundingBox(x=[{self.xmin:.3f}, {self.xmax:.3f}], "
            f"y=[{self.ymin:.3f}, {self.ymax:.3f}], "
            f"z=[{self.zmin:.3f}, {self.zmax:.3f}])"
        )
