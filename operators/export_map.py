import bpy

from operators.map_edit_operator import MapEditOperator, get_active_layers, update_sector


class NewMapOperator(MapEditOperator, bpy.types.Operator):
    """ Entity Operator"""
    bl_label = "Export map"
    bl_idname = "export_scene.export_map"
    bl_options = {"UNDO"}

    def execute(self, context: bpy.types.Context):
        if context.scene.map_build_obj:
            map_obj = context.scene.map_build_obj
            scene = context.scene
            bpy.ops.object.select_grouped(extend=True, type="CHILDREN_RECURSIVE")

            bpy.ops.export_scene.gltf(filepath=bpy.path.abspath(scene.map_build_path) + map_obj.name.lower() + ".gltf",export_format="GLTF_EMBEDDED", export_selected=True, export_apply=True)
            return {"FINISHED"}
        return {"FINISHED"}

    # def invoke(self, context, event):
    #     return context.window_manager.invoke_props_dialog(self)


def register():
    bpy.utils.register_class(NewMapOperator)


def unregister():
    bpy.utils.unregister_class(NewMapOperator)
