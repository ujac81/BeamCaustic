#!/usr/bin/env python
"""
BeamCaustic.py

Form rotational hyperbolic by lines.
"""

__author__ = 'ulrich.jansen@rwth-aachen.de'
__version__ = 0.95
__date__ = 'Mon 15 Jun 2015'

import math
import vtk

EMIT_RAD = 1.  # bottom emitting radius
Z_LEN = 5.  # length in axial direction
N_PHI = 360  # number of beams
THETA = 20. / 180. * math.pi  # radial "inwards" angle
TAU = 10. / 180. * math.pi  # tangential tilt angle

def add_line(points, ugrid, phi):
    """add line to output grid
    """

    # base point
    x0 = [math.cos(phi) * EMIT_RAD, math.sin(phi) * EMIT_RAD, 0]

    # unrotated beam end point
    xdash = EMIT_RAD - Z_LEN * math.atan(THETA)
    ydash = Z_LEN * math.atan(TAU)

    # apply rotational matrix on end point in (x,y)-plane
    x1 = [xdash*math.cos(phi)-ydash*math.sin(phi),
          xdash*math.sin(phi)+ydash*math.cos(phi),
          Z_LEN]

    line = vtk.vtkLine()
    line.GetPointIds().SetId(0, points.InsertNextPoint(x0))
    line.GetPointIds().SetId(1, points.InsertNextPoint(x1))
    ugrid.InsertNextCell(line.GetCellType(), line.GetPointIds())

if __name__ == '__main__':
    points = vtk.vtkPoints()
    ugrid = vtk.vtkUnstructuredGrid()

    phi = 0
    d_phi = 2. * math.pi / N_PHI
    for i in range(N_PHI):
        add_line(points, ugrid, phi)
        phi += d_phi

    ugrid.SetPoints(points)

    writer = vtk.vtkUnstructuredGridWriter()
    writer.SetFileName("rot_hyp.vtk")
    writer.SetInputData(ugrid)
    writer.Write()
