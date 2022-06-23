"""MapEdit Addon For Blender 2.79b"""
import bpy


def update_sector(self, context):
    obj = bpy.context.active_object
    if obj:
        for mod in obj.modifiers:
            if mod.type == "SOLIDIFY":
                # bpy.ops.object.mode_set(mode='EDIT')
                mod.thickness = obj.map_edit_brush.ceiling_height - obj.map_edit_brush.floor_height
                mesh_data = obj.data
                for vert in mesh_data.vertices:
                    vert.co.z = obj.map_edit_brush.floor_height


def update_sector_materials(self, context: bpy.types.Context):
    obj = context.active_object
    if obj.map_edit_brush.ceiling_texture is not None:
        obj.material_slots[0].material = obj.map_edit_brush.ceiling_texture
    if obj.map_edit_brush.floor_texture is not None:
        obj.material_slots[1].material = obj.map_edit_brush.floor_texture
    if obj.map_edit_brush.wall_texture is not None:
        obj.material_slots[2].material = obj.map_edit_brush.wall_texture


def update_sector_normals(self, context: bpy.types.Context):
    obj = context.active_object
    if obj:
        if obj.modifiers[0].type == "SOLIDIFY":
            obj.modifiers[0].use_flip_normals = obj.map_edit_brush.flip_normals


def get_active_layers():
    scn = bpy.context.scene
    active_layer = [False for x in range(20)]
    active_layer[scn.active_layer] = True
    return tuple(active_layer)


def get_all_sector_objects():
    return [obj for obj in bpy.data.objects if obj.map_edit_brush.brush_type == "SECTOR"]


def get_all_brush_objects():
    return [obj for obj in bpy.data.objects if obj.map_edit_brush.brush_type == "BRUSH"]


class MapEditOperator:
    """Mixin class for operators"""
    bl_options = {"UNDO"}

    def execute(self, context: bpy.types.Context):
        pass

