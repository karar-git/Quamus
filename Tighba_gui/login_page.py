from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QLineEdit, QGridLayout, QHBoxLayout, QVBoxLayout,QTextEdit, QFrame, QScrollArea
)
from PyQt6 import QtWidgets
import sys
from PyQt6.QtCore import Qt,QTimer
from PyQt6.QtGui import QIcon, QPixmap

class Login(QWidget):
    def __init__(self):
        super().__init__() 
       
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Logo/Image
        label = QLabel(self)
        pixmap = QPixmap("Tighba_gui/photo_2025-03-27_15-33-18-removebg-preview.png") 
      
        pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        
        layout.addWidget(label)

        # Grid Layout for Inputs
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)  

        # Labels & Input Fields
        label1 = QLabel("Username:")
        label1.setStyleSheet("font-size: 20px;color:#F5EEDC;")
        input1 = QLineEdit()
        input1.setStyleSheet("font-size: 16px; height: 25px;background-color:white;")  # Adjust height
        input1.setPlaceholderText("Enter your username (e.g. teeba99)")
        label2 = QLabel("Password:")
        label2.setStyleSheet("font-size: 20px; color:#F5EEDC; ")
        input2 = QLineEdit()
        input2.setStyleSheet("font-size: 16px; height: 25px;background-color:white; ")
        input2.setPlaceholderText("Enter your password")
        input2.setEchoMode(QLineEdit.EchoMode.Password)

        grid_layout.addWidget(label1, 0, 0)
        grid_layout.addWidget(input1, 0, 1)
        grid_layout.addWidget(label2, 3, 0)
        grid_layout.addWidget(input2, 3, 1)
        grid_layout.setContentsMargins(40,40,40,40)
         

        layout.addLayout(grid_layout)  # Add grid to main layout

        # Buttons Layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)  # Space between buttons

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
        button_layout.setContentsMargins(40,40,40,40)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button1.setFixedSize(250,40)
        button2.setFixedSize(250,40)
       
        

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
        self.parent().setCurrentIndex(2)#Switch to main chat window
        
        
class Regist(QWidget):
    def __init__(self):
        super().__init__()
        
       
        layoutR=QVBoxLayout()
        self.setLayout(layoutR)
        label = QLabel(self)
        pixmap = QPixmap("Tighba_gui/photo_2025-03-27_15-33-18-removebg-preview.png") 
      
        pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        label.setPixmap(pixmap)
        label.setContentsMargins(0,0,0,0)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        
        layoutR.addWidget(label)
         # Grid Layout for Inputs
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)  

        # Labels & Input Fields
        labelR = QLabel("Email:")
        labelR.setStyleSheet("font-size: 20px;color:#F5EEDC;")
        
        inputR = QLineEdit()
        inputR.setStyleSheet("font-size: 16px; height: 25px;background-color:white;") 
        inputR.setPlaceholderText("Enter your email (e.g. teeba99@gmail.com)")
        
        labelR3=QLabel("Username:")
        labelR3.setStyleSheet("font-size: 20px; color:#F5EEDC; ")
        inputR3 = QLineEdit()
        inputR3.setStyleSheet("font-size: 16px; height: 25px;background-color:white; ")
        inputR3.setPlaceholderText("Enter your Username")
        
        
        labelR2 = QLabel("Password:")
        labelR2.setStyleSheet("font-size: 20px; color: #F5EEDC; ")
        
        inputR2 = QLineEdit()
        inputR2.setStyleSheet("font-size: 16px; height: 25px;background-color:white; ")
        inputR2.setPlaceholderText("Enter your password")
        inputR2.setEchoMode(QLineEdit.EchoMode.Password)

        grid_layout.addWidget(labelR, 0, 0)
        grid_layout.addWidget(inputR, 0, 1)
        grid_layout.addWidget(labelR3, 3, 0)
        grid_layout.addWidget(inputR3, 3, 1)
        grid_layout.addWidget(labelR2, 6, 0)
        grid_layout.addWidget(inputR2, 6, 1)
        
        
        grid_layout.setContentsMargins(50,50,50,50)
         

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
        buttonM.setFixedSize(300,40)
        button_layout.addWidget(buttonM)
        button_layout.setContentsMargins(40,40,40,40)
        
       
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutR.addLayout(button_layout) 
        layoutR.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_widget = QWidget(self)
        container_widget.setLayout(layoutR)
        container_widget.setFixedSize(1000, 1000)
     
        
        
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(container_widget)
        self.setLayout(main_layout)
        
        main_layout.addWidget(container_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        
        buttonM.clicked.connect(self.goToMain)
        

class MessageBubble(QFrame):
    def __init__(self, text, sender):
        super().__init__()
        layout = QHBoxLayout()
        label = QLabel(text)
        label.setWordWrap(True)
        
        if sender == "User":
            label.setStyleSheet("background-color:white; padding: 10px; border-radius: 10px;")
            layout.addStretch()
            layout.addWidget(label)
            
        else:
            #this gonna be for the bot and the messege will be aligned to the left
            label.setStyleSheet("background-color: #4F949D ; padding: 10px; border-radius: 10px;color:white")
            layout.addWidget(label)
            layout.addStretch()
        
        self.setLayout(layout)
        
        
class ModernChatbot(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

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
        
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setStyleSheet("border: 2px solid #ccc; border-radius: 5px; padding: 5px;background-color:white")
        self.input_field.returnPressed.connect(self.handle_message)  # Handle Enter key press
        input_layout.addWidget(self.input_field)
        
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("background-color: #007BFF; color: white; border-radius: 5px; padding: 5px;")
        self.send_button.clicked.connect(self.handle_message)
        input_layout.addWidget(self.send_button)
        
        layout.addLayout(input_layout)
        self.setLayout(layout)




    def add_message(self, text, sender):
        message_bubble = MessageBubble(text, sender)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, message_bubble)
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())


    def handle_message(self):
        user_message = self.input_field.text().strip()
        if user_message:
            self.last_user_message = user_message  # Store the message before clearing the animation of dots
            self.add_message(user_message, "User")
            self.input_field.clear()
            self.show_typing_animation()




    def show_typing_animation(self):
        self.typing_bubble = MessageBubble(". .", "Bot")
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, self.typing_bubble)
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
        self.typing_index = 0
        self.typing_animation = [". . .", ". .", "."]
        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(self.update_typing_animation)
        self.typing_timer.start(500)

    def update_typing_animation(self):
        if self.typing_index < len(self.typing_animation):
            self.typing_bubble.layout().itemAt(0).widget().setText(self.typing_animation[self.typing_index])
            self.typing_index += 1
        else:
            self.typing_timer.stop()
            self.chat_layout.removeWidget(self.typing_bubble)
            self.typing_bubble.deleteLater()
            QTimer.singleShot(500, self.show_bot_response)  # Delay before response

    def show_bot_response(self):
        bot_response = self.get_response(self.last_user_message)
        self.add_message(bot_response, "Bot")

#Testing the gui with a simple bot
    def get_response(self, message):
        responses = {
            "hii": "Hi there!",
            "how are you": "I'm just a bot,i dont have feelings to response to such questions!",
            "bye": "Goodbye! Have a nice day!",
            "have a nice day": "thankss,you too"
        }
        return responses.get(message.lower(), "Hey, say something understandable!.")

app = QApplication(sys.argv)
app.setStyleSheet("""
    QLineEdit { background-color: white; padding: 5px; border-radius: 5px; }
    QPushButton { font-size: 16px; padding: 5px; border-radius: 5px; }
""")

widget = QtWidgets.QStackedWidget()
widget.setWindowIcon(QIcon("Tighba_gui/photo_2025-03-27_15-33-18-removebg-preview.png"))
widget.resize(350, 320)  
widget.setWindowTitle(" Quamus ")


login=Login()
regist=Regist()
main_chat=ModernChatbot()
widget.addWidget(login)
widget.addWidget(regist)
widget.addWidget(main_chat)

widget.setStyleSheet("background-color:#4F949D ")
widget.setCurrentIndex(0)
widget.show()

sys.exit(app.exec())

