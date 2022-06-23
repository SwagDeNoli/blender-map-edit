# pylint: disable=W,C, E0401
import bpy
import bgl
import blf


class Panel:
    def __init__(self, width, height, x, y, rgba):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.rgba = rgba

    def draw(self):
        r, g, b, a = self.rgba
        bgl.glColor4f(r, g, b, a)
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glBegin(bgl.GL_POLYGON)
        bgl.glVertex2f(self.x, self.y)
        bgl.glVertex2f(self.x, self.y + self.height)
        bgl.glVertex2f(self.x + self.width, self.y + self.height)
        bgl.glVertex2f(self.x + self.width, self.y)
        bgl.glEnd()

    def is_mouse_over(self):
        return True


class TextLabel:
    def __init__(self, text, size, x, y):
        self.text = text
        self.size = size
        self.x = x
        self.y = y
        # self.rgba = rgba

    def draw(self):
        # r, g, b, a = self.rgba
        # bgl.glColor4f(r, g, b, a)
        bgl.glColor4f(1, 1, 1, 1)
        blf.position(0, self.x, self.y, 0)
        blf.size(0, self.size, 72)
        blf.draw(0, self.text)
    
    def get_dimensions(self):
        return blf.dimensions(0, self.text)

    def is_mouse_over(self):
        return True


def draw_callback_px(self, context):
    self.panel.draw()
    self.text.draw()

    # restore opengl defaults
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)


class ModalDrawOperator(bpy.types.Operator):
    """Draw a line with the mouse"""

    bl_idname = "view3d.modal_operator"
    bl_label = "Simple Modal View3D Operator"

    def __init__(self):
        self.panel = Panel(100, 100, 0, 0, (0.3, 0.3, 0.3, 1.0))
        self.text = TextLabel("", 100, 0, 0)
        
        # self.mouse_over_color = 
    def modal(self, context, event):
        context.area.tag_redraw()
        (w, h) = self.text.get_dimensions()
        self.panel.width = w
        self.panel.height = h
        self.text.text =  str(event.mouse_region_x) + " " + str(event.mouse_region_y)
        # if event.type == "MOUSEMOVE":
        #     self.panel.x = event.mouse_region_x
        #     self.panel.y = event.mouse_region_y

        return {"PASS_THROUGH"}

    def invoke(self, context, event):
        if context.area.type == "VIEW_3D":
            # the arguments we pass the the callback
            args = (self, context)
            # Add the region OpenGL drawing callback
            # draw in view space with 'POST_VIEW' and 'PRE_VIEW'
            self._handle = bpy.types.SpaceView3D.draw_handler_add(
                draw_callback_px, args, "WINDOW", "POST_PIXEL"
            )

            context.window_manager.modal_handler_add(self)
            return {"RUNNING_MODAL"}
        else:
            self.report({"WARNING"}, "View3D not found, cannot run operator")
            return {"CANCELLED"}


def register():
    bpy.utils.register_class(ModalDrawOperator)


def unregister():
    bpy.utils.unregister_class(ModalDrawOperator)


if __name__ == "__main__":
    register()

# import bpy
# import bgl
# import blf
#
#
# def draw_poly(points):
#     for i in range(len(points)):
#         bgl.glVertex2f(points[i][0], points[i][1])
#
#
# def draw_callback_px(self, context):
#     panel_points = [[10.0, 10.0],
#                     [10.0, 100.0],
#                     [150.0, 100.0],
#                     [150.0, 10.0],
#                     ]
#
#     # draw poly for floating panel
#     bgl.glColor4f(0.3, 0.3, 0.3, 1.0)
#     bgl.glEnable(bgl.GL_BLEND)
#     bgl.glBegin(bgl.GL_POLYGON)
#     draw_poly(panel_points)
#     bgl.glEnd()
#
#     # draw outline
#     bgl.glColor4f(0.1, 0.1, 0.1, 1.0)
#     bgl.glLineWidth(2)
#     bgl.glBegin(bgl.GL_LINE_LOOP)
#     draw_poly(panel_points)
#     bgl.glEnd()
#
#     font_id = 0
#     # draw some text
#     bgl.glColor4f(0.8, 0.8, 0.8, 1.0)
#     blf.position(font_id, 15, 80, 0)
#     blf.size(font_id, 14, 72)
#     blf.draw(font_id, "Hello World")
#
#     blf.position(font_id, 15, 50, 0)
#     blf.draw(font_id, "I am floating")
#
#     # restore opengl defaults
#     bgl.glLineWidth(1)
#     bgl.glDisable(bgl.GL_BLEND)
#     bgl.glColor4f(0.0, 0.0, 0.0, 1.0)
#
#
# class ModalFloatyOperator(bpy.types.Operator):
#     """Draw a floating panel"""
#     bl_idname = "view3d.modal_floaty_operator"
#     bl_label = "Demo floating panel Operator"
#
#     def modal(self, context, event):
#         context.area.tag_redraw()
#
#         # if event.type == 'MOUSEMOVE':
#         #     self.mouse_path.append((event.mouse_region_x, event.mouse_region_y))
#
#         if event.type == 'LEFTMOUSE':
#             # bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
#             return {'PASS_THROUGH'}
#
#         return {'PASS_THROUGH'}
#
#     def invoke(self, context, event):
#         if context.area.type == 'VIEW_3D':
#             # the arguments we pass the the callback
#             args = (self, context)
#             # Add the region OpenGL drawing callback
#             # draw in view space with 'POST_VIEW' and 'PRE_VIEW'
#             self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
#
#             self.mouse_path = []
#
#             context.window_manager.modal_handler_add(self)
#             return {'RUNNING_MODAL'}
#         else:
#             self.report({'WARNING'}, "View3D not found, cannot run operator")
#             return {'CANCELLED'}
#
#
# def register():
#     bpy.utils.register_class(ModalFloatyOperator)
#
#
# def unregister():
#     bpy.utils.unregister_class(ModalFloatyOperator)
#
#
# if __name__ == "__main__":
#     register()
