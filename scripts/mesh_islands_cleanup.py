#!/usr/bin/python
# ================================
# (C)2023 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# EMAG
# mesh cleanup by mesh islands

from array import array
import lx
import modo
import modo.constants as c
import sys

sys.path.append(
    "{}\\scripts".format(lx.eval("query platformservice alias ? {kit_h3d_utilites:}"))
)
import h3d_utils as h3du
from h3d_debug import H3dDebug


def get_islands(mesh):
    if not mesh:
        return None
    if mesh.type != h3du.itype_str(c.MESH_TYPE):
        return None

    polygons = mesh.geometry.polygons
    islands = []
    while polygons:
        island = polygons[0].getIsland()
        islands.append(island)
        for poly in island:
            polygons.remove(poly)
    
    return islands


def main():
    # mesh.cleanup true true true true true true true true true true true
    meshes = modo.Scene().selectedByType(itype=c.MESH_TYPE)
    for mesh in meshes:
        islands = get_islands(mesh)

    print(islands)


if __name__ == "__main__":
    main()
