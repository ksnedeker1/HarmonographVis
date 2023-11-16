from PyQt5.QtWidgets import QApplication
from harmonograph_mvc.views.application_view import ApplicationView

import sys
import os
import traceback
import psutil


def excepthook(type, value, tb):
    message = "".join(traceback.format_exception(type, value, tb))
    print(message)


def print_memory_usage():
    process = psutil.Process(os.getpid())
    print("Memory usage:", process.memory_info().rss * 0.000001)


sys.excepthook = excepthook

app = QApplication([])
window = ApplicationView()
window.show()
print_memory_usage()
app.exec_()
print_memory_usage()
