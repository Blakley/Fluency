import os
import sys
import json
import customtkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk

from urllib.parse import urlparse
from pathlib import Path
import importlib
import requests

import time
import threading
from plyer import notification
from playsound import playsound

# Import phrases database
import database


# import packages 
import pickle
import tensorflow as tf 
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer



'''
	Fluency Language Learning | Desktop Application 
'''
class Fluency():
	"""
		Constructor for the Interface class.
		Initializes the GUI and sets the default appearance.
	"""
	def __init__(self):
		# ----------------------------
		#   Initialize GUI properties
		# ----------------------------

		# customkinter defaults
		customtkinter.set_appearance_mode("dark")
		customtkinter.set_default_color_theme("dark-blue")

		self.gui = customtkinter.CTk()
		self.gui.title("")
		self.gui.resizable(False, False)
		self.gui.attributes('-topmost', True)

		self.dimension = [800, 400]
		self.gui.geometry(f"{self.dimension[0]}x{self.dimension[1]}")

        # Get the app icon file
		if sys.platform == 'win32':  # Windows platform
			self.icon = os.path.abspath('..\icons\icon.ico')
		else:  # assume Linux platform
			self.icon = os.path.abspath('../icons/icon.png')
		self.gui.iconbitmap(default=self.icon)
		# print('icon: ', self.icon)

		# -------------------------------------
		#   Initialize Notification properties
		# -------------------------------------

		# Define dictionary keys and storage file
		self.language_key = 'language'
		self.frequency_key = 'frequency'
		self.theme_key = 'theme'

		# Define notification variables   
		self.frequency_updated = False
		self.notification_list_updated = False
		self.schedule_id = -1 # ID of currently scheduled notifications event
		self.creating_notification = False  # Creating a new notification
		self.phrase_categories = {}

		# create app themes
		self.theme_a = customtkinter.CTkImage(Image.open("../icons/light-off.png"), size=(20, 20))
		self.theme_b = customtkinter.CTkImage(Image.open("../icons/light-on.png"), size=(20, 20))
		self.app_theme = self.theme_b

		# -------------------------------------------------
		#   Initialize Seq2Seq Translation model properties
		# -------------------------------------------------
		self.model = None
		self.model_setup()

		# Start application
		self.setup()
		self.tabs()
		self.gui.mainloop()


	"""
		===========================================
					Seq2Seq Model functions
		===========================================
	"""


	"""
		Load the translation model
	"""
	def model_setup(self):
		# Load the trained model
		self.model = load_model('translation-model')

		# Load the tokenizers
		with open('english_tokenizer.pickle', 'rb') as handle:
		    self.english_tokenizer = pickle.load(handle)

		with open('french_tokenizer.pickle', 'rb') as handle:
		    self.french_tokenizer = pickle.load(handle)

		self.model.summary()


	"""
	"""
	def model_execute_translator(self, phrase):
		input_sequence = self.english_tokenizer.texts_to_sequences([phrase])
		padded_input_sequence = pad_sequences(input_sequence, maxlen=sequence_len, padding='post')

		decoded_text = '[start]'

		# Generate French translation one token at a time
		for i in range(sequence_len):
		    # Convert the current decoded text to a sequence of tokens
		    target_sequence = self.french_tokenizer.texts_to_sequences([decoded_text])
		    
		    # Remove the last token ('[end]') to use the remaining part as input for the next prediction
		    padded_target_sequence = pad_sequences(target_sequence, maxlen=sequence_len, padding='post')[:, :-1]

		    # Predict the next token in the French translation
		    prediction = model.predict([padded_input_sequence, padded_target_sequence])

		    # Get the index of the predicted token with the highest probability
		    idx = np.argmax(prediction[0, i, :]) - 1
		    
		    # Map the index to the corresponding French word using fr_index_lookup
		    token = fr_index_lookup[idx]

		    # Append the predicted token to the decoded text
		    decoded_text += ' ' + token

		    # If the predicted token is '[end]', stop generating further tokens
		    if token == '[end]':
		        break

		# Remove the special tokens '[start]' and '[end]' from the final decoded text
		return decoded_text[8:-6]



	"""
		Use the model to generate the corresponding
		language translation text
	"""
	def model_translate(self):
		selected_language = self.create_lang_menu.get()

		phrase_translation = ""

		# only works for french thus far:
		if selected_language == "French":
			phrase = self.phrase_input.get()
			if len(phrase) > 0:
				phrase_translation = self.model_execute_translator(phrase)

		if selected_language == "Turkish":
			phrase_translation = "Bu bir testtir"

		if selected_language == "Kurdish":
			phrase_translation = "Ev ji testek e"

		self.translation_input.delete(0, 'end')
		self.translation_input.insert(0, phrase_translation)


	"""
		===========================================
					Interface functions
		===========================================
	"""

	"""
		Creates and configures the tabs in the GUI.
	"""
	def tabs(self):

		# Create fonts
		self.font_a = customtkinter.CTkFont(family="Arial", size=64, weight="bold")
		self.font_b = customtkinter.CTkFont(family="Arial", size=38, weight="bold")
		self.font_c = customtkinter.CTkFont(family="Arial", size=14)
		self.font_d = customtkinter.CTkFont(family="Arial", size=18)

		self.tabview = customtkinter.CTkTabview(
			master=self.gui,
			width=(self.dimension[0]-100),
			height=(self.dimension[1]-50),
			border_width=0,
			corner_radius=0,
			text_color=["white", "white"],
			fg_color=["gray95", "gray10"]
		)
		self.tabview.pack(padx=100, pady=0, anchor=tk.CENTER, )
		

		# Main tab: Start notifications
		self.tabview.add("Home")
		self.tabview.set("Home")  # sets default tab

		# Create tab: Create new notifications
		self.tabview.add("Create")

		# Settings tab: Notifications settings
		self.tabview.add("Settings")

		# Create tab elements
		self.home_tab()
		self.creation_tab()
		self.settings_tab()

		# load application theme
		self.load_theme()

		# Create language cateogories
		self.update_categories()
 

	"""
		[Home Tab] Configurations
	"""
	def home_tab(self):
		# App name
		app_name = customtkinter.CTkLabel(
			master=self.tabview.tab("Home"),
			text="FLUENCY",
			fg_color="transparent",
			font=self.font_a
		)
		app_name.pack(pady=(20, 0), padx=(35, 25), anchor=tk.CENTER)

		# App description
		app_description = customtkinter.CTkLabel(
			master=self.tabview.tab("Home"),
			text="Unlock a world of languages",
			fg_color="transparent",
			font=self.font_c
		)

		app_description.pack(padx=50, pady=(0, 0), anchor=tk.CENTER)

		# Start Notifications button
		self.notify = customtkinter.CTkButton(
			master=self.tabview.tab("Home"),
			text="START",
			command=self.notifications_timer
		)
		self.notify.pack(padx=0, pady=(40, 5), anchor=tk.CENTER)


	"""
		[Create Tab] Configurations
	"""
	def creation_tab(self):

		# Notification creator frame
		dim = [self.dimension[0]-100, self.dimension[1]-100] # 800x400
		frame = customtkinter.CTkFrame(
			master=self.tabview.tab("Create"),
			width=dim[0],
			height=dim[1],
		)
		frame.pack(anchor=tk.CENTER, pady=(0, 10))

		# Tab Name
		tab_name = customtkinter.CTkLabel(
			master=self.tabview.tab("Create"),
			text="Notification Creator",
			fg_color=["gray90", "gray13"],
			font=self.font_b
		)
		tab_name.place(x=(dim[0]//2)-50, y=(dim[1]//2)-100, anchor=tk.CENTER)

		# Tab description
		tab_description = customtkinter.CTkLabel(
			master=self.tabview.tab("Create"),
			text="Create language translation notifications",
			fg_color=["gray90", "gray13"],
			font=self.font_c
		)

		tab_description.place(x=(dim[0]//2)-50, y=(dim[1]//2)-65, anchor=tk.CENTER)

		# phrase input
		self.phrase_input = customtkinter.CTkEntry(
			master=self.tabview.tab("Create"),
			placeholder_text="Phrase: ",
			corner_radius=0,
			width=(dim[0]//2) + 50
		)
		self.phrase_input.place(x=dim[0]-(dim[0]-20), y=(dim[1]//2)-20)

		# translation input
		self.translation_input = customtkinter.CTkEntry(
			master=self.tabview.tab("Create"),
			placeholder_text="Translation: ",
			corner_radius=0,
			width=(dim[0]//2) + 50
		)
		self.translation_input.place(x=dim[0]-(dim[0]-20), y=(dim[1]//2)+20)

		# category input
		self.category_input = customtkinter.CTkEntry(
			master=self.tabview.tab("Create"),
			placeholder_text="Phrase category: ",
			corner_radius=0,
			width=(dim[0]//2) + 50
		)
		self.category_input.place(x=dim[0]-(dim[0]-20), y=(dim[1]//2)+60)

		# audio source input
		self.audio_input = customtkinter.CTkEntry(
			master=self.tabview.tab("Create"),
			placeholder_text="Audio URL: ",
			corner_radius=0,
			width=(dim[0]//2) + 50
		)
		self.audio_input.place(x=dim[0]-(dim[0]-20), y=(dim[1]//2)+100)

		# browse for audio button
		audio_button = customtkinter.CTkButton(
			master=self.tabview.tab("Create"),
			text="Browse",
			command=self.browse_single_audio,
			width=50,
			height=20,
			corner_radius=0,
			text_color=["white", "white"],
			fg_color=["gray", "gray"],
		)
		audio_button.place(x=(dim[0]//2)+15, y=(dim[1]//2)+104)

		# Language selection dropdown
		value = self.languages[self.main_language]
		choice = customtkinter.StringVar(value=value)
		self.create_lang_menu = customtkinter.CTkOptionMenu(
			master=self.tabview.tab("Create"),
			values=["French", "Turkish", "Kurdish"],
			corner_radius=0,
			command=self.language_menu_create,
			variable=choice,
			text_color=["white", "white"],
			button_color=["#3d3e40", "#3d3e40"],
			fg_color=["gray", "gray"],
		)
		self.create_lang_menu.set(value)
		self.create_lang_menu.place(x=(dim[0]//2)+75, y=(dim[1]//2)-20)


		# Generate Translation button
		generate_button = customtkinter.CTkButton(
		    master=self.tabview.tab("Create"),
		    text="Generate",
		    corner_radius=0,
		    text_color=["white", "white"],
		    fg_color=["gray", "gray"],
		    command=self.model_translate,
		)
		generate_button.place(x=(dim[0]//2)+75, y=(dim[1]//2)+20)


		# Create new notification button
		create_button = customtkinter.CTkButton(
			master=self.tabview.tab("Create"),
			text="Create",
			corner_radius=0,
			text_color=["white", "white"],
			fg_color=["gray", "gray"],
			command=self.create_notification,
		)
		create_button.pack(pady=(10, 0), anchor=tk.CENTER)


	"""
		Configures the elements in the Settings tab.
	"""
	def settings_tab(self):
		dim = [self.dimension[0]-100, self.dimension[1]-100] # 800x400

		# Notifications frame
		frame_a = customtkinter.CTkFrame(
			master=self.tabview.tab("Settings"),
			width=(dim[0]//2),
			height=(dim[1])+40,
		)
		frame_a.grid(row=0, column=0, pady=(10, 0))

		# Misc settings frame
		frame_b = customtkinter.CTkFrame(
			master=self.tabview.tab("Settings"),
			width=(dim[0]//2)-100,
			height=(dim[1])+40,
		)
		frame_b.grid(row=0, column=1, pady=(10, 0), padx=(10, 0))

		# Frame a: description
		self.fa_description = customtkinter.CTkLabel(
			master=self.tabview.tab("Settings"),
			text=f'Notifications : {self.languages[self.main_language]}',
			fg_color=["gray90", "gray13"],
			font=self.font_d
		)

		# calculate description placement and place text
		self.title_pos = {
			'fr' : 259,
			'tr' : 254,
			'ku' : 253,
		} 
		self.fa_description.place(x=(dim[0]//2)-(self.title_pos[self.main_language]), y=(dim[1]//2)-115, anchor=tk.CENTER)


		# Delete button
		delete_button = customtkinter.CTkButton(
			master=self.tabview.tab("Settings"),
			text="Delete",
			corner_radius=0,
			width=70,
			text_color=["white", "white"],
			fg_color=["gray", "gray"],
			command=self.delete_notification,
		)
		delete_button.place(x=(dim[0]//2)-(self.title_pos[self.main_language])+210,  y=(dim[1]//2)-115, anchor=tk.CENTER)


		# Notification list box
		self.notification_list = tk.Listbox(
			master=self.tabview.tab("Settings"), 
			bg="#212121",
			fg="white",
			font=self.font_c,
			width=(dim[0]//2)-309,
			height=17,
			borderwidth=2,
			highlightthickness=0
		)

		# Bind select event to the listbox
		self.notification_list.place(x=(dim[0]//2)-340, y=(dim[1]//2)-100)
		self.notification_list.bind("<<ListboxSelect>>", self.notification_select)

		# Frame b: description
		fb_description = customtkinter.CTkLabel(
			master=self.tabview.tab("Settings"),
			text="Notification Settings:",
			fg_color=["gray90", "gray13"],
			font=self.font_d
		)
		fb_description.place(x=(dim[0]//2)+100, y=(dim[1]//2)-115, anchor=tk.CENTER)

		# Light/Dark theme button
		self.theme_button = customtkinter.CTkButton(
			master=self.tabview.tab("Settings"),
			image=self.app_theme,
			text="",
			anchor="center",
			width=0,
			corner_radius=0,
			hover_color=["gray", "gray"],
			fg_color=["gray90", "gray13"],
			command=self.application_theme,
		)
		self.theme_button.place(x=dim[0]-115, y=(dim[1]//2)-115, anchor=tk.CENTER)

		# Frequency section
		frequency_text = customtkinter.CTkLabel(
			master=self.tabview.tab("Settings"),
			text="Notification Frequency:",
			fg_color=["gray90", "gray13"],
			font=self.font_c
		)
		frequency_text.place(x=(dim[0]//2)+90, y=(dim[1]//2)-80, anchor=tk.CENTER)


		# Frequency radio buttons
		self.frequency_value = tk.IntVar(value=self.initial_frequency)
		frequencyA = customtkinter.CTkRadioButton(
			master=self.tabview.tab("Settings"), 
			text="Frequently",
			command = self.frequency_selection, 
			variable= self.frequency_value, 
			value=1,
			bg_color=["gray90", "gray13"],
		)

		frequencyB = customtkinter.CTkRadioButton(
			master=self.tabview.tab("Settings"), 
			text="Occasionally",
			command = self.frequency_selection, 
			variable= self.frequency_value, 
			value=2,
			bg_color=["gray90", "gray13"],
		)

		frequencyC = customtkinter.CTkRadioButton(
			master=self.tabview.tab("Settings"), 
			text="Infrequently",
			command = self.frequency_selection, 
			variable= self.frequency_value, 
			value=3,
			bg_color=["gray90", "gray13"],
		)

		frequencyA.place(x=(dim[0]//2)+70, y=(dim[1]//2)-55, anchor=tk.CENTER)
		frequencyB.place(x=(dim[0]//2)+70, y=(dim[1]//2)-30, anchor=tk.CENTER)
		frequencyC.place(x=(dim[0]//2)+70, y=(dim[1]//2)-5, anchor=tk.CENTER)

		# Notification language selection Text
		notification_text = customtkinter.CTkLabel(
			master=self.tabview.tab("Settings"),
			text="Notification Language:",
			fg_color=["gray90", "gray13"],
			font=self.font_c
		)
		notification_text.place(x=(dim[0]//2)+90, y=(dim[1]//2)+30, anchor=tk.CENTER)

		# Notification language selection dropdown menu		
		value = self.languages[self.main_language]
		choice = customtkinter.StringVar(value=value)
		self.main_lang_menu = customtkinter.CTkOptionMenu(
			master=self.tabview.tab("Settings"),
			values=["French", "Turkish", "Kurdish"],
			corner_radius=0,
			command=self.language_menu_main,
			variable=choice,
			text_color=["white", "white"],
			button_color=["#3d3e40", "#3d3e40"],
			fg_color=["gray", "gray"],
		)

		self.main_lang_menu.set(value)
		self.main_lang_menu.place(x=(dim[0]//2)+90, y=(dim[1]//2)+60, anchor=tk.CENTER)		

		# Notification language category selection Text
		phrase_category = customtkinter.CTkLabel(
			master=self.tabview.tab("Settings"),
			text="Phrase Category:",
			fg_color=["gray90", "gray13"],
			font=self.font_c
		)
		phrase_category.place(x=(dim[0]//2)+75, y=(dim[1]//2)+100, anchor=tk.CENTER)

		# Notification language category selection dropdown menu		
		category_value = "All"
		category_choice = customtkinter.StringVar(value=category_value)
		self.category_menu = customtkinter.CTkOptionMenu(
			master=self.tabview.tab("Settings"),
			values=["All"],
			corner_radius=0,
			command=self.category_changed,
			variable=category_choice,
			text_color=["white", "white"],
			button_color=["#3d3e40", "#3d3e40"],
			fg_color=["gray", "gray"],
			width=dim[1]//2 + 70
		)

		self.category_menu.set(category_value)
		self.category_menu.place(x=(dim[0]//2)+130, y=(dim[1]//2)+130, anchor=tk.CENTER)	


	"""
		Event handler for the Start Notifications button.
		Disables the Start button and enables the Stop button.
	"""
	def notifications_timer(self):
		# Update the button state
		text = ''
		state = self.notify.cget("text")	
		if state == 'START':
			text = 'STOP'
			self.notify.configure(text=f'{text}')
			self.start_notifications()
		else:
			text = 'START'
			self.notify.configure(text=f'{text}')
			self.end_notifications()

		# self.gui.iconify()
		self.notify.configure(state='disabled')
		self.gui.after(2000, self.notification_state)
		

	"""
		Notifications button state timer
		Handles button pressing delays
	"""
	def notification_state(self):
		# enable notifications button
		self.notify.configure(state='normal')


	"""
		Logic to handle creation of a new notification
		Handles making and storing new notification data
	"""
	def create_notification(self):
		print('Create a notification')
		self.creating_notification = True

		# Get user input values
		lang = self.create_lang_menu.get()
		phrase = self.phrase_input.get()
		translation = self.translation_input.get()

		# Handle if audio or local file is provided, prioritizing provided URL source
		audio = ''
		audio_url = self.audio_input.get()
		audio_file = None

		try:
			audio_file = self.audio_file
		except Exception as e:
			pass

		# Select file or URL
		if audio_url and self.check_audio_url(audio_url):
			print('Using audio URL:', audio_url)
			audio = audio_url
		elif audio_file:
			print('Using audio file:', audio_file)
			audio = audio_file
		else:
			print('No audio URL or file provided')

		# handle phrases in 'All' category
		category = self.category_input.get()
		if category == 'All':
			category = ''
		elif len(category) > 20:
			# Limit category text length to 20 characters
			messagebox.showwarning("Category Error", "The category can not be more than 20 characters long.")
			return

		# Create a new phrase object
		phrase_obj = [lang, phrase, translation, category, audio]
		self.all_notifications.append(phrase_obj)

		# Update the notification list in settings
		self.update_categories()

		# Update database file with newly created notification
		new_notification = {
			'phrase' : phrase,
			'translation' : translation,
			'category' : category,
			'audio': audio
		}

		updated_database = database.phrases
		for k, v in updated_database.items():
			# phrase_list = v
			language = self.languages[k]
			if lang == language:
				# update file
				updated_database[k].append(new_notification)
				self.update_file(updated_database, 'Notification successfully created')
				break

		# Clear the input fields
		self.phrase_input.delete(0, tk.END)
		self.translation_input.delete(0, tk.END)
		self.category_input.delete(0, tk.END)
		self.audio_input.delete(0, tk.END)
		self.audio_input.configure(placeholder_text='Audio URL: ')


	"""
		Notification selection handler
		Gets a notification from the listbox
	"""
	def notification_select(self, event):
		index = self.notification_list.curselection()
		if index:
			selected = self.notification_list.get(index)
			print(f"Selected Notification: {selected}")


	"""
		Logic to handle deleting existing notifications
	"""
	def delete_notification(self):
		# Warn users about phrase deletion 
		response = messagebox.askyesno("Confirmation", "Deleting this phrase will permanently delete it. Are you sure you want to delete?")
		if response:
			index = self.notification_list.curselection()
			if index:
				selected = self.notification_list.get(index)
				# extract phrase output
				extracted_phrase = selected.split(' |')[0].replace('Phrase: ', '')

				# Remove notification from notifications_list
				lang = self.languages[self.main_language]
				for i in range(len(self.all_notifications)):
		            # Get language
					if lang == self.all_notifications[i][0]:
						phrase = self.all_notifications[i][1]
						# Get selected phrase from list
						if phrase == extracted_phrase:
							# remove phrase from list
							self.all_notifications.pop(i)
							print('Removed phrase from all notifications')
							break

				# Remove category if empty
				category_count = {'All': 0}
				for n in self.all_notifications:
					if lang == n[0]:
						category = n[3]
						category_count[category] = category_count.get(category, 0) + 1
						category_count['All'] += 1

				# Remove and reset selected category in dropdown
				for k, v in self.phrase_categories.items():
					initial_length = len(v)
					v[:] = [c for c in v if c in category_count]
					if len(v) < initial_length:
						print('Removing category')
						self.reset_category()

				# Remove notification from listbox
				self.notification_list.delete(index)
				self.update_categories()

				# Update storage file, database.py, remove phrase
				self.remove_phrase(extracted_phrase)
			else:
				messagebox.showwarning("No Selection", "Please select a notification to delete.")


	"""
		Notification listbox tester
		Creates categories for each language
	"""
	def update_categories(self):
		# Load/Create phrase categories
		for n in self.all_notifications:
			lang = n[0]
			category = n[3]

			# store new language
			if lang not in self.phrase_categories:
				self.phrase_categories[lang] = []

			# store new category for language
			if category not in self.phrase_categories[lang]:
				self.phrase_categories[lang].append(category)

			# create default category if not created
			if 'All' not in self.phrase_categories[lang]:
				self.phrase_categories[lang].insert(0, 'All')

		# Update phrase category dropdown
		for k, v in self.phrase_categories.items():
			if k == self.languages[self.main_language]:
				self.category_menu.configure(values=v)
				break

		# Populate notification listbox with phrases from category for current language
		self.update_notification_list()


	"""
		Sets the currently selected category to the default: 'All'
	"""
	def reset_category(self):
		print('Resetting categories')
		category_value = 'All'
		category_choice = customtkinter.StringVar(value=category_value)		
		self.category_menu.configure(variable=category_choice)
		self.category_menu.set(category_value)


	"""
		Changes the notifications being displayed in settings
		Handler for notification list
	"""
	def update_notification_list(self):
		# all_notifications : ([lang, p['phrase'], p['translation'], category, p['audio']])		

		# Clear current list
		self.notification_list_updated = True
		self.notification_list.delete(0, tk.END)

		selected_category = self.category_menu.get()
		
		# Update list with notifications matching the language & selected category
		for n in self.all_notifications:
			# Get current main notification language
			if n[0] == self.languages[self.main_language]:
				# Get current phrase category
				if selected_category == n[3]:
					# display phrases from selected category
					phrase = f'Phrase: {n[1]} | Translation: {n[2]} | Audio: {n[4]}'
					self.notification_list.insert(tk.END, phrase)
				elif selected_category == 'All':
					# display all phrases
					phrase = f'Phrase: {n[1]} | Translation: {n[2]} | Audio: {n[4]}'
					self.notification_list.insert(tk.END, phrase)

		# Restart notification scheduler if calling function is create_notification()
		create_lang = self.create_lang_menu.get()
		if self.languages[self.main_language] == create_lang:		
			if self.creating_notification:
				print('Ending old notifications')
				self.creating_notification = False	
				self.end_notifications()


	"""
		 Validates if a URL points to an audio MP3 file
	"""
	def check_audio_url(self, url):
	    parsed_url = urlparse(url)
	    file_extension = Path(parsed_url.path).suffix

	    if file_extension.lower() == ".mp3":
	        # Additional check: download the file and verify its content
	        try:
	            response = requests.head(url)
	            content_type = response.headers.get('content-type')

	            if content_type == "audio/mpeg":
	                return True
	        except requests.exceptions.RequestException:
	            pass

	    return False


	"""
		Event handler for the Browse Audio button.
		Searches for locally stored audio file instead of from URL
	"""
	def browse_single_audio(self):
		self.audio_file = filedialog.askopenfilename(
			initialdir = "/",
			title = "Select an audio file",
			filetypes = (("Audio MP3", "*.mp3"),)
		)

		if self.audio_file:
			print("file: ", self.audio_file)
			self.audio_input.configure(placeholder_text=self.audio_file)
		else:
			print("No files selected.")


	"""
		Event handler for the Language selection dropdown in creation tab
	"""
	def language_menu_create(self, choice):		
		print("Changed language creation to:", choice)


	"""
		Event handler for the desktop notifications
		Update the language of the notifications
	"""
	def language_menu_main(self, choice):		
		# Get new notification language
		lang = next((key for key, val in self.languages.items() if val == choice), None)
		self.main_language = lang

		# Update storage file with new language
		print('Updating main language')
		self.storage[self.language_key] = self.main_language
		with open(self.storage_file, 'w') as f:
			json.dump(self.storage, f, indent=4, separators=(',', ': '))

		# Update 'Create' Tab current selected language in dropdown menu'
		value = self.languages[self.main_language]
		choice = customtkinter.StringVar(value=value)
		self.create_lang_menu.configure(variable=choice)
		self.create_lang_menu.set(value)

		# Update 'Settings' Tab notifications list title
		dim = [self.dimension[0]-100, self.dimension[1]-100]
		self.fa_description.configure(text=f'Notifications : {self.languages[self.main_language]}')
		self.fa_description.place(x=(dim[0]//2)-(self.title_pos[self.main_language]), y=(dim[1]//2)-115, anchor=tk.CENTER)

		# Change to the select language's notification list & categories
		self.reset_category()
		self.update_categories()
		self.end_notifications()


	"""
		Event handler for Notification frequency changes
	"""
	def frequency_selection(self):
		print("Frequency changed, current value:", self.frequency_value.get())

		# update the frequency
		if self.frequency_value.get() == 1:
			# self.selected_frequency = 10000  # Debugger: 10 seconds
			self.selected_frequency = 60 * 5 * 1000  # 5 minutes
		elif self.frequency_value.get() == 2:
			self.selected_frequency = 60 * 15 * 1000 # 15 minutes
		else:
			self.selected_frequency = 60 * 30 * 1000 # 30 minutes

		# Update the frequency in the storage file
		self.frequency_updated = True
		self.storage[self.frequency_key] = self.selected_frequency

		with open(self.storage_file, 'w') as f:
			json.dump(self.storage, f, indent=4, separators=(',', ': '))

		self.end_notifications() # update notification timing


	"""
		Event handler for Notification Phrase categories
		Populate notification listbox with phrases from category for current language
	"""
	def category_changed(self, choice):
		self.language_index = 0 # reset index
		self.initial_call = True

		print('Resetting language_index: ', self.language_index)
		self.update_notification_list()


	"""
		Event handler for application theme
		Toggles the color theme between dark and light
	"""
	def application_theme(self):
		# Handle loading initial theme
		if self.theme_button.cget('image') == self.theme_b:
			self.app_theme = self.theme_a
			self.storage[self.theme_key] = 'light'
			customtkinter.set_appearance_mode("light")

			# update notification list color
			self.notification_list.configure(bg="gray90")
			self.notification_list.configure(fg="black")
		else:
			self.app_theme = self.theme_b
			self.storage[self.theme_key] = 'dark'
			customtkinter.set_appearance_mode("dark")

			# update notification list color
			self.notification_list.configure(bg="#212121")
			self.notification_list.configure(fg="white")

		self.theme_button.configure(image=self.app_theme)

		# update theme in storage
		with open(self.storage_file, 'w') as f:
			json.dump(self.storage, f, indent=4, separators=(',', ': '))


	"""
		Loads initial application theme
		Obtains theme from storage and loads it
	"""
	def load_theme(self):		
		# Get theme from storage
		self.current_theme = self.storage[self.theme_key]

		# check current theme/switch theme
		if self.current_theme == 'dark':
			self.app_theme = self.theme_b
			customtkinter.set_appearance_mode("dark")

			# update notification list color
			self.notification_list.configure(bg="#212121")
			self.notification_list.configure(fg="white")
		else:
			self.app_theme = self.theme_a
			self.storage[self.theme_key] = 'light'
			customtkinter.set_appearance_mode("light")

			# update notification list color
			self.notification_list.configure(bg="gray90")
			self.notification_list.configure(fg="black")

		self.theme_button.configure(image=self.app_theme)


	"""
		Replaces the database.py file with the newly updated one
		After a notification is created
	"""
	def update_file(self, updated_database, message):
		# Convert the dictionary to JSON format
		json_data = json.dumps(updated_database, indent=4, ensure_ascii=False)

		# Create the file content with the variable assignment
		file_content = f"# Language phrase database\nphrases = {json_data}"

		# Open the file and write the JSON data
		with open('database.py', 'w', encoding='utf-8') as file:
			file.write(file_content)

		# Reload the module
		importlib.reload(database)
		messagebox.showinfo("Notifications updated", f"{message}")
		print('Updated database file')
		

	"""
		Replaces the database.py file with the newly updated one
		After a notification is deleted
	"""
	def remove_phrase(self, phrase):
		updated_database = database.phrases

		found = False
		for language, phrase_list in updated_database.items():
			if language == self.main_language:
				print(f'Rmoving {phrase} from database')

				for i, p in enumerate(phrase_list):
					if p['phrase'] == phrase:
						print('Exists and removing', p)
						del phrase_list[i]
						found = True
						self.language_index = 0
						self.initial_call = True
						break
			if found:
				break

		# update file
		self.update_file(updated_database, 'Notification successfully deleted')


	"""
		===========================================
				Desktop Notification functions
		===========================================
	"""
		
	"""
		Connects the language data to the interface
	"""
	def setup(self):
		# Current languages & notifications
		self.all_notifications = []
		self.languages = {
			'fr' : 'French',
			'tr' : 'Turkish',
			'ku' : 'Kurdish'
		}

		# Open notifications local storage file
		self.storage_file = 'storage.json'
		with open(self.storage_file, 'r') as f:
			self.storage = json.load(f)

		# Get application notification language
		self.main_language = self.storage[self.language_key]
		print('main language: ', self.main_language)

		# Setup intial frequncy and the frequency option selection
		self.selected_frequency = 0
		self.initial_frequency = 0

		# Set initial notification index
		self.language_index = 0 
		self.initial_call = True

		frequency = self.storage['frequency']
		if frequency == 10000:
			self.selected_frequency = 10000 # 5 minutes
			self.initial_frequency = 1
		elif frequency == 60 * 15 * 1000:
			self.selected_frequency = 60 * 15 * 1000 # 15 minutes
			self.initial_frequency = 2
		else:
			self.selected_frequency = 60 * 30 * 1000 # 30 minutes
			self.initial_frequency = 3

		# Load notifications from storage
		phrases = database.phrases
		for k, v in phrases.items():
			phrase_list = v
			lang = self.languages[k]

			# create phrase object			
			for p in phrase_list:
				# handle empty categories
				category = ''
				if p['category'] == '':
					category = 'All'
				else:
					category = p['category'] 
				self.all_notifications.append([lang, p['phrase'], p['translation'], category, p['audio']])


	"""
		Handles logic for scheduling desktop notifications
		Scehdules notifications based on selected frequency
	"""
	def start_notifications(self):
		# Run as long as application started
		if self.notify.cget("text")	== 'STOP':
			# Show notifications
			self.display_notifications()

			# Setup the notification scheduler
			self.schedule_id = self.gui.after(self.selected_frequency, self.start_notifications)		


	"""
		Displays a desktop notification
		Handles logic for displaying the notification
	"""
	def display_notifications(self):		
		# Delay between notifications (initial call only)
		if self.initial_call:
			self.initial_call = False
			delay_thread = threading.Timer(5, self.display_notifications)
			delay_thread.start()
		else:
			# Get total number of items in the current notifications list
			total_items = self.notification_list.size()

			# Check bounds
			if self.language_index >= total_items:
				self.language_index = 0

			# Get item at current language index
			selected = self.notification_list.get(self.language_index)

			# Construct the notification elements
			phrase = selected.replace("Phrase:", "").replace("Translation:", "").replace("Audio:", "")
			parts = phrase.split('|') 

			audio_part = parts[2].strip()
			phrase_part = parts[0].strip()
			translation_part = parts[1].strip()

			print(phrase_part, translation_part, audio_part)

			# Show the notification
			notification.notify(
				title=phrase_part,
				message=translation_part,
				timeout=8,
				app_icon=self.icon
			)

			# Play audio
			if len(audio_part) > 0:
				playsound(audio_part)

			# Update index
			self.language_index += 1


	"""
		Disables desktop notifications
		Removes scheduled notifications or Updates scheduler timing
	"""
	def end_notifications(self):
		# stop current notifications
		self.gui.after_cancel(self.schedule_id)
		self.schedule_id = -1

		# reset notification indexing
		self.language_index = 0 
		self.initial_call = True
		print('Resetting language_index: ', self.language_index)

		# handle updated frequency
		if self.frequency_updated: 
			print('Updating notifications timing')
			self.frequency_updated = False
			self.start_notifications()
		elif self.notification_list_updated: 
			# handle language change for notification list
			print('Updating notifications list')
			self.notification_list_updated = False
			self.start_notifications()
		else:
			self.schedule_id == -1000 # ended
			print('Ending notifications')



# Start application
if __name__ == '__main__':
	app = Fluency()