from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from kivy.clock import Clock

from utils.MenuBar import MenuBar


class CalendarScreen(MDScreen):
    def __init__(self, **kwargs):
        super(CalendarScreen, self).__init__(**kwargs)

        # Flag to ensure the MenuBar is added only once.
        self._menubar_added = False

        # Main layout
        self.root_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20)
        )

        # Title
        self.title_label = MDLabel(
            text="Calendar",
            font_style="H5",
            halign="center"
        )

        # Placeholder Calendar Widget
        self.calendar_placeholder = MDLabel(
            text="(Placeholder for Calendar Widget)\n\nThis area will display your calendar events.\n\nConnect your iPhone/Google Calendar here.",
            halign="center",
            valign="middle",
            font_style="Body1"
        )

        # Connect button for calendar integration
        self.connect_button = MDRaisedButton(
            text="Connect Calendar",
            size_hint=(None, None),
            size=(dp(200), dp(48)),
            pos_hint={'center_x': 0.5}
        )
        self.connect_button.bind(on_release=self.connect_calendar)

        # Assemble the layout
        self.root_layout.add_widget(self.title_label)
        self.root_layout.add_widget(self.calendar_placeholder)
        self.root_layout.add_widget(self.connect_button)
        self.add_widget(self.root_layout)

    def on_pre_enter(self):
        # Add the MenuBar if the screen manager is available and it hasn't been added yet.
        if self.manager and not self._menubar_added:
            self.add_menu_bar()
            self._menubar_added = True

    def add_menu_bar(self):
        # Create an AnchorLayout with pos_hint to stick the MenuBar in the top right.
        menubar_anchor = AnchorLayout(
            pos_hint={'right': 1, 'top': 1},
            size_hint=(None, None),
            size=(dp(200), dp(56))
        )
        menu = MenuBar(screen_manager=self.manager)
        menubar_anchor.add_widget(menu)
        self.add_widget(menubar_anchor)

    def connect_calendar(self, instance):
        # Placeholder functionality: update text to indicate connection.
        self.calendar_placeholder.text = "Calendar Connected! (Placeholder)"
