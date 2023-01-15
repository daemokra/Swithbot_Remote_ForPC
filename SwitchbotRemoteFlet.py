import os
from dotenv import load_dotenv
from switchbotpy import SwitchBotPy
import flet as ft

class SwitchBotRemote(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.on_keyboard_event = self.on_keyboard
    def build(self):
        load_dotenv()
        TOKEN  = os.getenv('TOKEN')
        SECRET = os.getenv('SECRET')
        self.switchbot = SwitchBotPy(token=TOKEN, secret=SECRET, nonce='')
        self.aircons = self.switchbot.get_airconditioners()
        self.main_ac = self.aircons[0]

        self.main_ac.temperature = os.getenv('TEMPERATURE')
        self.main_ac.mode = os.getenv('MODE')
        self.main_ac.speed = os.getenv('SPEED')

        # エアコンの設定値ディスプレイ
        self.ac_display_temp = ft.Text(value=str(self.main_ac.temperature)+'℃', size=15)
        self.ac_display_speed = ft.Text(value=str(self.main_ac.speed), size=10)
        self.ac_mode_icon = ft.Icon(name=self.get_mode_icon(), size=15)
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
                            self.ac_display_temp,
                            self.ac_mode_icon,
                            # TODO:いい感じのアイコンにする
                            ft.Icon(name=ft.icons.MODE_FAN_OFF_OUTLINED, size=15),
                            self.ac_display_speed
                        ]
                    )
                ]
            )
        )

        # 設定温度入力ボックス
        # TODO: max_lengthを指定して桁の制限を行う。
        #   ※TextFieldにmax_lengthを指定すると、counter_textが自動表示されheightを専有する。
        self.text_temperture = ft.TextField(
            text_size=15,
            height=30,
            width=60,
            keyboard_type=ft.KeyboardType.NUMBER,
            max_lines=1,
            suffix_text='℃',
            on_blur=self.on_blur_ac_temp,
            value=self.main_ac.temperature
            )
        self.input_temperture = ft.Container(
            padding = 0,
            margin  = 0,
            content = ft.Column(controls=[ft.Row(controls=[self.text_temperture])])
        )
        # 運転モード選択
        self.icon_ac_mode_heat = ft.IconButton(
            icon=ft.icons.SUNNY,
            selected=True if self.main_ac.mode == 'heat' else False,
            selected_icon=ft.icons.SUNNY,
            selected_icon_color=ft.colors.ORANGE,
            on_click=self.on_click_icon_ac_mode_heat
            )
        self.icon_ac_mode_cool = ft.IconButton(
            icon=ft.icons.AC_UNIT,
            selected=True if self.main_ac.mode == 'cool' else False,
            selected_icon=ft.icons.AC_UNIT,
            selected_icon_color=ft.colors.LIGHT_BLUE,
            on_click=self.on_click_icon_ac_mode_cool
            )

        # 風量選択
        # HACK:Dropdownで実装したい
        """
        self.speed = ft.Dropdown(
            height=30,
            width=120,
            options=[
                ft.dropdown.Option('自動'),
                ft.dropdown.Option('風量1'),
                ft.dropdown.Option('風量2'),
                ft.dropdown.Option('風量3'),
                ft.dropdown.Option('風量4'),
            ]
        )"""
        self.text_speed = ft.TextField(
            text_size=15,
            height=30,
            width=60,
            keyboard_type=ft.KeyboardType.NUMBER,
            max_lines=1,
            on_blur=self.on_blur_ac_speed,
            value=self.main_ac.speed
            )

        # 運転ON/OFFSwitch
        self.switch_power = ft.Switch(value=True if self.main_ac.state == 'on' else False, on_change=self.on_changed_switch_power)

        return ft.Container(
                margin=0,
                padding=0,
                alignment=ft.alignment.center,
                content = ft.Column(
                    controls = [
                        ft.Row(
                            controls=[
                                # FIXME:ダブルクリックすると最大化する
                                ft.WindowDragArea(ft.Container(ft.Icon(name=ft.icons.DRAG_INDICATOR, size=20), on_hover=lambda _: None)),
                                self.ac_display,
                                self.input_temperture,
                                self.icon_ac_mode_heat,
                                self.icon_ac_mode_cool,
                                self.text_speed,
                                self.switch_power,
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
        if self.main_ac.mode == 'cool':
            return ft.icons.AC_UNIT

    def on_keyboard(self,e: ft.KeyboardEvent):
        print(e)
        if e.key == "D" and e.ctrl:
            self.page.show_semantics_debugger = not self.page.show_semantics_debugger
            self.page.update()

    def on_blur_ac_temp(self, e):
        value = e.control.value
        if int(value) > 30:
            value = '30'
        if int(value) < 16:
            value = '16'
        self.main_ac.temperature = value
        self.ac_display_temp.value = str(value) + '℃'
        self.update()
        if self.switch_power.value == True:
            self.main_ac.turn_on()

    def on_blur_ac_speed(self, e):
        value = e.control.value.upper()
        if value == 'L':
            value = 'low'
        if value == 'M':
            value = 'medium'
        if value == 'H':
            value = 'high'
        if value == 'A':
            value = 'high'

        self.main_ac.speed = value
        self.ac_display_speed.value = value

        self.update()
        if self.switch_power.value == True:
            self.main_ac.turn_on()

    def on_changed_switch_power(self, e):
        if e.control.value == True:
            self.main_ac.turn_on()
        else:
            self.main_ac.turn_off()

    def on_click_icon_ac_mode_heat(self,e):
        if e.control.selected == True:
            return
        e.control.selected = True
        self.icon_ac_mode_cool.selected = not e.control.selected
        e.control.update()
        self.main_ac.mode='heat'
        self.ac_mode_icon.name=self.get_mode_icon()
        self.update()
        if self.switch_power.value == True:
            self.main_ac.turn_on()

    def on_click_icon_ac_mode_cool(self,e):
        if e.control.selected == True:
            return
        e.control.selected = True
        self.icon_ac_mode_heat.selected = not e.control.selected
        e.control.update()
        self.main_ac.mode='cool'
        self.ac_mode_icon.name=self.get_mode_icon()
        self.update()
        if self.switch_power.value == True:
            self.main_ac.turn_on()

def main(page: ft.Page):
    page.title = "Remote"
    page.window_height = 30
    page.window_max_height = 30
    page.window_width  = 550
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