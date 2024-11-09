from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.clock import Clock
from math import sin, cos
import random


class Dashboard(BoxLayout):
    def __init__(self, **kwargs):
        super(Dashboard, self).__init__(**kwargs)
        self.orientation = "vertical"

        # Upper half of the screen
        upper_half = BoxLayout(orientation="vertical", size_hint=(1, 0.5))

        # Slider and position label
        slider_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
        self.slider = Slider(min=-100, max=100, value=0)
        self.position_label = Label(text="Position: 0")
        self.slider.bind(value=self.update_position)
        slider_layout.add_widget(self.slider)
        slider_layout.add_widget(self.position_label)
        upper_half.add_widget(slider_layout)

        # Numerical dashboard items
        numbers_layout = GridLayout(cols=3, size_hint=(1, 0.8))

        self.Kp = Label(text="Kp")
        self.Ki = Label(text="Ki")
        self.Kd = Label(text="Kd")

        self.Kp2 = Label(text="Kp2")
        self.Ki2 = Label(text="Ki2")
        self.Kd2 = Label(text="Kd2")

        numbers_layout.add_widget(self.Kp)
        numbers_layout.add_widget(self.Ki)
        numbers_layout.add_widget(self.Kd)
        numbers_layout.add_widget(self.Kp2)
        numbers_layout.add_widget(self.Ki2)
        numbers_layout.add_widget(self.Kd2)
        upper_half.add_widget(numbers_layout)

        self.add_widget(upper_half)

        # Lower half of the screen (chart)
        self.graph = Graph(
            xlabel="Time",
            ylabel="Speed",
            x_ticks_minor=5,
            x_ticks_major=25,
            y_ticks_major=1,
            y_grid_label=True,
            x_grid_label=True,
            padding=5,
            x_grid=True,
            y_grid=True,
            xmin=0,
            xmax=100,
            ymin=-100,
            ymax=100,
        )

        # Create the second Y-axis
        self.graph.add_y_axis(ymin=0, ymax=100)

        self.plot1 = MeshLinePlot(color=[1, 0, 0, 1])
        self.plot1.points = [(x, sin(x/4)*10) for x in range(0, 101)]
        self.graph.add_plot(self.plot1)

        self.plot2 = MeshLinePlot(color=[0, 1, 0, 1])
        self.plot2.points = [(x, cos(x/4)*20) for x in range(0, 101)]
        self.graph.add_plot(self.plot2)

        self.add_widget(self.graph)

        # Start updating values
        Clock.schedule_interval(self.update_values, 1)

    def update_position(self, instance, value):
        self.position_label.text = f"Position: {int(value)}"

    def update_values(self, dt):
        value = round(random.uniform(0, 100), 2)
        self.Kp = f"Kp: {value:.2f}"

        # Update chart
        # x_values = range(101)
        # y_values = [random.uniform(0, 5) for _ in x_values]
        # self.plot1.points = [(x, y) for x, y in zip(x_values, y_values)]


class DashboardApp(App):
    def build(self):
        return Dashboard()


if __name__ == "__main__":
    DashboardApp().run()
