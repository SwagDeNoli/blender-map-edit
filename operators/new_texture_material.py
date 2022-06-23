import bpy
from operators.map_edit_operator import MapEditOperator


class NewTextureMaterialOperator(MapEditOperator, bpy.types.Operator):
    """ 2D Sector Operator"""
    bl_label = "Create New Texture Material"
    bl_idname = "object.new_texture"
    bl_options = {"UNDO"}

    def execute(self, context: bpy.types.Context):
        texture_path = context.scene.new_texture_path
        texture_name = context.scene.new_texture_name
        
        if texture_path != "":        
            img = bpy.data.images.load(texture_path, True)  # type: bpy.types.Image
    
            tex = bpy.data.textures.new(texture_name, 'IMAGE')  # type: bpy.types.Texture
            tex.image = img
    
            mat = bpy.data.materials.new(name=texture_name)
            mat.texture_slots.add()
            tex_slot = mat.texture_slots[0]
            tex_slot.texture = tex
            tex_slot.texture_coords = "UV"
    
            context.scene.new_texture_path = ""
            context.scene.new_texture_name = ""
            context.scene.update()
        return {"FINISHED"}


def register():
    bpy.utils.register_class(NewTextureMaterialOperator)


def unregister():
    bpy.utils.unregister_class(NewTextureMaterialOperator)
