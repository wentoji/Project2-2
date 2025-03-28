# Screens/LoginScreen.py
import os
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

# The KV code references root.bg_image_path


Builder.load_string('''
<LoginScreen>:
    name: "login_screen"

    MDFloatLayout:
        # Full-screen background image (pattern)
        FitImage:
            source: "Screens/imageStart.png"   # Ensure this image exists in the Screens folder
            allow_stretch: True
            keep_ratio: False

        # White container for the login form at the bottom
        MDBoxLayout:
            orientation: "vertical"
            size_hint_y: 0.65             # This container occupies the bottom 65% of the screen
            pos_hint: {"y": 0}            # Anchored to the bottom
            md_bg_color: 1, 1, 1, 1
            radius: [30, 30, 0, 0]
            padding: dp(20), dp(20)
            spacing: dp(15)

            MDLabel:
                text: "Login"
                halign: "center"
                font_style: "H4"
                size_hint_y: None
                height: self.texture_size[1]

            MDLabel:
                text: "Sign in to continue"
                halign: "center"
                font_style: "Body2"
                theme_text_color: "Custom"
                text_color: (0, 0, 0, 0.6)
                size_hint_y: None
                height: self.texture_size[1]

            MDTextField:
                id: username
                hint_text: "Name"
                icon_right: "account"
                size_hint_x: 0.8
                pos_hint: {"center_x": 0.5}

            MDTextField:
                id: password
                hint_text: "Password"
                icon_right: "lock"
                size_hint_x: 0.8
                pos_hint: {"center_x": 0.5}
                password: True

            MDRaisedButton:
                text: "Log In"
                md_bg_color: app.theme_cls.primary_dark  # Dark color for the login button
                pos_hint: {"center_x": 0.5}
                on_release:
                    root.try_login()

            MDLabel:
                id: message
                text: ""
                halign: "center"
                font_style: "Caption"
                theme_text_color: "Custom"
                text_color: (1, 0, 0, 1)
                size_hint_y: None
                height: self.texture_size[1]

            BoxLayout:
                orientation: "horizontal"
                size_hint_y: None
                height: dp(40)
                spacing: dp(10)
                pos_hint: {"center_x": 0.5}
                MDTextButton:
                    text: "Forgot Password?"
                    on_release:
                        # Handle forgot password logic here
                        pass
                MDLabel:
                    text: "|"
                    halign: "center"
                    size_hint_x: None
                    width: dp(10)
                    theme_text_color: "Custom"
                    text_color: (0, 0, 0, 0.6)
                MDTextButton:
                    text: "Signup!"
                    on_release:
                        root.go_to_signup()

        # Logo placed on top of everything, centered in the top region
        Image:
            source: "Screens/logo.png"   # Ensure this image exists in the Screens folder
            size_hint: None, None
            size: dp(150), dp(150)         # Adjust the size to make the logo bigger or smaller
            pos_hint: {"center_x": 0.5, "center_y": 0.825}
''')



class LoginScreen(MDScreen):
    # Expose a property so KV can do source: root.bg_image_path
    bg_image_path = StringProperty("")

    def try_login(self):
        # Your existing login logic
        from utils.AccountManager import authenticate
        from utils.session import set_user
        from kivy.utils import platform

        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()
        if authenticate(username, password):
            set_user(username)
            self.ids.username.text = ''
            self.ids.password.text = ''

            # Switch to the appropriate screen
            if platform in ['android', 'ios']:
                self.manager.current = 'chat'
            else:
                self.manager.current = 'chat'
        else:
            self.ids.message.text = '❌ Invalid username or password'

    def go_to_signup(self):
        self.manager.current = 'signup'
