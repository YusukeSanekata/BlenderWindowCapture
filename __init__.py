import bpy

from .screen_capture import ScreenCapture

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "ScreenCapture",
    "author": "Yusuke Sanekata",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Generic",
}

INTERVAL = 0.25

# https://colorful-pico.net/introduction-to-addon-development-in-blender/2.8/html/chapter_03/03_Handle_Timer_Event.html
class ScreenCaptureOperator(bpy.types.Operator):
    bl_idname = "object.screencapture"
    bl_label = "ScreenCapture"

    __timer = None
    __cap = None

    @classmethod
    def is_running(cls):
        return cls.__timer is not None

    def __handle_add(self, context):
        if not self.is_running():
            ScreenCaptureOperator.__timer = context.window_manager.event_timer_add(
                INTERVAL, window=context.window
            )
            ScreenCaptureOperator.__cap = ScreenCapture()
            context.window_manager.modal_handler_add(self)

    def __handle_remove(self, context):
        if self.is_running():
            context.window_manager.event_timer_remove(ScreenCaptureOperator.__timer)
            ScreenCaptureOperator.__timer = None
            ScreenCaptureOperator.__cap = None

    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()

        if not self.is_running():
            # 終了処理
            pass
            return {"FINISHED"}

        if event.type == "TIMER":
            # メイン処理
            ScreenCaptureOperator.__cap.capture(event.mouse_x, event.mouse_y)
        return {"PASS_THROUGH"}

    def invoke(self, context, event):
        if not ScreenCaptureOperator.is_running():
            # 初期化処理
            self.__handle_add(context)
            return {"RUNNING_MODAL"}
        else:
            self.__handle_remove(context)
        return {"FINISHED"}

class UIPanel(bpy.types.Panel):
    bl_label = "ScreenCapture"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        if not ScreenCaptureOperator.is_running():
            layout.operator(ScreenCaptureOperator.bl_idname, text="start", icon="PLAY")
        else:
            layout.operator(ScreenCaptureOperator.bl_idname, text="end", icon="PAUSE")

classes = [
    ScreenCaptureOperator,
    UIPanel,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()
