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

color_mapping = {None: Led([0, 0, 255], None),
                 'ABORTED': Led([255, 0, 255], None),
                 'SUCCESS': Led([0, 255, 0], None),
                 'UNSTABLE': Led([255, 255, 0], None),
                 'FAILURE': Led([255, 0, 0], None),
                 'ABORTED_building': Led([255, 0, 255], [0, 0, 255]),
                 'SUCCESS_building': Led([0, 255, 0], [0, 0, 255]),
                 'UNSTABLE_building': Led([255, 255, 0], [0, 0, 255]),
                 'FAILURE_building': Led([255, 0, 0], [0, 0, 255])
                 }
