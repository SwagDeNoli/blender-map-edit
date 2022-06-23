import bmesh
import bpy

from operators.cube_uv_projection_operator import CubeUVProjectOperator
from operators.map_edit_operator import MapEditOperator, get_all_sector_objects, get_all_brush_objects


class BuildMapOperator(MapEditOperator, bpy.types.Operator):
    """Custom Operator"""
    bl_label = "Build Map"
    bl_idname = "object.build_map"
    bl_options = {"UNDO"}

    def execute(self, context: bpy.types.Context):
        scene = context.scene

        if context.scene.map_build_obj is None:
            new_map_mesh = bpy.data.meshes.new("Mesh")
            new_map_object = bpy.data.objects.new("Map", new_map_mesh)
            bpy.context.scene.objects.link(new_map_object)
        else:
            new_map_object = context.scene.map_build_obj
            me = new_map_object.data
            bm = bmesh.new()
            bm.from_mesh(me)

            for vert in bm.verts:
                bm.verts.remove(vert)
            bm.to_mesh(me)

        sectors = get_all_sector_objects()
        brushes = get_all_brush_objects()

        # REVIEW: Check that this section does the same thing
        #  for both first sector and sectors afterwards
        for sector in sectors:
            if sector == sectors[0]:
                # new_map_object.data = sector.to_mesh(context.scene, True, "PREVIEW")
                apply_new_map_bool(new_map_object, sector, scene)
            else:
                apply_new_map_bool(new_map_object, sector, scene)

        # Get map mesh data and flip normals
        new_map_object.data.flip_normals()

        bpy.ops.object.select_all(action='DESELECT')
        new_map_object.select = True
        bpy.context.scene.objects.active = new_map_object
        # context.active_object = new_map_object

        bpy.ops.uv.cube_proj()

        for o in bpy.data.objects:
            if o.users == 0:
                bpy.data.objects.remove(o)
        for m in bpy.data.meshes:
            if m.users == 0:
                bpy.data.meshes.remove(m)
        return {'FINISHED'}


# Create map mesh to start boolean'ing from
def apply_new_map_bool(map_obj: bpy.types.Object, starting_obj: bpy.types.Object, scene: bpy.types.Scene):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects.active = map_obj

    # Copy 1st map brush's mesh to build map
    new_mesh = starting_obj.to_mesh(scene, True, "PREVIEW")
    # Create bool obj
    new_bool_obj = bpy.data.objects.new("_bool", new_mesh)
    new_bool_obj.location = starting_obj.location

    # Copy materials
    for m in starting_obj.data.materials:
        has_material = False
        for mat in map_obj.data.materials:
            if mat is not None and m is not None:
                if mat.name == m.name:
                    has_material = True
        if not has_material:
            map_obj.data.materials.append(m)

    bool_mod = map_obj.modifiers.new(name=new_bool_obj.name, type="BOOLEAN")
    bool_mod.object = new_bool_obj
    bool_mod.operation = "UNION"
    if bpy.app.version[1] >= 78:
        bool_mod.solver = "CARVE"

    bpy.context.scene.objects.active = map_obj
    bpy.ops.object.modifier_apply(modifier=new_bool_obj.name)