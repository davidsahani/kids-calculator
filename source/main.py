from display_text import DisplayText
from kivy.core.window import Window
from kivy.metrics import sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.label import MDLabel


class TextField(ScrollView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.bar_width = '0dp'

        self.label = MDLabel(
            markup=True,
            valign='top',
            halign='right',
            size_hint=(2, None),
        )
        self.add_widget(self.label)
        self.label.font_size = int(sp(25))
        self.label.font_name = "fonts/FiraCode-Retina"
        self.label.bind(texture_size=self._adjust_label_height)
        self._max_text_size_for_label_width = 0

    def _adjust_label_height(self, instance: MDLabel, size: tuple[int, int]) -> None:
        self.label.height = size[1]
        self._max_text_size_for_label_width = self._eval_max_text_size()

    def on_scroll_stop(self, touch, check_children: bool = True) -> bool | None:
        """Hide scrollbar when reached end otherwise show scrollbar"""
        if self.label.halign == 'left':
            self.bar_width = '0dp' if self.scroll_x < 0.02 else '2dp'
        else:
            self.bar_width = '0dp' if self.scroll_x > 0.9868 else '2dp'
        return super().on_scroll_stop(touch, check_children)

    def _adjust_line_height_and_scrollbar(self) -> None:
        """Adjust line height and move scrollbar to respective side"""
        if self.label.halign == 'left':
            if self.scroll_x != 0.0:
                self.scroll_x = 0.0  # move to left
            self.label.line_height = 0.7
        else:
            if self.scroll_x != 1.0:
                self.scroll_x = 1.0  # move to right
            self.label.line_height = 1

    def _eval_max_text_size(self) -> int:
        # 280 => weighting factor for self.width
        # which is diff b/w text_width and self.width
        return (self.width + 280) // self.label.font_size

    @property
    def max_text_size(self) -> int:
        max_text = self._max_text_size_for_label_width
        if max_text == 0:
            max_text = self._eval_max_text_size()
            self._max_text_size_for_label_width = max_text
        if self.label.halign == 'left':
            return max_text  # for division
        return max_text + int(max_text * 0.4)

    @property
    def text(self) -> str:
        return self.label.text

    def insert(self, text: str) -> None:
        """Insert text into label, replace spaces with non-breaking spaces

        Note: No next line is added.
        """
        self.label.text += text.replace(' ', '\u00A0')

    def set_text(self, text: str) -> None:
        """Set text into label, replace spaces with non-breaking spaces

        Note: Line height and scrollbar is adjusted.
        """
        self.label.text = text.replace(' ', '\u00A0')
        self._adjust_line_height_and_scrollbar()

    def set_ctext(self, text: str) -> None:
        """Set colored formatted text into the label

        Note: Spaces aren't replaced with non-breaking spaces.
        """
        font_size = self.label.font_size - 10  # colored text font size
        spacing_font_size = self.label.font_size - font_size
        spaced_text = f"[size={spacing_font_size}]\u00A0[/size]".join(text)
        self.label.text = f"[size={font_size}][color=#9BA4B5]{spaced_text}[/color][/size]"


class NumPad(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._app: 'CalculatorApp' = MDApp.get_running_app()  # type: ignore
        Window.bind(on_key_down=self._on_key_down)
        self.operators = {
            43: '+', 45: '-', 42: '*', 47: '/', 37: '%',
            270: '+', 269: '-', 268: '*', 267: '/'  # numpad
        }

    def _on_key_down(self, window, keycode: int, param: int,
                     text: str | None, modifiers: list[str]) -> bool:

        if 'shift' in modifiers:  # shift pressed
            if keycode == 61:  # + key
                self._app.insert_operator('+')
            elif keycode == 45:  # - key
                self._app.insert_operator('-')
            elif keycode == 56:  # 8 key
                self._app.insert_operator('*')
            elif keycode == 47:  # / key
                self._app.insert_operator('/')
            elif keycode == 53:  # 5 key
                self._app.insert_operator('%')
            return True

        if keycode == 8:  # backspace
            self._app.erase_to_left()
        elif keycode == 27:  # escape
            self._app.clear()
        elif 47 < keycode < 58:  # number keys
            self._app.insert(chr(keycode))
        elif 255 < keycode < 266:  # numpad number keys
            self._app.insert(str(keycode - 256))
        elif keycode in [46, 266]:  # . keys
            self._app.insert('.')
        elif keycode in [13, 271]:  # enter keys
            self._app.calculate()
        elif keycode == 61:  # + key
            self._app.insert_sign('+')
        elif keycode == 45:  # - key
            self._app.insert_sign('-')
        elif keycode in self.operators:  # operators
            self._app.insert_operator(self.operators[keycode])
        return True


class Screen(BoxLayout):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self._num_pad_removed = False
        self.size_hint = (1, 1)
        self.setup_widgets()

    def setup_widgets(self) -> None:
        self.num_pad = NumPad()
        self.text_field = TextField()
        self.num_pad.size_hint = (1, 1)
        self.text_field.size_hint = (1, 1)
        self.add_widget(self.text_field)
        self.add_widget(self.num_pad)

    def show_num_pad(self, show: bool = True) -> None:
        if show:
            Window.remove_widget(self.show_button)
            self.add_widget(self.num_pad)
            self._num_pad_removed = False
            return
        self.remove_widget(self.num_pad)
        self._num_pad_removed = True
        self.show_button = MDFloatingActionButton(
            icon="icons/dial-pad.png",
            pos_hint={"right": 1, "y": 0},
            on_release=self.show_num_pad
        )
        Window.add_widget(self.show_button)

    def hide_num_pad(self) -> None:
        if not self._num_pad_removed:
            self.show_num_pad(False)


class CalculatorApp(MDApp, DisplayText):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.load_kv("numpad.kv")
        self.screen = Screen()
        self.text_field = self.screen.text_field

    def build(self) -> Screen:
        return self.screen

    def calculate(self) -> None:
        self.show_calculation()

        label_height = self.text_field.height
        font_size = self.text_field.label.font_size
        lines = self.text_field.label.text.split('\n')

        # Hide numpad to display text hidden by numpad
        if len(lines) * font_size > label_height:
            self.screen.hide_num_pad()


if __name__ == '__main__':
    from kivy.utils import platform
    app = CalculatorApp()
    if platform not in ['android', 'ios']:
        app.title = "Kids Calculator"
        app.icon = "icons/calculator.png"
        Window.size = (380, 620)
    app.run()
