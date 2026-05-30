from model import GeminiModel
from view import MainWindow

class AppController:
    def __init__(self):
        self.model = GeminiModel()
        self.view = MainWindow(self)
    
    def run(self):
        self.view.run()