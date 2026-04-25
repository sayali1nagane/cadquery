"""CadQuery - A parametric 3D CAD scripting framework built on top of OCCT.

CadQuery is an intuitive, easy-to-use Python module for building parametric
3D CAD models. It is modeled after OpenSCAD but uses a Python-based scripting
interface, allowing users to leverage the full power of Python.

Example usage::

    import cadquery as cq

    result = (
        cq.Workplane("XY")
        .box(10, 10, 10)
        .faces(">Z")
        .workplane()
        .hole(5)
    )
"""

from .cq import CQ, Workplane
from .occ_impl.geom import Vector, Matrix, Plane, BoundBox
from .occ_impl.shapes import (
    Shape,
    Vertex,
    Edge,
    Wire,
    Face,
    Shell,
    Solid,
    Compound,
)
from .assembly import Assembly, ConstraintKind
from .selectors import (
    Selector,
    NearestToPointSelector,
    ParallelDirSelector,
    DirectionSelector,
    PerpendicularDirSelector,
    TypeSelector,
    DirectionMinMaxSelector,
    CenterNthSelector,
    RadiusNthSelector,
    LengthNthSelector,
    SumSelector,
    SubtractSelector,
    AndSelector,
    InverseSelector,
    StringSyntaxSelector,
)
from .sketch import Sketch
from . import exporters
from . import importers

__version__ = "2.4.0"
__author__ = "CadQuery Contributors"
__license__ = "Apache License 2.0"

__all__ = [
    # Core classes
    "CQ",
    "Workplane",
    # Geometry
    "Vector",
    "Matrix",
    "Plane",
    "BoundBox",
    # Shapes
    "Shape",
    "Vertex",
    "Edge",
    "Wire",
    "Face",
    "Shell",
    "Solid",
    "Compound",
    # Assembly
    "Assembly",
    "ConstraintKind",
    # Selectors
    "Selector",
    "NearestToPointSelector",
    "ParallelDirSelector",
    "DirectionSelector",
    "PerpendicularDirSelector",
    "TypeSelector",
    "DirectionMinMaxSelector",
    "CenterNthSelector",
    "RadiusNthSelector",
    "LengthNthSelector",
    "SumSelector",
    "SubtractSelector",
    "AndSelector",
    "InverseSelector",
    "StringSyntaxSelector",
    # Sketch
    "Sketch",
    # Modules
    "exporters",
    "importers",
]
