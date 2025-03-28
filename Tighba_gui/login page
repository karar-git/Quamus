from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QLineEdit, QGridLayout, QHBoxLayout, QVBoxLayout
)
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(350, 320)  # Adjusted for better proportions
        self.setWindowTitle(" Quamus ")
        self.setWindowIcon(QIcon("/home/teeba/Documents/cppDS/photo_2025-03-27_15-33-18-removebg-preview.png"))  # Ensure file exists!
       
       
       
        # Main Layout
        layout = QVBoxLayout()
        
        layout.setSpacing(0)  # Minimize space
        layout.setContentsMargins(10, 10, 10, 10)  # Remove unnecessary margins
        self.setLayout(layout)

        # Logo/Image
        label = QLabel(self)
        pixmap = QPixmap("/home/teeba/Documents/cppDS/photo_2025-03-27_15-33-18-removebg-preview.png")  # Ensure correct path
      
        pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Style to make it circular (if background allows)
        label.setStyleSheet("""
                QLabel {
                    border-radius: 40px; /* Half of 80px */
                    
                }
            """)
        layout.addWidget(label)

        # Grid Layout for Inputs
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)  

        # Labels & Input Fields
        label1 = QLabel("Username:")
        label1.setStyleSheet("font-size: 20px;color:#F5EEDC;")
        input1 = QLineEdit()
        input1.setStyleSheet("font-size: 16px; height: 25px;background-color:white;")  # Adjust height
        input1.setPlaceholderText("Enter your username")
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
        button_layout.setSpacing(10)  # Space between buttons

        button1 = QPushButton("Register")
        button1.setStyleSheet("""
                font-size: 16px; 
                padding: 6px;
                background-color:#b35c44; 
                color:white;
                 border-radius: 5px;
                           
                              """)

        button2 = QPushButton("Login")
        button2.setStyleSheet("""font-size: 16px; padding: 6px;  background-color:#b35c44; color:white;
                              
                              """)
        

       
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)
        button_layout.setContentsMargins(40,40,40,40)
      
        
        

        layout.addLayout(button_layout)  # Add button layout to main layout
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        container_widget = QWidget(self)
        container_widget.setLayout(layout)
        container_widget.setFixedSize(1000, 1000)
        container_widget.setStyleSheet("background-color:#4F959D ; radius:50%;")
        self.setStyleSheet("background-color:#4F959D ")
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(container_widget)
        self.setLayout(main_layout)
        
        main_layout.addWidget(container_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        
       
# Application Setup
app = QApplication(sys.argv)
app.setStyleSheet("""
    QLineEdit { background-color: white; padding: 5px; border-radius: 5px; }
    QPushButton { font-size: 16px; padding: 5px; border-radius: 5px; }
""")

window = Window()
window.show()
app.exec()
