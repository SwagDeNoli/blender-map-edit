import bpy

from operators.map_edit_operator import MapEditOperator, get_active_layers


class NewBrushOperator(MapEditOperator, bpy.types.Operator):
    """ 2D Sector Operator"""
    bl_label = "Create New Brush"
    bl_idname = "object.new_brush"
    bl_options = {"UNDO"}

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=False, location=[0, 0, 0],
                                        layers=get_active_layers())

        obj = context.active_object
        obj.name = "BRUSH"
        # obj.map_edit_prop.ceiling_height = 4
        # obj.map_edit_prop.floor_height = 0
        obj.map_edit_prop.brush_type = "BRUSH"
        if context.scene.flip_map_normals:
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.normals_make_consistent(inside=True)
            bpy.ops.object.mode_set(mode="OBJECT")

        return {"FINISHED"}


def register():
    bpy.utils.register_class(NewBrushOperator)


def unregister():
    bpy.utils.unregister_class(NewBrushOperator)
