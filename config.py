from datetime import time
from model import Section
from model import Led
from model import Job

led_count = 60
request_interval = 60

startup_time = time(hour=07, minute=30)
shutdown_time = time(hour=18, minute=30)

jenkins_url = "https://jenkins.example.com"
jenkins_username = "jenkins_user"
jenkins_password = "top_secret"

sections = [
    Section("development", 0, 9, [Job("dev", True), Job("dev-test")]),
    Section("sonar", 10, 19, [Job("sonar")]),
    Section("regression-tests", 20, 29, [Job("regression-test")])
]

blue = [0, 0, 255]
red = [255, 0, 0]
orange = [255, 92, 0]
green = [0, 255, 0]
pink = [255, 0, 255]

color_mapping = {None: Led(blue),
                 'ABORTED': Led(pink),
                 'SUCCESS': Led(green),
                 'UNSTABLE': Led(orange),
                 'FAILURE': Led(red),
                 'ABORTED_building': Led(pink, blue),
                 'SUCCESS_building': Led(green, blue),
                 'UNSTABLE_building': Led(orange, blue),
                 'FAILURE_building': Led(red, blue)
                 }