from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QLineEdit, QGridLayout, QHBoxLayout, QVBoxLayout
)
from PyQt6 import QtWidgets
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap

class Login(QWidget):
    def __init__(self):
        super().__init__() 
       
        layout = QVBoxLayout()
        self.setLayout(layout)
       
        # Logo/Image
        label = QLabel(self)
        pixmap = QPixmap("/home/teeba/Documents/cppDS/photo_2025-03-27_15-33-18-removebg-preview.png") 
      
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

    def goToRegist(self):
        self.parent().setCurrentIndex(1)  # Switch to registration window
        
        
class Regist(QWidget):
    def __init__(self):
        super().__init__()
        
       
        self.setWindowIcon(QIcon("/home/teeba/Documents/cppDS/photo_2025-03-27_15-33-18-removebg-preview.png"))  
        
        layoutR=QVBoxLayout()
        self.setLayout(layoutR)
        label = QLabel(self)
        pixmap = QPixmap("/home/teeba/Documents/cppDS/photo_2025-03-27_15-33-18-removebg-preview.png") 
      
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
        font-size: 20px;
                              
                              
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
        
        
        

        
        
        
        
        
        
app = QApplication(sys.argv)
app.setStyleSheet("""
    QLineEdit { background-color: white; padding: 5px; border-radius: 5px; }
    QPushButton { font-size: 16px; padding: 5px; border-radius: 5px; }
""")

widget = QtWidgets.QStackedWidget()
widget.setWindowIcon(QIcon("/home/teeba/Documents/cppDS/photo_2025-03-27_15-33-18-removebg-preview.png"))
widget.resize(350, 320)  
widget.setWindowTitle(" Quamus ")
mainWindow = Login()
RegistWindow = Regist()

widget.addWidget(mainWindow)
widget.addWidget(RegistWindow)
widget.setStyleSheet("background-color:#4F949D ")
widget.setCurrentIndex(0)  # Start with Login screen
widget.show()

sys.exit(app.exec())
