from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem
from kivy.metrics import dp

class MenuBar(MDBoxLayout):
    def __init__(self, screen_manager, **kwargs):
        super(MenuBar, self).__init__(**kwargs)
        # Make the menubar span the full width at the top.
        self.size_hint = (1, None)
        self.height = dp(56)
        self.orientation = 'horizontal'
        self.padding = dp(10)  # small left/right padding
        self.screen_manager = screen_manager

        # Define the menu items.
        # "Home" corresponds to your ChatScreen (registered as 'chat'),
        # "Calendar" for your Calendar screen (registered as 'calendar'),
        # "Settings" to the settings screen,
        # and "Logout" sends you back to login (resetting all screens with a reset() method).
        self.menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Home",
                "height": dp(48),
                "on_release": lambda x="chat": self.select_screen(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Calendar",
                "height": dp(48),
                "on_release": lambda x="calendar": self.select_screen(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Settings",
                "height": dp(48),
                "on_release": lambda x="settings": self.select_screen(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Logout",
                "height": dp(48),
                "on_release": lambda x="logout": self.select_screen(x)
            }
        ]

        # Create the actual MDDropdownMenu.
        self.menu = MDDropdownMenu(
            caller=None,  # We'll set the caller below.
            items=self.menu_items,
            width=dp(200)
        )

        # Icon button to open the dropdown menu.
        self.main_button = MDIconButton(
            icon="menu",
            pos_hint={"center_y": 0.5}
        )
        self.main_button.bind(on_release=lambda *args: self.open_menu())
        self.add_widget(self.main_button)

    def open_menu(self):
        """Open the MDDropdownMenu anchored to the icon button."""
        self.menu.caller = self.main_button  # Anchor to this button.
        self.menu.open()

    def select_screen(self, screen_name):
        """
        If 'Logout' is selected, iterate over all screens in the screen manager
        and call their reset() method if available. Then switch to the 'login' screen.
        Otherwise, simply switch to the selected screen.
        """
        if screen_name == "logout":
            for screen in self.screen_manager.screens:
                if hasattr(screen, 'reset') and callable(screen.reset):
                    screen.reset()
            self.screen_manager.current = "login"
        else:
            self.screen_manager.current = screen_name
        self.menu.dismiss()
