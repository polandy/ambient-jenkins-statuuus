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
    Section("feature branches", 0, led_count/3-1, ["feature_branch_"]),
    Section("main branches", led_count/3, led_count/3*2-1, ["development", "release_", "master"]),
    Section("misc", led_count/3*2, led_count-1, ["regression_tests", "sonar_build"])
]

# The constructor of Led takes two arguments: a primary and a secondary color as RGB-codes.
# When a build is in progress the color is switching between the primary and secondary colors.
# You only need to change the RGB-Codes. 
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
```

## Run
```
python app.py
```
