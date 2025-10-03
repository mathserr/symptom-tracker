from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import json
from datetime import datetime, date
class SymptomTracker(BoxLayout):
   def __init__(self, **kwargs):
       super().__init__(orientation="vertical", **kwargs)
       
       # Title
       title = Label(text="Daily Symptom Tracker", size_hint_y=None, height=50)
       self.add_widget(title)
       
       # Current datetime display
       self.current_datetime = datetime.now()
       self.datetime_label = Label(text=f"Logging for: {self.current_datetime.strftime('%Y-%m-%d %H:%M')}", size_hint_y=None, height=40)
       self.add_widget(self.datetime_label)
       
       # Date input for logging another day
       date_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=50)
       date_label = Label(text="Log for date (YYYY-MM-DD):", size_hint_x=0.4)
       self.date_input = TextInput(hint_text="2025-10-03", multiline=False, size_hint_x=0.4)
       change_date_btn = Button(text="Change Date", size_hint_x=0.2)
       change_date_btn.bind(on_press=self.change_date)
       
       date_layout.add_widget(date_label)
       date_layout.add_widget(self.date_input)
       date_layout.add_widget(change_date_btn)
       self.add_widget(date_layout)
       
       # Symptoms checkboxes
       self.symptoms = {}
       symptom_names = ["Stomach Pain", "Head Pain", "Knee Pain", "Bloated Feeling"]
       
       for symptom in symptom_names:
           # Create horizontal layout for each symptom
           symptom_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=40)
           
           # Checkbox
           checkbox = CheckBox(size_hint_x=None, width=50)
           self.symptoms[symptom] = checkbox
           
           # Label
           label = Label(text=symptom, halign="left")
           label.bind(size=label.setter('text_size'))
           
           symptom_layout.add_widget(checkbox)
           symptom_layout.add_widget(label)
           self.add_widget(symptom_layout)
       
       # Button to save
       save_btn = Button(text="Save Today's Symptoms", size_hint_y=None, height=50)
       save_btn.bind(on_press=self.save_symptoms)
       self.add_widget(save_btn)
       
       # Display log
       self.log_label = Label(text="Today's symptoms:\n", halign="left", valign="top")
       self.log_label.bind(size=self.log_label.setter('text_size'))
       self.add_widget(self.log_label)
       
       self.load_log()
   def save_symptoms(self, instance):
       # Use the current selected date
       selected_date = self.current_datetime.strftime('%Y-%m-%d')
       current_time = datetime.now().strftime('%H:%M:%S')
       
       # Get checked symptoms
       checked_symptoms = []
       for symptom_name, checkbox in self.symptoms.items():
           if checkbox.active:
               checked_symptoms.append(symptom_name)
       
       try:
           with open("symptom_log.json", "r") as f:
               data = json.load(f)
       except:
           data = {}
       
       # Create entry with datetime
       if selected_date not in data:
           data[selected_date] = []
       
       # Add new entry with timestamp
       entry = {
           "datetime": f"{selected_date} {current_time}",
           "symptoms": checked_symptoms
       }
       
       # Replace if logging for the same date, or add if new date
       data[selected_date] = [entry]  # For simplicity, replace existing entries for the same date
       
       with open("symptom_log.json", "w") as f:
           json.dump(data, f, indent=2)
       
       self.load_log()
   
   def change_date(self, instance):
       date_text = self.date_input.text.strip()
       if date_text:
           try:
               # Parse the input date
               selected_date = datetime.strptime(date_text, '%Y-%m-%d')
               self.current_datetime = selected_date
               self.datetime_label.text = f"Logging for: {self.current_datetime.strftime('%Y-%m-%d %H:%M')}"
               self.date_input.text = ""
               self.load_log()
           except ValueError:
               # Invalid date format, show error in label
               self.datetime_label.text = "Invalid date format! Use YYYY-MM-DD"
   
   def load_log(self):
       selected_date = self.current_datetime.strftime('%Y-%m-%d')
       try:
           with open("symptom_log.json", "r") as f:
               data = json.load(f)
       except:
           data = {}
       
       # Load symptoms for selected date
       date_entries = data.get(selected_date, [])
       
       # Clear all checkboxes first
       for symptom_name, checkbox in self.symptoms.items():
           checkbox.active = False
       
       # Get the latest entry for the selected date
       current_symptoms = []
       entry_datetime = ""
       if date_entries:
           if isinstance(date_entries[0], dict):  # New format
               latest_entry = date_entries[-1]  # Get the most recent entry
               current_symptoms = latest_entry.get('symptoms', [])
               entry_datetime = latest_entry.get('datetime', '')
           else:  # Old format compatibility
               current_symptoms = date_entries
       
       # Update checkbox states
       for symptom_name, checkbox in self.symptoms.items():
           checkbox.active = symptom_name in current_symptoms
       
       # Update display text
       if current_symptoms:
           symptoms_text = "\n".join([f"✓ {symptom}" for symptom in current_symptoms])
           if entry_datetime:
               display_text = f"Symptoms for {selected_date}:\nLogged at: {entry_datetime}\n\n{symptoms_text}"
           else:
               display_text = f"Symptoms for {selected_date}:\n{symptoms_text}"
       else:
           display_text = f"No symptoms recorded for {selected_date}"
       
       self.log_label.text = display_text

class SymptomTrackerApp(App):
   def build(self):
       return SymptomTracker()

if __name__ == "__main__":
   SymptomTrackerApp().run()