#global variables
import joblib
from tensorflow import Variable, zeros

from tensorflow.keras import layers, Model, utils
#from tensorflow.keras.callbacks import EarlyStopping
from sentence_transformers import SentenceTransformer
from tensorflow.keras.callbacks import ModelCheckpoint
import numpy as np
import pandas as pd

#combined_dataset = pd.read_json('/home/karar/Desktop/recom/data_scraping/preprocessed/combined_dataset.json')
import tensorflow as tf


from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QLineEdit, QGridLayout, QHBoxLayout, QVBoxLayout, QTextEdit,
    QFrame, QScrollArea, QMessageBox, QSpinBox
)
from PyQt6 import QtWidgets
import sys
import json
import os
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QPixmap, QMovie

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))

import recommendatoin_systems.two_tower_model
from chatbot import bot
from various_preprocessing.utils import Autoencoder
from recommendatoin_systems.personality_nn import VectorCombiner
users_file = "users.json"


items_embedd = np.load('./item_embedding.npy')
items_embedd = np.stack(items_embedd)
items_embedd = tf.convert_to_tensor(items_embedd , dtype=tf.float32)

user_personality = Variable(zeros([len(items_embedd[1])]))
vec_dim = len(items_embedd[1])

my_vect_model = SentenceTransformer("paraphrase-MiniLM-L12-v2")
mlb_skill = joblib.load('../models/recommendatoin_systems/final_Models/mlb_skill.pkl')

skill_dim= 11898
encoder_skill = Autoencoder(skill_dim, latent_dim=24)

dummy_input = tf.keras.Input(shape=(skill_dim,))
encoder_skill(dummy_input)  # Build the model
encoder_skill.load_weights('../models/recommendatoin_systems/final_Models/autoencoderweights.weights.h5')
#normalization_layer = tf.keras.layers.Normalization()

normalization_layer = tf.keras.models.load_model(
    '../models/recommendatoin_systems/final_Models/norm_layer.keras',
    custom_objects={'Normalization': tf.keras.layers.Normalization}
)
#normalization_layer = tf.keras.models.load_model('../models/recommendatoin_systems/final_Models/norm_layer')




def load_users():
    if not os.path.exists(users_file):
        return {}
    with open(users_file, 'r') as f:
        return json.load(f)


def save_users(users):
    with open(users_file, 'w') as f:
        json.dump(users, f, indent=4)


def save_user(email, username, password):
    users = load_users()
    if username in users:
        return False  # Username already exists
    users[username] = {"email": email, "password": password}
    save_users(users)
    return True


def authenticate_user(username, password):
    if not os.path.exists(users_file):
        return "no_file"  # No user file found
    users = load_users()
    if username in users and users[username]['password'] == password:
        return True  # Authentication success
    return False  # Authentication failure


class Login(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Logo/Image
        label = QLabel(self)
        pixmap = QPixmap("photo_2025-03-27_15-33-18-removebg-preview.png")

        pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio,
                              Qt.TransformationMode.SmoothTransformation)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(label)

        # Grid Layout for Inputs
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        # Labels & Input Fields
        label1 = QLabel("Username:")
        label1.setStyleSheet("font-size: 20px;color:#F5EEDC;")
        self.user_input = QLineEdit()
        self.user_input.setStyleSheet("font-size: 16px; height: 25px;background-color:white;")
        self.user_input.setPlaceholderText("Enter your username (e.g. teeba99)")

        label2 = QLabel("Password:")
        label2.setStyleSheet("font-size: 20px; color:#F5EEDC; ")
        self.pass_input = QLineEdit()
        self.pass_input.setStyleSheet("font-size: 16px; height: 25px;background-color:white; ")
        self.pass_input.setPlaceholderText("Enter your password")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        grid_layout.addWidget(label1, 0, 0)
        grid_layout.addWidget(self.user_input, 0, 1)
        grid_layout.addWidget(label2, 3, 0)
        grid_layout.addWidget(self.pass_input, 3, 1)
        grid_layout.setContentsMargins(40, 40, 40, 40)

        layout.addLayout(grid_layout)  # Add grid to main layout

        # Buttons Layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        button1 = QPushButton("Register")
        button2 = QPushButton("Login")

        button1.setStyleSheet("""
                QPushButton{
                     font-size: 16px; 
                    padding: 6px;
                    background-color:#b35c44; 
                    color:white;
                    border-radius: 5px;
                    
                    
                }              
                   
    QPushButton:hover {
        background-color: #f1a8a1;  /* Light red color when hovered */
        font-size: 20px;
    }
    """)

        button2.setStyleSheet("""
                               QPushButton{
                     font-size: 16px; 
                    padding: 6px;
                    background-color:#b35c44; 
                    color:white;
                    border-radius: 5px;
                    
                    
                }              
                   
    QPushButton:hover {
        background-color: #f1a8a1;  /* Light red color when hovered */
        font-size: 20px;
    }
                              
                              """)

        button_layout.addWidget(button1)
        button_layout.addWidget(button2)
        button_layout.setContentsMargins(40, 40, 40, 40)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button1.setFixedSize(250, 40)
        button2.setFixedSize(250, 40)

        layout.addLayout(button_layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        container_widget = QWidget(self)
        container_widget.setLayout(layout)
        container_widget.setFixedSize(1000, 1000)
        container_widget.setStyleSheet("background-color:#4F959D ; radius:50%;")

        main_layout = QVBoxLayout()
        main_layout.addWidget(container_widget)
        self.setLayout(main_layout)

        main_layout.addWidget(container_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        button1.clicked.connect(self.goToRegist)
        button2.clicked.connect(self.goToMain)

    def goToRegist(self):
        self.parent().setCurrentIndex(1)  # Switch to registration window

    def goToMain(self):
        username = self.user_input.text()
        password = self.pass_input.text()
        result = authenticate_user(username, password)
        if result == "no_file":
            QMessageBox.warning(self, "Error", "No accounts exist. Please register first.")
        elif result:
            QMessageBox.information(self, "Success", "Login successful!")
            self.parent().setCurrentIndex(2)
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password.")


class Regist(QWidget):
    def __init__(self):
        super().__init__()

        layoutR = QVBoxLayout()
        self.setLayout(layoutR)
        label = QLabel(self)
        pixmap = QPixmap("photo_2025-03-27_15-33-18-removebg-preview.png")

        pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio,
                              Qt.TransformationMode.SmoothTransformation)
        label.setPixmap(pixmap)
        label.setContentsMargins(0, 0, 0, 0)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layoutR.addWidget(label)

        # Grid Layout for Inputs
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        # Labels & Input Fields
        labelR = QLabel("Email:")
        labelR.setStyleSheet("font-size: 20px;color:#F5EEDC;")

        self.email_input = QLineEdit()
        self.email_input.setStyleSheet("font-size: 16px; height: 25px;background-color:white;")
        self.email_input.setPlaceholderText("Enter your email (e.g. teeba99@gmail.com)")

        labelR3 = QLabel("Username:")
        labelR3.setStyleSheet("font-size: 20px; color:#F5EEDC; ")
        self.user_input = QLineEdit()
        self.user_input.setStyleSheet("font-size: 16px; height: 25px;background-color:white; ")
        self.user_input.setPlaceholderText("Enter your Username")

        labelR2 = QLabel("Password:")
        labelR2.setStyleSheet("font-size: 20px; color: #F5EEDC; ")

        self.pass_input = QLineEdit()
        self.pass_input.setStyleSheet("font-size: 16px; height: 25px;background-color:white; ")
        self.pass_input.setPlaceholderText("Enter your password")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        grid_layout.addWidget(labelR, 0, 0)
        grid_layout.addWidget(self.email_input, 0, 1)
        grid_layout.addWidget(labelR3, 3, 0)
        grid_layout.addWidget(self.user_input, 3, 1)
        grid_layout.addWidget(labelR2, 6, 0)
        grid_layout.addWidget(self.pass_input, 6, 1)

        grid_layout.setContentsMargins(50, 50, 50, 50)

        layoutR.addLayout(grid_layout)  # Add grid to the layout

        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        buttonM = QPushButton("Regist")
        buttonM.setStyleSheet("""
                QPushButton{
                     font-size: 16px; 
                    padding: 6px;
                    background-color:#b35c44; 
                    color:white;
                    border-radius: 5px;
                    
                    
                }              
                   
    QPushButton:hover {
        background-color: #f1a8a1;  /* Light red color when hovered */
        font-size: 20px;}
    """)
        buttonM.setFixedSize(300, 40)
        button_layout.addWidget(buttonM)
        button_layout.setContentsMargins(40, 40, 40, 40)

        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutR.addLayout(button_layout)

        buttonM.clicked.connect(self.goToMain)

    def goToMain(self):
        email = self.email_input.text()
        username = self.user_input.text()
        password = self.pass_input.text()

        if not email or not username or not password:
            QMessageBox.warning(self, "Error", "All fields are required,please fill them")
            return
        if "@" not in email or ".com" not in email:
            QMessageBox.warning(self, "Error", "Please enter a valid email address")
            return

        # Save the user data in the file
        if save_user(email, username, password):
            QMessageBox.information(self, "Success", "Account created successfully!")

            self.parent().setCurrentIndex(2)
        else:
            QMessageBox.warning(self, "Error", "Username already exists.")

class MessageBubble(QFrame):
    def __init__(self, text, sender, courses_for_rating=None):
        super().__init__()
        layout = QHBoxLayout()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(10, 10, 10, 10) # Add some padding inside

        if courses_for_rating:
            label = QLabel("Please rate these courses:")
            label.setWordWrap(True)
            label.setStyleSheet("font-size: 14px; color: white; padding: 10px;")
            content_layout.addWidget(label)
            for course_title, course_index in courses_for_rating:
                course_layout = QHBoxLayout()
                course_label = QLabel(course_title)
                course_label.setStyleSheet("font-size: 14px;")
                rating_spinbox = QSpinBox()
                rating_spinbox.setRange(0, 5)
                course_layout.addWidget(course_label)
                course_layout.addWidget(rating_spinbox)
                content_layout.addLayout(course_layout)
                setattr(self, f"spinbox_{course_index}", rating_spinbox)
            widget = QWidget()
            widget.setLayout(content_layout)
            if sender == "User":
                widget.setStyleSheet("background-color:white; border-radius: 10px; padding: 10px;")
                widget.setContentsMargins(15,15,15,15)
                layout.addStretch()
                layout.addWidget(widget)
            else:
                widget.setStyleSheet("background-color: #4F949D ; border-radius: 10px;color:white; padding: 10px;")
                layout.addWidget(widget)
                layout.addStretch()

        else:
            label = QLabel(text)
            label.setWordWrap(True)
            if sender == "User":
                label.setStyleSheet("background-color:white; border-radius: 10px; padding: 10px")
                layout.addStretch()
                layout.addWidget(label)
            else:
                label.setStyleSheet("background-color: #4F949D ; border-radius: 10px;color:white; padding: 10px")
                layout.addWidget(label)
                layout.addStretch()
            content_layout.addWidget(label)
            widget = QWidget()
            widget.setLayout(content_layout)
            layout.addWidget(widget)
            if sender == "User":
                layout.setAlignment(Qt.AlignmentFlag.AlignRight)
            else:
                layout.setAlignment(Qt.AlignmentFlag.AlignLeft)


        self.setLayout(layout)

    def get_course_ratings(self, courses_for_rating):
        ratings = {}
        for _, course_index in courses_for_rating:
            spinbox = getattr(self, f"spinbox_{course_index}", None)
            if spinbox:
                ratings[course_index] = spinbox.value()
        return ratings


class ModernChatbot(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.typing_bubble = None  # Initialize typing_bubble
        self.last_courses_for_rating = None # To store courses for rating display

    def init_ui(self):
        self.setStyleSheet("background-color: #d4cebe")
        layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.addStretch()
        self.scroll_area.setWidget(self.chat_container)
        layout.addWidget(self.scroll_area)
        self.typing_icon = QLabel()
        self.typing_icon.setStyleSheet("background: transparent;")
        self.typing_icon.setFixedSize(85, 85)
        self.typing_icon.setVisible(False)  # hidden by default
        self.chat_layout.addWidget(self.typing_icon, alignment=Qt.AlignmentFlag.AlignLeft)
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setStyleSheet(
            "border: 2px solid #ccc; border-radius: 5px; padding: 5px;background-color:white")
        self.input_field.returnPressed.connect(self.handle_message)  # Handle Enter key press
        input_layout.addWidget(self.input_field)
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("background-color: #007BFF; color: white; border-radius: 5px; padding: 5px;")
        self.send_button.clicked.connect(self.handle_message)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)
        self.setLayout(layout)

    def add_message(self, text, sender, courses_for_rating=None):
        message_bubble = MessageBubble(text, sender, courses_for_rating)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, message_bubble)
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
        return message_bubble

    def handle_message(self):
        user_message = self.input_field.text().strip()
        if user_message:
            self.last_user_message = user_message  # Store the message before clearing the animation of dots
            self.add_message(user_message, "User")
            self.input_field.clear()
            self.show_typing_animation()
            self.show_animation()

    def show_typing_animation(self):
        self.typing_bubble = MessageBubble(". .", "Bot")
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, self.typing_bubble)
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
        self.typing_index = 0
        self.typing_animation = [". . .", ". .", "."]
        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(self.update_typing_animation)
        self.typing_timer.start(500)

    def show_animation(self):
        gif_path = "video-2025-04-02-22-12-45-unscreen.gif"
        movie = QMovie(gif_path)
        movie.setScaledSize(self.typing_icon.size())  # Resize GIF to icon size
        self.typing_icon.setMovie(movie)
        self.typing_icon.setVisible(True)
        movie.start()

        QTimer.singleShot(2000, self.remove_typing_animation)

    def remove_typing_animation(self):
        self.typing_icon.setVisible(False)

    def update_typing_animation(self):
        if self.typing_bubble:  # Check if typing_bubble exists
            label_item = self.typing_bubble.layout().itemAt(0)
            if label_item and label_item.widget() and isinstance(label_item.widget(), QLabel):
                if self.typing_index < len(self.typing_animation):
                    label_item.widget().setText(self.typing_animation[self.typing_index])
                    self.typing_index += 1
                else:
                    self.typing_timer.stop()
                    self.chat_layout.removeWidget(self.typing_bubble)
                    self.typing_bubble.deleteLater()
                    self.typing_bubble = None  # Reset typing_bubble
                    QTimer.singleShot(500, self.process_bot_response)  # Delay before response
            else:
                self.typing_timer.stop()
                if self.typing_bubble in self.chat_layout:
                    self.chat_layout.removeWidget(self.typing_bubble)
                    self.typing_bubble.deleteLater()
                    self.typing_bubble = None
                QTimer.singleShot(500, self.process_bot_response)  # Fallback

    def process_bot_response(self):
        bot_response = self.get_response(self.last_user_message)
        if isinstance(bot_response, list) and all(isinstance(item, tuple) and len(item) == 2 for item in
                                                 bot_response):
            self.last_courses_for_rating = bot_response # Store the courses for rating display later
            self.display_courses_for_rating(bot_response)
        else:
            self.add_message(bot_response, "Bot")

    def display_courses_for_rating(self, courses_with_indices):
        self.rating_message_bubble = self.add_message("Please rate these courses:", "Bot",
                                                    courses_for_rating=courses_with_indices)
        submit_button_layout = QHBoxLayout()
        submit_button = QPushButton("Submit Ratings")
        submit_button.clicked.connect(self.collect_ratings)
        submit_button_layout.addStretch()
        submit_button_layout.addWidget(submit_button)
        submit_button_layout.addStretch()
        submit_widget = QWidget()
        submit_widget.setLayout(submit_button_layout)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, submit_widget)
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
    def collect_ratings(self):
        if self.rating_message_bubble and self.last_courses_for_rating:
            ratings = self.rating_message_bubble.get_course_ratings(self.last_courses_for_rating)
            rated_courses_info = []
            if ratings:
                for (title, index), rating in zip(self.last_courses_for_rating, ratings.values()):
                    if rating > 0:  # Check if the rating is greater than 0
                        rated_courses_info.append(f"- {title}: {rating}/5")

                if rated_courses_info:
                    ratings_text = "You rated the following courses:\n" + "\n".join(rated_courses_info)
                    self.add_message(ratings_text, "Bot")
                else:
                    self.add_message("No courses were rated.", "Bot")
            else:
                self.add_message("No courses were rated.", "Bot")
        self.rating_message_bubble = None  # Reset for next rating request
        self.last_courses_for_rating = None # Reset stored courses

    def get_response(self, message):
        #just for testing
        if "RECOMMENDED:" in message:

            courses = [("Introduction to AI", 101), ("Advanced Machine Learning", 102),
                       ("Natural Language Processing", 103), ("Computer Vision Basics", 104)]
            return courses
        else:
            return bot.handle_message(message, my_vect_model, mlb_skill, normalization_layer , encoder_skill)

app = QApplication(sys.argv)
app.setStyleSheet("""
    QLineEdit { background-color: white; padding: 5px; border-radius: 5px; }
    QPushButton { font-size: 16px; padding: 5px; border-radius: 5px; }
""")

widget = QtWidgets.QStackedWidget()
widget.setWindowIcon(QIcon("photo_2025-03-27_15-33-18-removebg-preview.png"))
widget.resize(350, 320)
widget.setWindowTitle(" Quamus ")

login = Login()
regist = Regist()
main_chat = ModernChatbot()
widget.addWidget(login)
widget.addWidget(regist)
widget.addWidget(main_chat)

widget.setStyleSheet("background-color:#4F949D ")
widget.setCurrentIndex(0)
widget.show()

sys.exit(app.exec())

app = QApplication(sys.argv)
app.setStyleSheet("""
    QLineEdit { background-color: white; padding: 5px; border-radius: 5px; }
    QPushButton { font-size: 16px; padding: 5px; border-radius: 5px; }
""")

widget = QtWidgets.QStackedWidget()
widget.setWindowIcon(QIcon("photo_2025-03-27_15-33-18-removebg-preview.png"))
widget.resize(350, 320)
widget.setWindowTitle(" Quamus ")

login = Login()
regist = Regist()
main_chat = ModernChatbot()
widget.addWidget(login)
widget.addWidget(regist)
widget.addWidget(main_chat)

widget.setStyleSheet("background-color:#4F949D ")
widget.setCurrentIndex(0)
widget.show()

sys.exit(app.exec())
