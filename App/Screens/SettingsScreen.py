from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from kivy.clock import Clock

from utils.MenuBar import MenuBar

class SettingsScreen(MDScreen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

        # Outer layout for the main content
        self.root_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(10)
        )

        # Content layout for settings information
        self.layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(10)
        )

        self.title_label = MDLabel(
            text="Settings & Customization",
            font_style="H5",
            halign="center"
        )
        self.info_label = MDLabel(
            text="Adjust your preferences, manage data, and review account settings.",
            font_style="Body1",
            halign="center"
        )

        self.change_pass_btn = MDRaisedButton(
            text="Change Password (Coming Soon)",
            size_hint=(1, None),
            height=dp(48)
        )
        self.manage_categories_btn = MDRaisedButton(
            text="Manage Categories (Coming Soon)",
            size_hint=(1, None),
            height=dp(48)
        )
        self.clear_data_btn = MDRaisedButton(
            text="Clear Data (Coming Soon)",
            size_hint=(1, None),
            height=dp(48)
        )

        # Add widgets to the content layout
        self.layout.add_widget(self.title_label)
        self.layout.add_widget(self.info_label)
        self.layout.add_widget(self.change_pass_btn)
        self.layout.add_widget(self.manage_categories_btn)
        self.layout.add_widget(self.clear_data_btn)

        # Add the content layout to the root layout
        self.root_layout.add_widget(self.layout)
        self.add_widget(self.root_layout)

        # Flag to prevent multiple menubar additions
        self._menubar_added = False

    def on_pre_enter(self):
        # Only add the MenuBar when the screen is about to be entered, and when the screen manager exists.
        if self.manager and not self._menubar_added:
            self.add_menu_bar()
            self._menubar_added = True

    def add_menu_bar(self):
        # Create an AnchorLayout with pos_hint to position at the top right.
        menubar_anchor = AnchorLayout(
            pos_hint={'right': 1, 'top': 1},
            size_hint=(None, None),
            size=(dp(200), dp(56))
        )
        # Create the MenuBar using the screen manager (which is now available).
        menu = MenuBar(screen_manager=self.manager)
        menubar_anchor.add_widget(menu)
        # Add the menubar overlay to the screen.
        self.add_widget(menubar_anchor)
