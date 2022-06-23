import math
import os
import shutil

import bmesh
import bpy
import bpy_extras.io_utils
from bpy.props import StringProperty
from bpy.types import Context
from bpy_extras.io_utils import ExportHelper, axis_conversion


class CustomExportOperator(bpy.types.Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "export_scene.mapmesh_export"
    bl_label = "Export MAPMESH file types"
    bl_options = {'PRESET', 'UNDO'}

    # ExportHelper mixin class uses this
    filename_ext = ".mapmesh"

    filter_glob = StringProperty(
        default="*.mapmesh",
        options={'HIDDEN'},
    )

    def execute(self, context: Context):
        if context.scene.map_build_obj:
            return write_some_data(context, self.filepath)
        return {"FINISHED"}


def write_some_data(context, filepath):
    print("running write_some_data...")

    f = open(filepath, 'w', encoding='utf-8')
    ob = context.active_object

    export_mesh = ob.to_mesh(context.scene, True, "PREVIEW")
    bm = bmesh.new()
    bm.from_mesh(export_mesh)

    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    bm.to_mesh(export_mesh)
    bm.free()

    m = axis_conversion(from_forward="-Y", from_up="Z", to_forward="-Z", to_up="Y").to_4x4()
    export_mesh.transform(m)

    verts = export_mesh.vertices
    faces = export_mesh.polygons
    # print(plain_verts)
    # for face in faces:
    # for vert in verts:
    #     f.write('v {} {} {}\n'.format(verts[vert].co.x, verts[vert].co.y, verts[vert].co.z))
    tex_to_copy = []
    for face in faces:
        # Write faces
        f.write('f')
        for vert in reversed(face.vertices):
            f.write('( {} {} {} )'.format(verts[vert].co.x, verts[vert].co.y, verts[vert].co.z))

        slot = ob.material_slots[face.material_index]
        mat = slot.material
        if mat is not None:
            tex_name = bpy.path.display_name_from_filepath(mat.active_texture.image.name)
            if mat.active_texture.image not in tex_to_copy:
                tex_to_copy.append(mat.active_texture.image)
            f.write('| tex {} '.format(tex_name))
        else:
            print("No mat in slot", f.material_index)
        f.write('| uv')
        for loop in reversed(face.loop_indices):
            uv = export_mesh.uv_layers.active.data[loop].uv
            f.write(' {} {}'.format(-1 * uv.x, -1 * uv.y))
            # f.write(' {} {}'.format(uv.x, uv.y))
        f.write('\n')

    bm.free()

    children = []
    for child in ob.children:
        if child.map_edit_entity.tag != "":
            new_child = child.copy()
            new_child.matrix_world = m * new_child.matrix_world
            children.append(new_child)    
    for child in children:
        f.write('entity {}'.format(child.map_edit_entity.tag))
        f.write(" | {} {} {}".format(child.location.x, child.location.y, child.location.z))
        f.write(" | {} {} {}".format(child.rotation_euler.x, child.rotation_euler.y, child.rotation_euler.z))
        bpy.data.objects.remove(child)
    f.close()
    
    tex_dest = os.path.dirname(filepath) + r"\textures"
    print(tex_dest)
    if not os.path.exists(tex_dest):
        os.mkdir(tex_dest)
    for tex in tex_to_copy:
        print(bpy.path.abspath(tex.filepath))
        shutil.copy(bpy.path.abspath(tex.filepath), tex_dest)

    bpy.data.meshes.remove(export_mesh, True)

    return {'FINISHED'}
