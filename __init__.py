bl_info = {
    'name': 'MapEdit',
    'category': 'Object',
    'version': (0, 0, 1),
    'blender': (2, 7, 9)
}

import inspect
import os
import sys

import bpy

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

print(sys.version)

if "bpy" in locals():
    import importlib

    from .operators import build_map, map_edit_operator, new_brush, new_sector, cube_uv_projection_operator, \
        new_texture_material, new_entity, export_map, export_mapmesh, morpheas_example

    importlib.reload(build_map)
    importlib.reload(map_edit_operator)
    importlib.reload(new_brush)
    importlib.reload(new_sector)
    importlib.reload(cube_uv_projection_operator)
    importlib.reload(new_texture_material)
    importlib.reload(new_entity)
    importlib.reload(export_map)
    importlib.reload(export_mapmesh)
    importlib.reload(morpheas_example)

    from .panels import map_edit_panels

    importlib.reload(map_edit_panels)

    from .operators.map_edit_operator import update_sector_materials, update_sector_normals


class MapEditProperty():
    pass


class MapEditEntityProp(MapEditProperty, bpy.types.PropertyGroup):
    tag = bpy.props.StringProperty()


class MapEditBrushProp(MapEditProperty, bpy.types.PropertyGroup):
    ceiling_height = bpy.props.FloatProperty(update=map_edit_operator.update_sector)
    floor_height = bpy.props.FloatProperty(update=map_edit_operator.update_sector)
    brush_type = bpy.props.EnumProperty(items=[
        ("SECTOR", "2D Sector", "is a 2D sector (plane)"),
        ("BRUSH", "3D Brush", "is a 3D brush (mesh)"),
        ("NONE", "None", "marks object as non-usable in map mesh build")
    ],
        name="Brush Type",
        description="Brush type",
        default="NONE"
    )
    ceiling_texture = bpy.props.PointerProperty(type=bpy.types.Material, update=update_sector_materials)
    wall_texture = bpy.props.PointerProperty(type=bpy.types.Material, update=update_sector_materials)
    floor_texture = bpy.props.PointerProperty(type=bpy.types.Material, update=update_sector_materials)


def register():
    # Register custom properties before everything else to avoid errors
    bpy.utils.register_class(MapEditBrushProp)
    bpy.utils.register_class(MapEditEntityProp)
    bpy.types.Object.map_edit_brush = bpy.props.PointerProperty(type=MapEditBrushProp)
    bpy.types.Object.map_edit_entity = bpy.props.PointerProperty(type=MapEditEntityProp)
    bpy.types.Scene.flip_map_normals = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.map_build_obj = bpy.props.PointerProperty(name="Map Build Object", type=bpy.types.Object)
    bpy.types.Scene.map_build_path = bpy.props.StringProperty(name="", description="Choose a directory: ", default="",
                                                              maxlen=1024, subtype="FILE_PATH")
    bpy.types.Scene.new_texture_path = bpy.props.StringProperty(name="", description="Choose a directory: ", default="",
                                                                maxlen=1024, subtype="FILE_PATH")
    bpy.types.Scene.new_texture_name = bpy.props.StringProperty(name="", description="Choose a name: ", default="")
    bpy.types.Scene.texel_density = bpy.props.IntProperty(name="Texel Density", default=64)
    bpy.types.Scene.texture_size = bpy.props.IntProperty(name="Texture Size", default=128)
    bpy.utils.register_module(__name__)


def unregister():
    del bpy.types.Object.map_edit_prop
    del bpy.types.Scene.flip_map_normals
    del bpy.types.Scene.map_build_obj
    del bpy.types.Scene.new_texture_path
    del bpy.types.Scene.new_texture_name
    bpy.utils.unregister_module(__name__)
