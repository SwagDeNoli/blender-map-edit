"""MapEdit Addon For Blender 2.79b"""
import bpy
import typing
from bpy import types
import bmesh
from bpy.types import UILayout


class TPanelTool:
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    # @classmethod
    # def poll(cls, context):
    #     return context.object is not None


# WARNING: WHEN ACCESSING A SUB-PROP FROM A PROPERTYGROUP
# MAKE SURE TO PASS THE **** PROPGROUP AS THE DATA PARAM
class MapEditPanel(TPanelTool, bpy.types.Panel):
    bl_label = "MapEdit"
    bl_idname = "mapedit.panel"
    # bl_context = "object"
    bl_category = "MapEdit"

    def draw(self, context: bpy.types.Context):
        layout = self.layout
        obj = context.active_object

        col = layout.column(align=True)
        col.label("Sector Creation Tools")
        col.operator("object.new_sector", text="New 2D Sector", icon="SURFACE_NCURVE")
        # col.operator("object.new_brush", text="New 3D Brush", icon="SNAP_FACE")
        
        col = layout.column(align=True)
        col.label("Entity Creation Tools")
        col.operator("object.new_entity", text="New Entity", icon="ARMATURE_DATA")

        col = layout.column(align=True)
        col.label("Map Build Tools")
        col.operator("object.build_map", text="Generate Map Mesh", icon="MOD_BUILD")
        col.operator("export_scene.mapmesh_export", text="Export Map Mesh", icon="MOD_BUILD")
        col.prop(context.scene, "map_build_path", text="")
        col.prop(context.scene, "map_build_obj", "Map Object")
        col = layout.column(align=True)
        col.prop(context.scene, "texel_density")
        # col.prop(context.scene, "texture_size")
        col.separator()

        if obj is not None and obj.map_edit_brush.brush_type == "SECTOR":
            col = layout.column(align=True)
            col.label("Ceiling Height")
            col.prop(context.active_object.map_edit_brush, "ceiling_height")
            col.prop(context.active_object.map_edit_brush, "floor_height")
            col.prop_search(obj.map_edit_brush, "ceiling_texture", bpy.data, "materials")
            col.prop_search(obj.map_edit_brush, "wall_texture", bpy.data, "materials")
            col.prop_search(obj.map_edit_brush, "floor_texture", bpy.data, "materials")

        col.separator()
        
        if obj is not None and obj.map_edit_entity.tag != "":
            col = layout.column(align=True)
            col.label("Entity tag")
            col.prop(context.active_object.map_edit_entity, "tag")

        col.separator()

        col = layout.column(align=True)
        col.label(text="Texture Path")
        col.prop(context.scene, "new_texture_path", text="")
        col.label(text="Texture Name")
        col.prop(context.scene, "new_texture_name", text="")
        col.operator("object.new_texture", text="Create New Texture")


classes = [
    MapEditPanel
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
