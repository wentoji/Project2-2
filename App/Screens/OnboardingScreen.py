import re
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp

from utils.session import get_user
from utils.AccountManager import load_users, save_users

class OnboardingScreen(MDScreen):
    def __init__(self, **kwargs):
        super(OnboardingScreen, self).__init__(**kwargs)

        # We'll store the user’s scheduling onboarding data here
        self.user_data = {
            'biggest_struggle': None,
            'chronotype': None,
            'motivation_style': None,
            'mood_impact': None,
            'connect_calendar': None
        }

        # Define the steps with widget types and, if dropdown, a list of options
        self.steps = [
            {
                'question': "What is your biggest struggle with scheduling? (Choose one)",
                'key': 'biggest_struggle',
                'validate': self.validate_struggle,
                'widget_type': 'dropdown',
                'options': ["Procrastination", "Organization", "Overcommitment", "Other"]
            },
            {
                'question': "Are you a morning bird or a night owl?",
                'key': 'chronotype',
                'validate': self.validate_chronotype,
                'widget_type': 'dropdown',
                'options': ["Morning", "Night"]
            },
            {
                'question': "Which best describes you: More routine-oriented or sudden sparks of motivation?",
                'key': 'motivation_style',
                'validate': self.validate_motivation,
                'widget_type': 'dropdown',
                'options': ["Routine", "Spontaneous"]
            },
            {
                'question': "On a scale of 1-5, how much does your mood impact your productivity?",
                'key': 'mood_impact',
                'validate': self.validate_mood_impact,
                'widget_type': 'textfield'
            },
            {
                'question': "Connect your calendar:",
                'key': 'connect_calendar',
                'validate': None,  # No validation for a placeholder
                'widget_type': 'button'
            }
        ]
        self.current_step = 0

        # --------------------------
        # LAYOUT & UI
        # --------------------------
        self.root_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(10)
        )

        self.layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10)
        )

        self.question_label = MDLabel(
            font_style="H6",
            halign="left",
            text=""
        )
        self.error_label = MDLabel(
            text="",
            halign="left",
            theme_text_color="Error"
        )
        # Create an input container so we can easily replace its content
        self.input_container = MDBoxLayout(size_hint=(1, None), height=dp(48))

        # Navigation buttons
        self.nav_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint=(1, None),
            height=dp(48)
        )
        self.back_button = MDRaisedButton(text="< Back")
        self.next_button = MDRaisedButton(text="Next >")
        self.back_button.bind(on_press=self.go_back)
        self.next_button.bind(on_press=self.go_next)
        self.nav_layout.add_widget(self.back_button)
        self.nav_layout.add_widget(self.next_button)

        # Assemble the main layout
        self.layout.add_widget(self.question_label)
        self.layout.add_widget(self.error_label)
        self.layout.add_widget(self.input_container)
        self.layout.add_widget(self.nav_layout)

        self.root_layout.add_widget(self.layout)
        self.add_widget(self.root_layout)

        # Placeholder for the dropdown menu; will be set in create_dropdown
        self.dropdown_menu = None

        # Show the first step
        self.show_step(0)

    # ----------------------------------------------------------------
    # Step Display / Navigation
    # ----------------------------------------------------------------
    def show_step(self, step_index):
        """Update UI for the current step, create proper input widget and clear previous error/input."""
        if step_index < 0 or step_index >= len(self.steps):
            return

        step_data = self.steps[step_index]
        self.question_label.text = step_data['question']
        self.error_label.text = ""

        # Clear the input container
        self.input_container.clear_widgets()

        # Create a new input widget based on widget_type
        widget_type = step_data.get("widget_type", "textfield")
        if widget_type == "dropdown":
            self.input_widget = self.create_dropdown(step_data['options'])
        elif widget_type == "button":
            self.input_widget = self.create_connect_calendar_widget()
        else:
            self.input_widget = MDTextField(
                multiline=False,
                size_hint=(1, None),
                height=dp(48)
            )
        self.input_container.add_widget(self.input_widget)
        self.back_button.disabled = (step_index == 0)

        if step_index == len(self.steps) - 1:
            self.next_button.text = "Finish"
        else:
            self.next_button.text = "Next >"

    def go_next(self, instance):
        """When Next/Finish is pressed, validate & store current answer, then proceed."""
        step_data = self.steps[self.current_step]
        key = step_data['key']

        # For button widget, assume the action already stored its value.
        if step_data.get("widget_type") == "button":
            raw_answer = self.user_data.get(key, "")
        else:
            raw_answer = self.input_widget.text.strip()

        if step_data.get('validate'):
            error_msg = step_data['validate'](raw_answer)
            if error_msg:
                self.error_label.text = f"Error: {error_msg}"
                return

        self.user_data[key] = raw_answer

        if self.current_step == len(self.steps) - 1:
            self.complete_onboarding()
        else:
            self.current_step += 1
            self.show_step(self.current_step)

    def go_back(self, instance):
        """Navigate back one step."""
        if self.current_step > 0:
            self.current_step -= 1
            self.show_step(self.current_step)

    def complete_onboarding(self):
        """Onboarding complete: save data and transition screens."""
        username = get_user()  # Ensure set_user(username) was called after signup
        self.save_onboarding_data(username)
        print("Onboarding complete! Data collected:", self.user_data)
        # Transition to your main scheduling/chatbot screen; update as needed.
        self.manager.current = 'chat'

    # ----------------------------------------------------------------
    # Creating Specialized Input Widgets
    # ----------------------------------------------------------------
    def create_dropdown(self, options):
        """Creates an MDTextField with an attached dropdown menu that opens on touch."""
        dropdown_field = MDTextField(
            multiline=False,
            size_hint=(1, None),
            height=dp(48),
            readonly=True,
            hint_text="Select an option"
        )

        # Build menu items for the dropdown; using lambda with a default arg to capture the option
        menu_items = []
        for option in options:
            menu_items.append({
                "viewclass": "OneLineListItem",
                "text": option,
                "on_release": lambda opt=option: self.dropdown_callback(opt)
            })

        self.dropdown_menu = MDDropdownMenu(
            caller=dropdown_field,
            items=menu_items,
            width_mult=4
        )

        # Instead of binding on_focus, bind on_touch_down so the menu opens when tapped.
        dropdown_field.bind(on_touch_down=self.dropdown_touch_down)
        return dropdown_field

    def dropdown_touch_down(self, instance, touch):
        """Open dropdown when the field is touched."""
        if instance.collide_point(*touch.pos):
            self.dropdown_menu.open()
        return False  # Allow other touch events to propagate

    def dropdown_callback(self, selection):
        """Handle selection from the dropdown menu."""
        self.input_widget.text = selection
        self.dropdown_menu.dismiss()

    def create_connect_calendar_widget(self):
        """Creates a placeholder button for connecting the calendar."""
        btn = MDRaisedButton(
            text="Connect Calendar (Placeholder)",
            size_hint=(1, None),
            height=dp(48)
        )
        btn.bind(on_release=self.on_connect_calendar)
        return btn

    def on_connect_calendar(self, instance):
        """Placeholder action for connecting a calendar."""
        instance.text = "Calendar Connected"
        self.user_data['connect_calendar'] = "Connected"

    # ----------------------------------------------------------------
    # Save Onboarding Data to JSON
    # ----------------------------------------------------------------
    def save_onboarding_data(self, username):
        """Merge the wizard data into the user’s record in users.json."""
        users = load_users()
        if username not in users:
            users[username] = {}
        if isinstance(users[username], str):
            hashed_pass = users[username]
            users[username] = {'password': hashed_pass}
        users[username]['onboarding'] = self.user_data
        save_users(users)

    # ----------------------------------------------------------------
    # Validation Methods
    # ----------------------------------------------------------------
    def validate_struggle(self, answer):
        valid_options = ['procrastination', 'organization', 'overcommitment', 'other']
        if answer.lower() not in valid_options:
            return ("Please select one of the options: Procrastination, Organization, Overcommitment, Other.")
        return ""

    def validate_chronotype(self, answer):
        valid = ['morning', 'night']
        if answer.lower() not in valid:
            return "Please select 'Morning' or 'Night'."
        return ""

    def validate_motivation(self, answer):
        valid = ['routine', 'spontaneous']
        if answer.lower() not in valid:
            return "Please select 'Routine' or 'Spontaneous'."
        return ""

    def validate_mood_impact(self, answer):
        if not answer.isdigit():
            return "Please enter a number between 1 and 5."
        num = int(answer)
        if not (1 <= num <= 5):
            return "Please enter a number between 1 and 5."
        return ""
