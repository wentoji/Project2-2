from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, ImageLeftWidget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from kivy.clock import Clock

from utils.MenuBar import MenuBar
from utils.session import get_user

class ChatScreen(MDScreen):
    def __init__(self, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)

        # Flag to ensure MenuBar is only added once.
        self._menubar_added = False

        # --------------------------
        # MAIN LAYOUT
        # --------------------------
        self.root_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(10),
            spacing=dp(10)
        )

        # --------------------------
        # HEADER WITH ICON & GREETING
        # --------------------------
        self.header_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(60),
            spacing=dp(10)
        )
        # Robot persona icon
        self.robot_icon = MDIconButton(
            icon="robot",
            icon_size="40sp"
        )
        # Greeting label (updated in on_pre_enter)
        self.greeting_label = MDLabel(
            text="",
            font_style="H5",
            halign="left",
            valign="middle"
        )
        self.header_layout.add_widget(self.robot_icon)
        self.header_layout.add_widget(self.greeting_label)

        # --------------------------
        # SCROLLABLE CHAT PANE
        # --------------------------
        self.chat_scroll = MDScrollView()
        self.chat_list = MDList()
        self.chat_scroll.add_widget(self.chat_list)

        # --------------------------
        # INPUT LAYOUT: TEXTFIELD & SEND BUTTON
        # --------------------------
        self.input_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(60),
            spacing=dp(10)
        )
        self.input_field = MDTextField(
            hint_text="Type your message...",
            size_hint=(0.8, None),
            height=dp(48)
        )
        self.send_button = MDRaisedButton(
            text="Send",
            size_hint=(0.2, None),
            height=dp(48)
        )
        self.send_button.bind(on_release=self.send_message)
        self.input_layout.add_widget(self.input_field)
        self.input_layout.add_widget(self.send_button)

        # --------------------------
        # ASSEMBLE THE MAIN SCREEN
        # --------------------------
        self.root_layout.add_widget(self.header_layout)
        self.root_layout.add_widget(self.chat_scroll)
        self.root_layout.add_widget(self.input_layout)
        self.add_widget(self.root_layout)

        # After a short delay, add the initial bot message
        Clock.schedule_once(self.add_initial_bot_message, 0.5)

    def on_pre_enter(self):
        # Update the greeting with the latest username when the screen is entered.
        username = get_user() or "User"
        self.greeting_label.text = f"Hello, {username} :)))"
        # Add the MenuBar if it hasn't been added yet and the screen manager is available.
        if self.manager and not self._menubar_added:
            self.add_menu_bar()
            self._menubar_added = True

    def add_menu_bar(self):
        # Create an AnchorLayout with pos_hint to stick the MenuBar in the top-right corner.
        menubar_anchor = AnchorLayout(
            pos_hint={'right': 1, 'top': 1},
            size_hint=(None, None),
            size=(dp(200), dp(56))
        )
        menu = MenuBar(screen_manager=self.manager)
        menubar_anchor.add_widget(menu)
        self.add_widget(menubar_anchor)

    def add_initial_bot_message(self, dt):
        # Add the first bot message welcoming the user.
        username = get_user() or "User"
        self.add_bot_message(f"Hello, {username}! How can I help you with your schedule today?")

    def add_bot_message(self, message):
        # Create a chat bubble for the bot (with a left icon)
        item = OneLineAvatarIconListItem(text=message)
        icon = ImageLeftWidget(source="robot_icon.png")  # Replace with your actual robot icon file
        item.add_widget(icon)
        self.chat_list.add_widget(item)
        # Scroll to the latest message.
        Clock.schedule_once(lambda dt: self.chat_scroll.scroll_to(item), 0.1)

    def add_user_message(self, message):
        # Create a chat bubble for the user.
        item = OneLineAvatarIconListItem(text=message)
        icon = ImageLeftWidget(source="user_icon.png")  # Replace with your actual user icon file if desired
        item.add_widget(icon)
        self.chat_list.add_widget(item)
        Clock.schedule_once(lambda dt: self.chat_scroll.scroll_to(item), 0.1)

    def send_message(self, instance):
        # When the send button is pressed, add the user's message and simulate a bot response.
        message = self.input_field.text.strip()
        if message:
            self.add_user_message(message)
            self.input_field.text = ""
            # Simulate a bot response after a delay (replace with your chatbot logic)
            Clock.schedule_once(lambda dt: self.add_bot_message("This is your bot response."), 1)

    def reset(self):
        """
        Reset the ChatScreen to its initial state:
        - Clear all chat messages.
        - Reset the input field.
        - Update the greeting with the current user.
        - Re-add the initial bot welcome message.
        """
        self.chat_list.clear_widgets()
        self.input_field.text = ""
        self.on_pre_enter()  # Updates the greeting (and adds the MenuBar if needed)
        self.add_initial_bot_message(0)  # Immediately add the welcome message


