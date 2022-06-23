import bpy

from operators.map_edit_operator import MapEditOperator, get_active_layers, update_sector


class NewEntityOperator(MapEditOperator, bpy.types.Operator):
    """ Entity Operator"""
    bl_label = "Create New Entity"
    bl_idname = "object.new_entity"
    bl_options = {"UNDO"}

    entity_tag = bpy.props.StringProperty()

    def execute(self, context: bpy.types.Context):
        if context.scene.map_build_obj:

            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.empty_add(type='ARROWS',
                                     view_align=False,
                                     location=(0.0, 0.0, 0.0),
                                     layers=get_active_layers())
            obj = context.active_object
            obj.name = "entity_" + self.entity_tag
            obj.map_edit_entity.tag = self.entity_tag
            print(obj.map_edit_entity.tag)
            obj.parent = context.scene.map_build_obj
            return {"FINISHED"}
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


def register():
    bpy.utils.register_class(NewEntityOperator)


def unregister():
    bpy.utils.unregister_class(NewEntityOperator)
