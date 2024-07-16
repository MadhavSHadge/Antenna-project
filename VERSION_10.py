import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QGroupBox, QGridLayout, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
import serial
import datetime
import time

# Define the file path for saving motor settings
file_path = 'motor_settings.txt'

class ArduinoMotorControl(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initSerial()

    def initUI(self):
        self.setWindowTitle('Arduino Motor Control')
        self.setGeometry(100, 100, 800, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QGridLayout()  # Using QGridLayout for more control
        central_widget.setLayout(main_layout)

        # Motor controls
        motor_controls_group = QGroupBox('Speed Controls')
        motor_controls_layout = QVBoxLayout()
        motor_controls_group.setLayout(motor_controls_layout)

        self.speed_label = QLabel('Calculated Speed (PWM 0-255):')
        motor_controls_layout.addWidget(self.speed_label)

        self.calculated_speed_display = QLabel('N/A')
        motor_controls_layout.addWidget(self.calculated_speed_display)

        speed_button_layout = QHBoxLayout()
        motor_controls_layout.addLayout(speed_button_layout)

        self.stop_button = QPushButton('Stop Motor')
        self.stop_button.clicked.connect(self.stop_motor)
        speed_button_layout.addWidget(self.stop_button)

        main_layout.addWidget(motor_controls_group, 0, 0, 2, 1)  # (row, column, rowspan, colspan)

        # Direction controls
        direction_group = QGroupBox('Direction Controls')
        direction_layout = QHBoxLayout()
        direction_group.setLayout(direction_layout)

        self.forward_button = QPushButton('Clockwise')
        self.forward_button.clicked.connect(self.forward)
        direction_layout.addWidget(self.forward_button)

        self.backward_button = QPushButton('Anticlockwise')
        self.backward_button.clicked.connect(self.backward)
        direction_layout.addWidget(self.backward_button)

        self.direction_button = QPushButton('Direction Find')
        self.direction_button.clicked.connect(self.direction_count)
        direction_layout.addWidget(self.direction_button)

        main_layout.addWidget(direction_group, 0, 1)

        # Encoder value display
        encoder_group = QGroupBox('Encoder Value')
        encoder_layout = QVBoxLayout()
        encoder_group.setLayout(encoder_layout)

        self.encoder_value_label = QLabel('Current Encoder Value: N/A')
        encoder_layout.addWidget(self.encoder_value_label)

        self.read_encoder_button = QPushButton('Read Encoder Value')
        self.read_encoder_button.clicked.connect(self.read_encoder)
        encoder_layout.addWidget(self.read_encoder_button)

        main_layout.addWidget(encoder_group, 1, 1)

        # Pulse count and angle setting
        pulse_group = QGroupBox('Set Antenna Angle')
        pulse_layout = QGridLayout()
        pulse_group.setLayout(pulse_layout)

        pulse_label = QLabel('Enter Angle In Degrees:')
        pulse_layout.addWidget(pulse_label, 0, 0)

        self.pulse_entry = QLineEdit()
        pulse_layout.addWidget(self.pulse_entry, 0, 1)

        self.write_pulse_button = QPushButton('Set Angle')
        self.write_pulse_button.clicked.connect(self.write_encoder)
        pulse_layout.addWidget(self.write_pulse_button, 0, 2)

        self.angle_value_label = QLabel('Current Angle Value: N/A')
        pulse_layout.addWidget(self.angle_value_label, 1, 0, 1, 2)

        self.read_angle_button = QPushButton('Read Angle Value')
        self.read_angle_button.clicked.connect(self.read_encoder_angle)
        pulse_layout.addWidget(self.read_angle_button, 1, 2)

        main_layout.addWidget(pulse_group, 2, 0, 1, 2)

        # Timer controls
        timer_group = QGroupBox('Set Clock For Rotation')
        timer_layout = QGridLayout()
        timer_group.setLayout(timer_layout)

        self.hours_entry = QLineEdit('00')
        timer_layout.addWidget(self.hours_entry, 0, 0)

        self.minutes_entry = QLineEdit('00')
        timer_layout.addWidget(self.minutes_entry, 0, 1)

        self.seconds_entry = QLineEdit('00')
        timer_layout.addWidget(self.seconds_entry, 0, 2)

        start_stop_layout = QHBoxLayout()
        timer_layout.addLayout(start_stop_layout, 1, 0, 1, 3)

        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_timer)
        start_stop_layout.addWidget(self.start_button)

        self.stop_button_timer = QPushButton('Stop')
        self.stop_button_timer.clicked.connect(self.stop_timer)
        start_stop_layout.addWidget(self.stop_button_timer)

        main_layout.addWidget(timer_group, 3, 0, 1, 2)

        # Reset Button
        self.reset_button = QPushButton('Reset')
        self.reset_button.clicked.connect(self.reset_all)
        main_layout.addWidget(self.reset_button, 4, 0, 1, 2)

        # Initialize settings from file
        self.read_motor_settings()

    def initSerial(self):
        self.serial_port = '/dev/ttyUSB1'  # Adjust the port as necessary
        self.baud_rate = 9600
        self.ser = serial.Serial(self.serial_port, self.baud_rate)
        time.sleep(2)  # Allow some time for the serial connection to establish

    def read_motor_settings(self):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()
                if len(lines) >= 2:
                    self.pulse_entry.setText(lines[1].strip())

    def write_motor_settings(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(file_path, 'a') as file:
            file.write("\n")
            file.write("<----------------------------------------------------> \n")
            file.write(f"Date and Time: {current_time}\n\n")
            file.write(f"The Angle of the Antenna is: {self.pulse_entry.text()} \n")
            file.write("<----------------------------------------------------> \n\n")

    def send_command(self, command):
        self.ser.write(command.encode('utf-8'))

    def forward(self):
        self.send_command('F')

    def backward(self):
        self.send_command('B')

    def stop_motor(self):
        self.send_command('S')

    def direction_count(self):
        self.send_command('D')

    def read_encoder(self):
        self.send_command('E')
        encoder_value = self.ser.readline().decode().strip()
        self.encoder_value_label.setText(f"Current Encoder Value: {encoder_value}")

    def read_encoder_angle(self):
        self.send_command('A')
        angle_value = self.ser.readline().decode().strip()
        self.angle_value_label.setText(f"Current Angle Value: {angle_value}")

    def write_encoder(self):
        try:
            pulses = int(self.pulse_entry.text())
            self.ser.write(f'P{pulses}'.encode())
            self.write_motor_settings()
            QMessageBox.information(self, "Pulse Count Set", f"Motor will run for {pulses} pulses")
        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter valid integer values for pulse count")

    def start_timer(self):
        try:
            total_time = int(self.hours_entry.text()) * 3600 + int(self.minutes_entry.text()) * 60 + int(self.seconds_entry.text())
        except ValueError:
            QMessageBox.critical(self, "Invalid Input", "Please enter valid integers for hours, minutes, and seconds.")
            return

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

        # Calculate PWM based on the given time
        rpm = 10  # Motor's RPM
        rotations_per_second = rpm / 60
        pulses_per_rotation = 360  # Example value, should be set according to the motor's encoder
        required_pulses = rotations_per_second * total_time

        # Convert pulses to PWM (0-255)
        pwm_value = min(max(int((required_pulses / pulses_per_rotation) * 255), 0), 255)
        self.calculated_speed_display.setText(str(pwm_value))
        self.ser.write(str(pwm_value).encode())

    def stop_timer(self):
        if hasattr(self, 'timer'):
            self.timer.stop()
        self.stop_motor()

    @pyqtSlot()
    def update_timer(self):
        total_time = int(self.hours_entry.text()) * 3600 + int(self.minutes_entry.text()) * 60 + int(self.seconds_entry.text())
        total_time -= 1

        hours = total_time // 3600
        minutes = (total_time % 3600) // 60
        seconds = total_time % 60

        self.hours_entry.setText(f"{hours:02d}")
        self.minutes_entry.setText(f"{minutes:02d}")
        self.seconds_entry.setText(f"{seconds:02d}")

        if total_time == 0:
            self.stop_timer()
            QMessageBox.information(self, "Time's Up", "The timer has ended!")
            self.stop_motor()
            QMessageBox.information(self, "Rotation Complete", "The antenna has reached the maximum level.")

    def reset_all(self):
        self.pulse_entry.setText('0')
        self.hours_entry.setText('00')
        self.minutes_entry.setText('00')
        self.seconds_entry.setText('00')
        self.encoder_value_label.setText('Current Encoder Value: N/A')
        self.angle_value_label.setText('Current Angle Value: N/A')
        self.calculated_speed_display.setText('N/A')

        self.send_command('R')  # Assuming 'R' command resets the motor to initial position
        self.read_encoder()  # Update the encoder value to reflect the reset

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ArduinoMotorControl()
    window.show()
    sys.exit(app.exec_())
