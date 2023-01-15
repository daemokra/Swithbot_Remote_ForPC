import os
from dotenv import load_dotenv
from switchbotpy import SwitchBotPy
import flet as ft
"""
        aircon = switchbot.get_airconditioners()
        main_ac = aircon[0]
        #main_ac.temperature = 16
        #main_ac.mode        = 'heat'
        #main_ac.speed       = 'low'
        #result = aircon[0].turn_on(16,'heat','auto')
        result = aircon[0].turn_on(17,'heat','auto')
        print(result)
"""
class SwitchBotRemote(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
    def build(self):
        load_dotenv()
        TOKEN  = os.getenv('TOKEN')
        SECRET = os.getenv('SECRET')
        self.switchbot = SwitchBotPy(token=TOKEN, secret=SECRET, nonce='')
        self.aircons = self.switchbot.get_airconditioners()
        self.main_ac = self.aircons[0]
        self.ac_mode_icon = ft.Icon(name=self.get_mode_icon(), size=15)

        # エアコンの設定値ディスプレイ
        self.ac_display = ft.Container(
            border_radius = ft.border_radius.all(10),
            padding = 5,
            margin  = 5,
            height = 30,
            width = 130,
            bgcolor=ft.colors.WHITE12,
            content = ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(value=str(self.main_ac.temperature)+'℃', size=15),
                            self.ac_mode_icon,
                            ft.Icon(name=ft.icons.MODE_FAN_OFF_OUTLINED, size=15),
                            ft.Text(value=str(self.main_ac.mode), size=10),
                        ]
                    )
                ]
            )
        )

        # 設定温度入力ボックス
        # TODO: max_lengthを指定して桁の制限を行う。
        #   ※TextFieldにmax_lengthを指定すると、counter_textが自動表示されheightを専有する。
        self.input_temperture = ft.Container(
            padding = 0,
            margin  = 0,
            content = ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.TextField(text_size=15,height=30, width=60, keyboard_type=ft.KeyboardType.NUMBER, max_lines=1, suffix_text='℃')
                        ]
                    )
                ]
            )
        )

        return ft.Container(
                margin=0,
                padding=0,
                alignment=ft.alignment.center,
                content = ft.Column(
                    controls = [
                        ft.Row(
                            controls=[
                                ft.WindowDragArea(ft.Container(ft.Icon(name=ft.icons.DRAG_INDICATOR, size=20), on_hover=lambda _: None)),
                                self.ac_display,
                                self.input_temperture,
                                ft.IconButton(ft.icons.CLOSE, on_click=lambda _: self.page.window_close())
                            ]
                        )
                        ]
                )
            )


    def get_mode_icon(self):
        if self.main_ac.mode == 'auto':
            return ft.icons.HDR_AUTO
        if self.main_ac.mode == 'heat':
            return ft.icons.SUNNY
        if self.main_ac == 'cool':
            return ft.icons.AC_UNIT

def main(page: ft.Page):
    page.title = "Remote"
    page.window_height = 30
    page.window_max_height = 30
    page.window_width  = 350
    page.window_always_on_top = True
    page.window_frameless = True
    page.window_maximizable = False
    page.window_full_screen = False
    page.window_resizable = False
    page.window_skip_task_bar = True
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    remote = SwitchBotRemote(page)
    page.add(remote)

ft.app(target=main)