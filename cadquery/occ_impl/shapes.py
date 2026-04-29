"""OpenCASCADE shape wrappers for CadQuery.

This module provides Python wrappers around OpenCASCADE topology classes,
offering a more Pythonic interface for working with 3D shapes.
"""

from typing import Optional, Tuple, List, Union, Iterator

from OCC.Core.TopoDS import (
    TopoDS_Shape,
    TopoDS_Vertex,
    TopoDS_Edge,
    TopoDS_Wire,
    TopoDS_Face,
    TopoDS_Shell,
    TopoDS_Solid,
    TopoDS_Compound,
)
from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepBuilderAPI import (
    BRepBuilderAPI_MakeVertex,
    BRepBuilderAPI_MakeEdge,
    BRepBuilderAPI_MakeFace,
    BRepBuilderAPI_MakeSolid,
)
from OCC.Core.BRepPrimAPI import (
    BRepPrimAPI_MakeBox,
    BRepPrimAPI_MakeSphere,
    BRepPrimAPI_MakeCylinder,
)
from OCC.Core.BRepAlgoAPI import (
    BRepAlgoAPI_Fuse,
    BRepAlgoAPI_Cut,
    BRepAlgoAPI_Common,
)
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop_VolumeProperties, brepgprop_SurfaceProperties
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Ax2, gp_Dir
from OCC.Core.TopAbs import (
    TopAbs_VERTEX,
    TopAbs_EDGE,
    TopAbs_FACE,
    TopAbs_SOLID,
    TopAbs_SHELL,
    TopAbs_WIRE,
)
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import topods

from .geom import Vector


class Shape:
    """Base class for all CadQuery shapes.

    Wraps a TopoDS_Shape and provides common operations like boolean
    operations, mass property queries, and bounding box calculations.
    """

    def __init__(self, obj: TopoDS_Shape):
        self._shape = obj

    @property
    def wrapped(self) -> TopoDS_Shape:
        """Return the underlying OCC shape."""
        return self._shape

    def volume(self) -> float:
        """Compute the volume of the shape. Returns 0 for non-solid shapes."""
        props = GProp_GProps()
        brepgprop_VolumeProperties(self._shape, props)
        return props.Mass()

    def area(self) -> float:
        """Compute the surface area of the shape."""
        props = GProp_GProps()
        brepgprop_SurfaceProperties(self._shape, props)
        return props.Mass()

    def center_of_mass(self) -> Vector:
        """Return the center of mass as a Vector."""
        props = GProp_GProps()
        brepgprop_VolumeProperties(self._shape, props)
        com = props.CentreOfMass()
        return Vector(com.X(), com.Y(), com.Z())

    def bounding_box(self) -> Tuple[Vector, Vector]:
        """Return the axis-aligned bounding box as (min_corner, max_corner)."""
        bbox = Bnd_Box()
        brepbndlib_Add(self._shape, bbox)
        xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
        return Vector(xmin, ymin, zmin), Vector(xmax, ymax, zmax)

    def fuse(self, other: "Shape") -> "Shape":
        """Boolean union with another shape."""
        result = BRepAlgoAPI_Fuse(self._shape, other._shape)
        result.Build()
        return Shape(result.Shape())

    def cut(self, other: "Shape") -> "Shape":
        """Boolean subtraction of another shape from this one."""
        result = BRepAlgoAPI_Cut(self._shape, other._shape)
        result.Build()
        return Shape(result.Shape())

    def intersect(self, other: "Shape") -> "Shape":
        """Boolean intersection with another shape."""
        result = BRepAlgoAPI_Common(self._shape, other._shape)
        result.Build()
        return Shape(result.Shape())

    def vertices(self) -> List["Shape"]:
        """Return all vertices of this shape."""
        explorer = TopExp_Explorer(self._shape, TopAbs_VERTEX)
        result = []
        while explorer.More():
            result.append(Shape(explorer.Current()))
            explorer.Next()
        return result

    def edges(self) -> List["Shape"]:
        """Return all edges of this shape."""
        explorer = TopExp_Explorer(self._shape, TopAbs_EDGE)
        result = []
        while explorer.More():
            result.append(Shape(explorer.Current()))
            explorer.Next()
        return result

    def faces(self) -> List["Shape"]:
        """Return all faces of this shape."""
        explorer = TopExp_Explorer(self._shape, TopAbs_FACE)
        result = []
        while explorer.More():
            result.append(Shape(explorer.Current()))
            explorer.Next()
        return result

    def is_valid(self) -> bool:
        """Check whether the underlying shape is valid."""
        return not self._shape.IsNull()

    def __repr__(self) -> str:
        return f"<Shape: {self._shape.ShapeType()}>"


class Solid(Shape):
    """Represents a solid 3D body."""

    @classmethod
    def make_box(
        cls,
        length: float,
        width: float,
        height: float,
        pnt: Optional[Vector] = None,
    ) -> "Solid":
        """Create a box solid.

        Args:
            length: Size along the X axis.
            width: Size along the Y axis.
            height: Size along the Z axis.
            pnt: Corner point; defaults to the origin.
        """
        origin = pnt or Vector(0, 0, 0)
        builder = BRepPrimAPI_MakeBox(
            gp_Pnt(origin.x, origin.y, origin.z), length, width, height
        )
        return cls(builder.Shape())

    @classmethod
    def make_sphere(cls, radius: float, pnt: Optional[Vector] = None) -> "Solid":
        """Create a sphere solid.

        Args:
            radius: Radius of the sphere.
            pnt: Centre point; defaults to the origin.
        """
        origin = pnt or Vector(0, 0, 0)
        builder = BRepPrimAPI_MakeSphere(
            gp_Pnt(origin.x, origin.y, origin.z), radius
        )
        return cls(builder.Shape())

    @classmethod
    def make_cylinder(
        cls,
        radius: float,
        height: float,
        pnt: Optional[Vector] = None,
        direction: Optional[Vector] = None,
    ) -> "Solid":
        """Create a cylinder solid.

        Args:
            radius: Radius of the cylinder.
            height: Height of the cylinder.
            pnt: Base centre point; defaults to the origin.
            direction: Axis direction; defaults to +Z.
        """
        origin = pnt or Vector(0, 0, 0)
        axis_dir = direction or Vector(0, 0, 1)
        ax2 = gp_Ax2(
            gp_Pnt(origin.x, origin.y, origin.z),
            gp_Dir(axis_dir.x, axis_dir.y, axis_dir.z),
        )
        builder = BRepPrimAPI_MakeCylinder(ax2, radius, height)
        return cls(builder.Shape())
