import bpy
import bmesh
import typing

from enum import Enum

from operators.map_edit_operator import MapEditOperator


class FaceDirection(Enum):
    X = 0,
    Y = 1,
    Z = 2,
    NEG_X = 3,
    NEG_Y = 4,
    NEG_Z = 5


class CubeUVProjectOperator(MapEditOperator, bpy.types.Operator):
    bl_label = "Unwrap object"
    bl_idname = "uv.cube_proj"
    bl_options = {"UNDO"}

    def execute(self, context: bpy.types.Context):
        mesh_data = context.active_object.data

        bm = bmesh.new()
        bm.from_mesh(mesh_data)

        uv_layer = bm.loops.layers.uv.verify()
        bm.faces.layers.tex.verify()

        for face in bm.faces:  # type: bmesh.types.BMFace

            normal_x = abs(face.normal.x)
            normal_y = abs(face.normal.y)
            normal_z = abs(face.normal.z)

            largest_normal = normal_x
            face_direction = FaceDirection.X

            if largest_normal < normal_y:
                largest_normal = normal_y
                face_direction = FaceDirection.Y
            if largest_normal < normal_z:
                largest_normal = normal_z
                face_direction = FaceDirection.Z

            if face_direction == FaceDirection.X:
                if face.normal.x < 0:
                    face_direction = FaceDirection.NEG_X
            if face_direction == FaceDirection.Y:
                if face.normal.y < 0:
                    face_direction = FaceDirection.NEG_Y
            if face_direction == FaceDirection.Z:
                if face.normal.z < 0:
                    face_direction = FaceDirection.NEG_Z

            for uv_loop in face.loops:
                luv = uv_loop[uv_layer]
                if face_direction == FaceDirection.X:
                    luv.uv.x = uv_loop.vert.co.y * context.scene.texel_density / 128
                    luv.uv.y = uv_loop.vert.co.z * context.scene.texel_density / 128
                if face_direction == FaceDirection.NEG_X:
                    luv.uv.x = uv_loop.vert.co.y * (context.scene.texel_density / 128) * -1
                    luv.uv.y = uv_loop.vert.co.z * context.scene.texel_density / 128
                if face_direction == FaceDirection.Y:
                    luv.uv.x = uv_loop.vert.co.x * (context.scene.texel_density / 128) * -1
                    luv.uv.y = uv_loop.vert.co.z * context.scene.texel_density / 128
                if face_direction == FaceDirection.NEG_Y:
                    luv.uv.x = uv_loop.vert.co.x * context.scene.texel_density / 128
                    luv.uv.y = uv_loop.vert.co.z * context.scene.texel_density / 128
                if face_direction == FaceDirection.Z:
                    luv.uv.x = uv_loop.vert.co.x * context.scene.texel_density / 128
                    luv.uv.y = uv_loop.vert.co.y * context.scene.texel_density / 128
                if face_direction == FaceDirection.NEG_Z:
                    luv.uv.x = uv_loop.vert.co.x * context.scene.texel_density / 128
                    luv.uv.y = uv_loop.vert.co.y * (context.scene.texel_density / 128) * -1

        # Modify bmesh
        print("done")
        # Write back bmesh to actual mesh
        bm.to_mesh(mesh_data)
        # Free bmesh
        bm.free()
        return {'FINISHED'}
