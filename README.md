# ambient-jenkins-statuuus
ambient-jenkins-statuuus is a little python project to show the states of jenkins builds on a [BlinkyTape](https://github.com/Blinkinlabs/BlinkyTape).

# Requirements
* Python 2.7.9
* [Python Jenkins](https://python-jenkins.readthedocs.io/en/latest/), a python wrapper for the Jenkins REST API
* [pySerial](https://pythonhosted.org/pyserial/), a module that encapsulates the access for the serial port

## Config
All the configuration happens in the file `config.py`:
```
# Example configuration
from datetime import time
from model import Section
from model import Led
from model import Job

# Number Of Leds
led_count = 60
# Request the jenkins every 2 seconds for the build states
request_interval = 2

# Define the startup / shutdown time
startup_time = time(hour=07, minute=30)
shutdown_time = time(hour=22, minute=30)

# Jenkins URL and user credentials
jenkins_url = "https://jenkins.example.com"
jenkins_username = "jenkins_username"
jenkins_password = "top_secret;"

# Define 'led sections'. A section consists in 
sections = [
    Section("development", 0, 9, [Job("dev", True), Job("dev-test")]),
    Section("sonar", 10, 19, [Job("sonar")]),
    Section("regression-tests", 20, 29, [Job("regression-test")])
]

# The constructor of Led takes two arguments: a primary and a secondary color as RGB-codes.
# When a build is in progress the color is switching between the primary and secondary colors.
# You only need to change the RGB-Codes. 
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
```

## Run
```
python app.py
```
