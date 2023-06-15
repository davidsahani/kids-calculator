from kivy.clock import Clock
from kivymd.uix.button import MDRaisedButton


class DelayedButton(MDRaisedButton):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.delay = 0.5
        self._duration_count = 0.0
        self._long_press_clock_event = None
        self._long_press_callback = kwargs.get('on_long_press')
        self.register_event_type('on_long_press')

    def _start_long_press_clock(self) -> None:
        self._long_press_clock_event = Clock.schedule_interval(
            self._check_long_press_duration, 0.1)

    def _stop_long_press_clock(self) -> None:
        if self._long_press_clock_event is None:
            return
        self._long_press_clock_event.cancel()
        self._long_press_clock_event = None
        self._duration_count = 0.0

    def _check_long_press_duration(self, dt: float) -> None:
        if self._duration_count >= self.delay:
            self._stop_long_press_clock()
            self.dispatch('on_long_press')
        else:
            self._duration_count += dt

    def on_touch_down(self, touch) -> bool:
        if touch.is_mouse_scrolling:
            return False
        if not self.collide_point(*touch.pos):
            return False
        self._is_long_press = True
        self._start_long_press_clock()
        return super().on_touch_down(touch)

    def on_touch_move(self, touch) -> bool:
        if not self.collide_point(*touch.pos):
            self._stop_long_press_clock()
        return super().on_touch_move(touch)

    def on_touch_up(self, touch) -> bool:
        self._stop_long_press_clock()
        return super().on_touch_up(touch)

    def on_long_press(self) -> None:
        if self._long_press_callback is not None:
            self._long_press_callback(self)
