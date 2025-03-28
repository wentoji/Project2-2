import os
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from App.Screens.LoginScreen import LoginScreen
from App.Screens.SignupScreen import SignupScreen
from App.Screens.OnboardingScreen import OnboardingScreen
from App.Screens.ChatScreen import ChatScreen
from App.Screens.SettingsScreen import SettingsScreen
from App.Screens.CalendarScreen import CalendarScreen

class MainApp(MDApp):
    def build(self):
        # Create a ScreenManager
        sm = ScreenManager()

        # Build the path to your image file
        current_dir = os.path.dirname(__file__)
        # Adjust if "imageStart.png" is in a different folder:
        image_path = os.path.join(current_dir, "Screens", "imageStart.png")

        # Create the LoginScreen instance and set bg_image_path
        login_screen = LoginScreen(name='login')
        login_screen.bg_image_path = image_path

        # Add screens
        sm.add_widget(login_screen)
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(OnboardingScreen(name='onboarding'))
        sm.add_widget(ChatScreen(name='chat'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(CalendarScreen(name='calendar'))

        # Start on the login screen
        sm.current = "login"
        return sm

if __name__ == '__main__':
    MainApp().run()
