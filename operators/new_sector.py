import bpy

from operators.map_edit_operator import MapEditOperator, get_active_layers, update_sector


class NewSectorOperator(MapEditOperator, bpy.types.Operator):
    """ 2D Sector Operator"""
    bl_label = "Create New Sector"
    bl_idname = "object.new_sector"
    bl_options = {"UNDO"}

    def execute(self, context: bpy.types.Context):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.mesh.primitive_plane_add(radius=1,
                                         view_align=False,
                                         enter_editmode=False,
                                         location=(0.0, 0.0, 0.0),
                                         layers=get_active_layers()
                                         )
        obj = context.active_object

        obj.map_edit_brush.ceiling_height = 4
        obj.map_edit_brush.floor_height = 0
        obj.map_edit_brush.brush_type = "SECTOR"

        obj.draw_type = 'WIRE'
        solidify_mod = obj.modifiers.new(name="SOLIDIFY", type="SOLIDIFY")
        solidify_mod.offset = 1
        solidify_mod.use_even_offset = True
        solidify_mod.use_quality_normals = True
        solidify_mod.material_offset = 1
        solidify_mod.material_offset_rim = 2

        # Make sure there will always be 3 material slots on an object,
        # And that there will always be 1 material
        if len(bpy.data.materials) == 0:
            new_mat = bpy.data.materials.new(name="Default0Mat")
            obj.data.materials.append(new_mat)
            obj.data.materials.append(None)
            obj.data.materials.append(None)
        else:
            obj.data.materials.append(None)
            obj.data.materials.append(None)
            obj.data.materials.append(None)

        obj.name = "SECTOR"
        print(obj.map_edit_entity.tag)


        update_sector(self, context)

        return {"FINISHED"}


def register():
    bpy.utils.register_class(NewSectorOperator)


def unregister():
    bpy.utils.unregister_class(NewSectorOperator)
