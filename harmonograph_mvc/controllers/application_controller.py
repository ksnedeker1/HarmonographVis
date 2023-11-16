from harmonograph_mvc.models.harmonograph import Harmonograph, HarmonographParams
from harmonograph_mvc.models.renderer import ImageBlender
from harmonograph_mvc.utils.timing import timed


class ApplicationController:
    def __init__(self, min_alpha: int = 0, steps: int = 10):
        self.min_alpha = min_alpha
        self.steps = steps
        self.images = {}
        self.invalid_param_widgets = []
        self.params = None
        self.harmonograph = None
        self.blender = None
        self.start_time = None
        self.display_mode = 0
        self.dim = 2
        self.pendulums = 2

    def get_param_values(self, param_widgets, t_param_widgets):
        params = []
        t_params = []
        self.invalid_param_widgets = []

        for input_widget in param_widgets:
            value = input_widget.get_value()

            if value is None:
                self.invalid_param_widgets.append(input_widget)
            else:
                params.append(value)

        for input_widget in t_param_widgets:
            value = input_widget.get_value()

            if value is None:
                self.invalid_param_widgets.append(input_widget)
            else:
                t_params.append(value)

        pendulum_params = []
        for pendulum in range(self.pendulums):
            pendulum_axes_params = []
            for axis in range(self.dim):
                axis_params = tuple(params[i] for i in range(pendulum + axis * self.pendulums, len(params),
                                                             self.dim * self.pendulums))
                pendulum_axes_params.append(axis_params)
            pendulum_params.append(tuple(pendulum_axes_params))
        return pendulum_params, t_params

    def set_harmonograph_params(self, param_values):
        print("PARAMS:", param_values[0], *param_values[1])
        self.params = HarmonographParams(param_values[0], *param_values[1])

    def switch_display_mode(self):
        self.display_mode = (self.display_mode + 1) % 4

    @timed
    def generate_image(self, width, height, show_pendulum_paths, min_alpha, alpha_steps):
        self.blender = ImageBlender(width - 50, height - 50, min_alpha, alpha_steps)
        self.harmonograph = Harmonograph(self.params)
        self.blender.reset()

        if show_pendulum_paths:
            pendulum_coords = self.harmonograph.get_pendulum_coords(min(self.blender.width, self.blender.height) - 1)

            self.images = {}
            self.images['full'] = self.blender.blend(
                *self.harmonograph.get_coords(min(self.blender.width, self.blender.height) - 1))

            for i, coords in enumerate(pendulum_coords, start=1):
                self.blender.reset()
                image = self.blender.blend(*coords)
                self.images[f'pendulum_{i}'] = image

        else:
            x, y = self.harmonograph.get_coords(min(self.blender.width, self.blender.height) - 1)
            image = self.blender.blend(x, y)

            self.images = {'full': image}

    def get_images(self):
        return self.images

    def get_invalid_param_widgets(self):
        return self.invalid_param_widgets
