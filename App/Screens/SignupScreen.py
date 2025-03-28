from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp

Builder.load_string('''
<SignupScreen>:
    name: "signup_screen"

    MDFloatLayout:
        # Background image covering the full screen
        FitImage:
            source: "Screens/imageStart.png"  # Make sure the image is in this folder
            allow_stretch: True
            keep_ratio: False

        # Logo positioned on top of the background
        Image:
            source: "Screens/logo.png"          # Path to your logo
            size_hint: None, None
            size: dp(150), dp(150)               # Adjust logo size as needed
            pos_hint: {"center_x": 0.5, "center_y": 0.825}

        # White rounded container for the signup form at the bottom
        MDBoxLayout:
            orientation: "vertical"
            size_hint_y: 0.65                    # Covers the bottom 65% of the screen
            pos_hint: {"y": 0}                   # Anchored at the bottom
            md_bg_color: 1, 1, 1, 1
            radius: [30, 30, 0, 0]
            padding: dp(20), dp(20)
            spacing: dp(15)

            MDLabel:
                text: "Signup"
                halign: "center"
                font_style: "H4"
                size_hint_y: None
                height: self.texture_size[1]

            MDLabel:
                text: "Create your account"
                halign: "center"
                font_style: "Body2"
                theme_text_color: "Custom"
                text_color: 0, 0, 0, 0.6
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
                text: "Sign Up"
                md_bg_color: app.theme_cls.primary_dark  # Dark color for the button
                pos_hint: {"center_x": 0.5}
                on_release:
                    root.try_signup()

            MDLabel:
                id: message
                text: ""
                halign: "center"
                font_style: "Caption"
                theme_text_color: "Custom"
                text_color: (1, 0, 0, 1)
                size_hint_y: None
                height: self.texture_size[1]

            # Footer row: link to the login screen
            BoxLayout:
                orientation: "horizontal"
                size_hint_y: None
                height: dp(40)
                spacing: dp(10)
                pos_hint: {"center_x": 0.5}

                MDLabel:
                    text: "Already have an account?"
                    halign: "center"
                    size_hint_x: None
                    width: dp(180)
                    theme_text_color: "Custom"
                    text_color: (0, 0, 0, 0.6)

                MDTextButton:
                    text: "Login"
                    on_release:
                        root.go_to_login()
''')


class SignupScreen(MDScreen):
    def try_signup(self):
        from utils.AccountManager import create_account
        from utils.session import set_user

        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()

        if create_account(username, password):
            set_user(username)
            self.ids.username.text = ''
            self.ids.password.text = ''
            self.ids.message.text = '✅ Account created! Proceed to onboarding.'
            self.manager.current = 'onboarding'
        else:
            self.ids.message.text = '⚠️ Username already exists'

    def go_to_login(self):
        self.manager.current = 'login'
