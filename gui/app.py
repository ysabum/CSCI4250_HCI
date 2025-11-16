import sys
import os
# This catches the file location for importing functions from the other python folders in the project
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QMessageBox
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import Qt, QUrl

#Layout on importing functions for use
from cv2_Python_Files.cv2_Working_Example import run_camera

class MainMenu(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout()

        #Title
        title = QLabel("--- CSCI4250 HCI Camera Tracking Application ---")
        title.setObjectName("title")
        layout.addWidget(title)

        #Start Button
        start_button = QPushButton("Start")
        start_button.setObjectName('start_button')
        start_button.setToolTip("Click to start the screen reader")
        start_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(start_button)

        #About Button will link to GitHub Repo
        about_button = QPushButton("About")
        about_button.setObjectName('about_button')
        about_button.setToolTip("Click to open the GitHub repository for this project")
        about_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/ysabum/CSCI4250_HCI/tree/main")))
        layout.addWidget(about_button)

        #Exit will close the application
        exit_button = QPushButton("Exit")
        exit_button.setObjectName('exit_button')
        exit_button.setToolTip("Click to close the app")
        # exit_button.clicked.connect(QApplication.quit)
        exit_button.clicked.connect(self.force_quit)        
        layout.addWidget(exit_button)

        layout.addStretch()

        self.setLayout(layout)

    def force_quit(self):
        """Forcefully closes the application and all associated windows.

        This method attempts to close any OpenCV windows and then terminates the application process.
        """
        try:
            cv2.destroyAllWindows()
        except:
            pass
        QApplication.instance().quit()
        os._exit(0)

class StartScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Choose a screen and enable the webcam?")
        title.setObjectName("title")
        layout.addWidget(title)

        # Confirmation Button to launch program
        confirm_button = QPushButton("Yes")
        confirm_button.clicked.connect(self.enable_webcam)
        layout.addWidget(confirm_button)

        # Back button to navigate back to the main menu
        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_button)

        layout.addStretch()
        self.setLayout(layout)

    def enable_webcam(self):
        # Placeholder for actual function to choose a screen and enable webcam.
        # Imported a run_camera() function in cv2_Working_Example.py as a placeholder.
        run_camera()

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt App Shell")
        layout = QVBoxLayout()

        self.stacked_widget = QStackedWidget()

        # Add Main Menu Index
        self.main_menu = MainMenu(self.stacked_widget)
        self.stacked_widget.addWidget(self.main_menu)

        # Add Start Screen Index
        self.start_screen = StartScreen(self.stacked_widget)
        self.stacked_widget.addWidget(self.start_screen)

        # Sets current Index
        self.stacked_widget.setCurrentIndex(0)

        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

def main():
    # Main Script to run the Application
    app = QApplication(sys.argv)

    # Style Sheet Import!
    with open(os.path.join(os.path.dirname(__file__), "styles.qss"), "r") as f:
        app.setStyleSheet(f.read())

    window = App()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
