#!/usr/bin/python
# ================================
# (C)2023 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# EMAG
# mesh cleanup by mesh islands
# select mesh items and run the script

import lx
import modo
import modo.constants as c
import sys

sys.path.append(
    "{}\\scripts".format(lx.eval("query platformservice alias ? {kit_h3d_utilites:}"))
)
import h3d_utils as h3du
from h3d_debug import H3dDebug


REMOVE_FLOATING_VERTICES = "h3d_imc_remove_floating_vertices"
REMOVE_ONE_POINT_POLYGONS = "h3d_imc_remove_one_point_polygons"
REMOVE_TWO_POINTS_POLYGONS = "h3d_imc_remove_two_points_polygons"
FIX_DUPLICATE_POINTS_IN_POLYGON = "h3d_imc_fix_duplicate_points_in_polygon"
REMOVE_COLINEAR_VERTICES = "h3d_imc_remove_colinear_vertices"
FIX_FACE_NORMAL_VECTORS = "h3d_imc_fix_face_normal_vectors"
MERGE_VERTICES = "h3d_imc_merge_vertices"
MERGE_DISCO_VALUES = "h3d_imc_merge_disco_values"
UNIFY_POLYGONS = "h3d_imc_unify_polygons"
FORCE_UNIFY = "h3d_imc_force_unify"
REMOVE_DISCO_WEIGHT_VALUES = "h3d_imc_remove_disco_weight_values"


class Options:
    remove_floating_vertices = False
    remove_one_point_polygons = False
    remove_two_points_polygons = False
    fix_duplicate_points_in_polygon = False
    remove_colinear_vertices = False
    fix_face_normal_vectors = False
    merge_vertices = False
    merge_disco_values = False
    unify_polygons = False
    force_unify = False
    remove_disco_weight_values = False


def mesh_cleanup(opt):
    lx.eval("!mesh.cleanup {} {} {} {} {} {} {} {} {} {} {}".format(
            opt.remove_floating_vertices,
            opt.remove_one_point_polygons,
            opt.remove_two_points_polygons,
            opt.fix_duplicate_points_in_polygon,
            opt.remove_colinear_vertices,
            opt.fix_face_normal_vectors,
            opt.merge_vertices,
            opt.merge_disco_values,
            opt.unify_polygons,
            opt.force_unify,
            opt.remove_disco_weight_values
            ))


def main():
    # mesh.cleanup true true true true true true true true true true true
    print("")
    print("start mesh_islands_cleanup.py ...")

    opt = Options()
    opt.remove_floating_vertices = h3du.get_user_value(REMOVE_FLOATING_VERTICES)
    opt.remove_one_point_polygons = h3du.get_user_value(REMOVE_ONE_POINT_POLYGONS)
    opt.remove_two_points_polygons = h3du.get_user_value(REMOVE_TWO_POINTS_POLYGONS)
    opt.fix_duplicate_points_in_polygon = h3du.get_user_value(FIX_DUPLICATE_POINTS_IN_POLYGON)
    opt.remove_colinear_vertices = h3du.get_user_value(REMOVE_COLINEAR_VERTICES)
    opt.fix_face_normal_vectors = h3du.get_user_value(FIX_FACE_NORMAL_VECTORS)
    opt.merge_vertices = h3du.get_user_value(MERGE_VERTICES)
    opt.merge_disco_values = h3du.get_user_value(MERGE_DISCO_VALUES)
    opt.unify_polygons = h3du.get_user_value(UNIFY_POLYGONS)
    opt.force_unify = h3du.get_user_value(FORCE_UNIFY)
    opt.remove_disco_weight_values = h3du.get_user_value(REMOVE_DISCO_WEIGHT_VALUES)

    # get selected meshes
    selected_meshes = modo.Scene().selectedByType(itype=c.MESH_TYPE)
    # cleanup selected meshes in a loop
    for mesh in selected_meshes:
        # group selected mesh in a temp folder
        mesh.select(replace=True)
        lx.eval("layer.groupSelected")
        group_loc = mesh.parent
        # unmerge mesh into a temp folder
        mesh.select(replace=True)
        lx.eval("layer.unmergeMeshes")
        # select all meshes in a folder
        for child in group_loc.children():
            child.select()
        # cleanup selected meshes
        mesh_cleanup(opt)
        # merge selected meshes
        lx.eval("layer.mergeMeshes true")
        # parent mesh to an previous parent
        parent_item = group_loc.parent
        parent_id = parent_item.id if parent_item else None
        lx.eval("item.parent {} {} {} inPlace:1 duplicate:0".format(mesh.id, parent_id, group_loc.parentIndex))
        # remove a temp folder
        modo.Scene().removeItems(group_loc)

    print("done.")


if __name__ == "__main__":
    main()
