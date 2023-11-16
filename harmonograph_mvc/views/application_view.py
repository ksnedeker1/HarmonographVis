from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QPushButton, QLabel, QWidget, \
    QDesktopWidget, QHBoxLayout, QCheckBox, QGridLayout, QSpacerItem, QSizePolicy, QLineEdit, QComboBox, QStackedWidget

from harmonograph_mvc.utils.parse_input import ParseParamInput
from harmonograph_mvc.controllers.application_controller import ApplicationController


class ApplicationView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.controller = ApplicationController()

        self.default_min_alpha = 25
        self.default_alpha_steps = 45

        self.images = {}

        self.setup_window()
        self.setup_layout()
        self.setup_controls()
        self.setup_pendulum_parameters_page()
        self.setup_alpha_blending_page()
        self.setup_status()

    def setup_window(self):
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(screen)

        self.screen_width = int(screen.width() * 0.85)
        self.screen_height = int(screen.height() * 0.85)

        if self.screen_width / 16 * 9 > self.screen_height:
            self.screen_width = int(self.screen_height / 9 * 16)
        else:
            self.screen_height = int(self.screen_width / 16 * 9)

        self.setGeometry(0, 0, self.screen_width, self.screen_height)

    def setup_layout(self):
        self.widget = QWidget(self)
        self.layout = QHBoxLayout(self.widget)

        self.image_width = self.screen_height - 40
        self.image_height = self.screen_height - 40

        self.setStyleSheet("background-color: darkgray;")

    def setup_status(self):
        self.status_label = QLabel(self.controls)
        self.controls_layout.addWidget(self.status_label, alignment=Qt.AlignBottom)

    def setup_controls(self):
        self.controls = QWidget(self)
        self.controls.setFixedWidth(self.screen_width - self.image_width)
        self.controls_layout = QVBoxLayout(self.controls)

        self.generate_button = QPushButton('Generate', self.controls)
        self.generate_button.clicked.connect(self.start_image_generation)
        self.controls_layout.addWidget(self.generate_button)

        self.image_order = ['full', 'pendulum_1', 'pendulum_2']
        self.current_image_index = 0

        self.show_pendulum_paths = QCheckBox('Show Pendulum Paths', self)
        self.display_mode = 0
        self.display_mode_btn = QPushButton('Switch Display Mode', self)
        self.display_mode_btn.clicked.connect(self.switch_image)

        checkbox_layout = QHBoxLayout()
        checkbox_layout.addWidget(self.show_pendulum_paths)
        checkbox_layout.addWidget(self.display_mode_btn)
        self.controls_layout.addLayout(checkbox_layout)

        spacer = QSpacerItem(0, 1000000, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.controls_layout.addItem(spacer)

        self.settings_combo_box = QComboBox()
        self.settings_combo_box.addItem("Pendulum Parameters")
        self.settings_combo_box.addItem("Alpha Blending")
        self.settings_combo_box.currentIndexChanged.connect(self.switch_setting)
        self.controls_layout.addWidget(self.settings_combo_box)

        self.stack = QStackedWidget(self.controls)
        self.controls_layout.addWidget(self.stack)

        self.layout.addWidget(self.controls)

        self.view = QGraphicsView(self)
        self.layout.addWidget(self.view)

        self.setCentralWidget(self.widget)

    def setup_pendulum_parameters_page(self):
        self.pendulum_page = QWidget()
        self.setup_params(self.pendulum_page)  # Passing the page as the parent widget
        self.stack.addWidget(self.pendulum_page)

    def setup_alpha_blending_page(self):
        self.alpha_page = QWidget()
        self.alpha_layout = QHBoxLayout(self.alpha_page)  # Change to QHBoxLayout

        # Set up 'Min Alpha' parameter
        self.min_alpha_label = QLabel('Min Alpha:')
        self.min_alpha_input = QLineEdit(str(self.default_min_alpha))
        self.min_alpha_layout = QHBoxLayout()
        self.min_alpha_layout.addWidget(self.min_alpha_label)
        self.min_alpha_layout.addWidget(self.min_alpha_input)

        # Set up 'Alpha Steps' parameter
        self.steps_label = QLabel('Alpha Steps:')
        self.steps_input = QLineEdit(str(self.default_alpha_steps))
        self.steps_layout = QHBoxLayout()
        self.steps_layout.addWidget(self.steps_label)
        self.steps_layout.addWidget(self.steps_input)

        self.alpha_layout.addLayout(self.min_alpha_layout)
        self.alpha_layout.addLayout(self.steps_layout)

        self.stack.addWidget(self.alpha_page)

    def setup_params(self, parent_widget):
        self.param_inputs = []
        self.t_inputs = []
        self.params_grid = QGridLayout()
        param_names = ['Amplitude', 'Dampening', 'Frequency', 'Phase']
        default_values = [1.0, 0.0005, 1.0, 0.0]

        column_labels = ['Pendulum 1 (x)', 'Pendulum 2 (x)', 'Pendulum 1 (y)', 'Pendulum 2 (y)']
        for i, label in enumerate(column_labels):
            label_widget = QLabel(label, parent_widget)
            label_widget.setAlignment(Qt.AlignCenter)
            label_widget.setFixedHeight(15)
            self.params_grid.addWidget(label_widget, 0, i + 2)

        for i, param_name in enumerate(param_names):
            row_label = QLabel(param_name, parent_widget)
            row_label.setAlignment(Qt.AlignCenter)
            self.params_grid.addWidget(row_label, i + 1, 0)
            for j in range(4):
                param_input = ParseParamInput(parent_widget)  # Create ParseParamInput instance
                param_input.setText(str(default_values[i]))
                param_input.setAlignment(Qt.AlignCenter)
                self.params_grid.addWidget(param_input, i + 1, j + 2)
                self.param_inputs.append(param_input)

        t_params_layout = QHBoxLayout()
        t_params_names = ['Start Time', 'End Time', 'Samples']
        t_default_values = [0, 2000, 200000]  # Replace with your actual default values
        for i, t_param_name in enumerate(t_params_names):
            t_label = QLabel(t_param_name, parent_widget)
            t_label.setAlignment(Qt.AlignCenter)
            t_params_layout.addWidget(t_label)
            t_input = ParseParamInput(str(t_default_values[i]), parent_widget)
            t_input.setAlignment(Qt.AlignCenter)
            t_params_layout.addWidget(t_input)
            self.t_inputs.append(t_input)

        parent_layout = QVBoxLayout(parent_widget)
        parent_layout.addLayout(self.params_grid)
        parent_layout.addLayout(t_params_layout)

    def switch_setting(self):
        index = self.settings_combo_box.currentIndex()
        self.stack.setCurrentIndex(index)

    def hide_layout_widgets(self, layout):
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if widget is not None:  # check if the item is a widget
                widget.hide()

    def show_layout_widgets(self, layout):
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if widget is not None:  # check if the item is a widget
                widget.show()

    def update_status(self, status):
        self.status_label.setText(status)

    def start_image_generation(self):
        self.reset_invalid_widget_highlighting()

        self.update_status("Generating...")

        # This will start the actual image generation after a very short delay, giving the GUI time to update
        QTimer.singleShot(100, self.call_generate_image)

    def call_generate_image(self):
        # Extract the parameters from the UI
        param_values = self.controller.get_param_values(self.param_inputs, self.t_inputs)

        invalid_params_exist = self.set_invalid_widget_highlighting()

        if invalid_params_exist:
            return

        # Pass the parameters to the controller
        self.controller.set_harmonograph_params(param_values)

        # Trigger image generation
        elapsed_time = self.controller.generate_image(self.image_width, self.image_height,
                                                      self.show_pendulum_paths.isChecked(),
                                                      int(self.min_alpha_input.text()),
                                                      int(self.steps_input.text()))

        # After image is generated, get the images from the controller
        self.images = self.controller.get_images()

        # Then update the UI
        self.display_image('full')

        self.update_status(f"Image generation completed in {elapsed_time:.2f} seconds.")

    def display_image(self, name):
        """Displays the image with the given name."""
        image = self.images.get(name)

        if image is not None:
            scene = QGraphicsScene()
            scene.addPixmap(QPixmap.fromImage(image))
            self.view.setScene(scene)
        else:
            self.update_status(f"Image '{name}' not found.")

    def switch_image(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.image_order)
        self.display_image(self.image_order[self.current_image_index])
        self.update_status(f"Displaying {self.image_order[self.current_image_index]} image.")

    def set_invalid_widget_highlighting(self):
        invalid_param_widgets = self.controller.get_invalid_param_widgets()

        if invalid_param_widgets:
            for widget in invalid_param_widgets:
                widget.setStyleSheet("border: 1px solid red;")
            self.update_status("Invalid input. Please correct highlighted fields.")
            return True

        return False

    def reset_invalid_widget_highlighting(self):
        for widget in self.controller.get_invalid_param_widgets():
            widget.setStyleSheet("")
