import bpy
# from enum import Enum


class Action:
    SELECT = 'SELECT'
    DESELECT = 'DESELECT'


classes = [
    Action
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
