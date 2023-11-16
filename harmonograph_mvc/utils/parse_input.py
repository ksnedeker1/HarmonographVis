import numpy as np
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QValidator
import re


ALLOWED_KEYWORDS = {'pi': 'np.pi',                      # Pi
                    'e': 'np.e',                        # Euler's number
                    'gr': '((1 + 5 ** 0.5) / 2)',       # Golden ratio
                    }


class ExpressionValidator(QValidator):
    def validate(self, string, pos):
        # Allow empty field
        if not string:
            return QValidator.Acceptable, string, pos

        # Allow backspace at any point
        if pos < len(string):
            return QValidator.Acceptable, string, pos

        last_word = re.split('[-+*/.()\s ]', string)[-1]

        # Scenario 1: last char is arithmetic symbol, space, number or parentheses
        if re.match('^[0-9+\-*/.()\s]*$', string[-1]) is not None:
            return QValidator.Acceptable, string, pos

        # Scenario 2: last char is a letter which matches first char of any keyword
        elif len(last_word) == 1 and any(keyword.startswith(last_word) for keyword in ALLOWED_KEYWORDS):
            return QValidator.Acceptable, string, pos

        # Scenario 3: last char is expected to continue at least one keyword
        elif len(last_word) > 1 and any(keyword.startswith(last_word) for keyword in ALLOWED_KEYWORDS):
            return QValidator.Acceptable, string, pos

        # If none of the scenarios match, the input is invalid
        else:
            return QValidator.Invalid, string, pos


class ParseParamInput(QLineEdit):
    def __init__(self, init_value, parent=None):
        super().__init__(parent)
        self.setValidator(ExpressionValidator())
        self.setText(str(init_value))

    def get_value(self):
        out = self.text()
        for identifier in ALLOWED_KEYWORDS.keys():
            out = out.replace(identifier, ALLOWED_KEYWORDS[identifier])
        try:
            return float(eval(out))
        except Exception:
            return None
