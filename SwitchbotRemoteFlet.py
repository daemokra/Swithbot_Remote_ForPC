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
            bgcolor=ft.colors.WHITE12,
            content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(value=str(self.main_ac.temperature), size=15),
                        self.ac_mode_icon
                    ]
                )
            ]
        ))
        return ft.WindowDragArea(
            ft.Container(
                margin=0,
                padding=0,
                alignment=ft.alignment.center,
                content = ft.Column(
                    controls = [
                        ft.Row(
                            controls=[
                                self.ac_display,
                                ft.IconButton(ft.icons.CLOSE, on_click=lambda _: self.page.window_close(), icon_size=15)
                            ]
                        )
                        ]
                )
            )
        )


    def get_mode_icon(self):
        if self.main_ac.mode == 'auto':
            return ft.icons.HDR_AUTO
        if self.main_ac.mode == 'heat':
            return ft.icons.SUNNY
        if self.main_ac == 'cool':
            return ft.icons.SEVERE_COLD

def main(page: ft.Page):
    page.title = "Remote"
    page.window_height = 30
    page.window_width  = 100
    page.window_always_on_top = True
    page.window_frameless = True
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    remote = SwitchBotRemote(page)
    page.add(remote)

ft.app(target=main)