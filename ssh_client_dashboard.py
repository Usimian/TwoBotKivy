from math import sin, cos
import random
import time

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window

from ssh_client import ssh_client

Window.size = (720, 480)


class Dashboard(BoxLayout):
    def __init__(self, **kwargs):
        super(Dashboard, self).__init__(**kwargs)
        self.orientation = "vertical"

        self.Rp = 0.0
        self.Ri = 0.0
        self.Rd = 0.0
        self.Kp = 0.0
        self.Ki = 0.0
        self.Kd = 0.0
        self.Kp2 = 0.0
        self.Ki2 = 0.0
        self.Kd2 = 0.0

        self.Pos = 0.0  # Current position
        self.Vb = 0.0   # Battery voltage

        # Upper half of the screen
        upper_half = BoxLayout(orientation="vertical", size_hint=(1, 0.8))

        # Slider
        slider_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.2))
        self.slider = Slider(min=-500, max=500, value=0)
        self.slider.bind(value=self.update_position)

        # Position label
        self.position_label = Label(text="Position(mm): 0")
        self.position_label.value = 0

        # Current position label
        self.current_pos_label = Label(text="Position(mm): 0")
        self.current_pos_label.value = 0.0

        # Battery label
        self.battery_label = Label(text="Battery: 0.00V")
        self.battery_label.value = 0

        # Zero position button
        self.reset_pos = Button(text="Position Zero")
        self.reset_pos.bind(on_press=self.on_button_press)

        # Add all to layout
        slider_layout.add_widget(self.slider)
        slider_layout.add_widget(self.position_label)
        slider_layout.add_widget(self.current_pos_label)
        slider_layout.add_widget(self.reset_pos)
        slider_layout.add_widget(self.battery_label)
        upper_half.add_widget(slider_layout)

        # Numerical dashboard items
        numbers_layout = GridLayout(cols=3, size_hint=(1, 0.8))

        self.label_Rp = Label(text="Rp")
        self.label_Ri = Label(text="Ri")
        self.label_Rd = Label(text="Rd")
        self.label_Kp = Label(text="Kp")
        self.label_Ki = Label(text="Ki")
        self.label_Kd = Label(text="Kd")
        self.label_Kp2 = Label(text="Kp2")
        self.label_Ki2 = Label(text="Ki2")
        self.label_Kd2 = Label(text="Kd2")

        numbers_layout.add_widget(self.label_Rp)
        numbers_layout.add_widget(self.label_Ri)
        numbers_layout.add_widget(self.label_Rd)
        numbers_layout.add_widget(self.label_Kp)
        numbers_layout.add_widget(self.label_Ki)
        numbers_layout.add_widget(self.label_Kd)
        numbers_layout.add_widget(self.label_Kp2)
        numbers_layout.add_widget(self.label_Ki2)
        numbers_layout.add_widget(self.label_Kd2)
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
        self.plot1.points = [(x, sin(x / 4) * 10) for x in range(0, 101)]
        self.graph.add_plot(self.plot1)

        self.plot2 = MeshLinePlot(color=[0, 1, 0, 1])
        self.plot2.points = [(x, cos(x / 4) * 20) for x in range(0, 101)]
        self.graph.add_plot(self.plot2)

        self.add_widget(self.graph)

        # Start updating values
        Clock.schedule_interval(self.update_values, 1)

        self.client = ssh_client()  # Create ssh client return socket

    # Set position value
    def set_position_value(self, val):
        self.battery_label.text = f"Battery: {self.Vb:.2f}V"

        self.current_pos_label.value = self.Pos
        self.current_pos_label.text = f"Pos: {self.Pos:.2f}mm"

        self.position_label.value = val
        self.position_label.text = f"Move to: {int(val)}mm"
        response = str(int(self.position_label.value))
        self.client.socket.send(response.encode())  # Send position value to RP
        self.slider.value = val

    # Button pressed
    def on_button_press(self, instance):
        self.set_position_value(0)
        time.sleep(0.2)

    # Slider value changed
    def update_position(self, instance, value):
        self.set_position_value(value)
        time.sleep(0.1)

    # Receive data from host
    def update_values(self, dt):
        # Update K values
        self.Rp = self.client.json_data["Rp"]
        self.Ri = self.client.json_data["Ri"]
        self.Rd = self.client.json_data["Rd"]
        self.Vb = self.client.json_data["Vb"]
        self.Kp = self.client.json_data["Kp"]
        self.Ki = self.client.json_data["Ki"]
        self.Kd = self.client.json_data["Kd"]

        self.Kp2 = self.client.json_data["Kp2"]
        self.Ki2 = self.client.json_data["Ki2"]
        self.Kd2 = self.client.json_data["Kd2"]
        self.Pos = self.client.json_data["Pos"]

        self.label_Rp.text = f"Rp: {self.Rp:.2f}"
        self.label_Ri.text = f"Ri: {self.Ri:.2f}"
        self.label_Rd.text = f"Rd: {self.Rd:.2f}"
        if self.Vb < 10.0:
            self.battery_label.color = (1, 0, 0, 1)
        else:
            self.battery_label.color = (0, 1, 0, 1)
        self.battery_label.text = f"Battery: {self.Vb:.2f}V"
        self.label_Kp.text = f"Kp: {self.Kp:.2f}"
        self.label_Ki.text = f"Ki: {self.Ki:.2f}"
        self.label_Kd.text = f"Kd: {self.Kd:.2f}"
        self.label_Kp2.text = f"Kp2: {self.Kp2:.2f}"
        self.label_Ki2.text = f"Ki2: {self.Ki2:.2f}"
        self.label_Kd2.text = f"Kd2: {self.Kd2:.2f}"
        self.set_position_value(self.position_label.value)

        # Update chart
        x_values = range(101)
        y_values = [random.uniform(0, 5) for _ in x_values]
        self.plot1.points = [(x, y) for x, y in zip(x_values, y_values)]


class DashboardApp(App):
    def build(self):
        return Dashboard()


if __name__ == "__main__":
    DashboardApp().run()
