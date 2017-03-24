from model import Section

led_count = 60

jenkins_url = "https://jenkins.example.com"
jenkins_username = "jenkins_user"
jenkins_password = "top_secret"

sections = [
    Section("development", 0, 9, ["dev", "dev-test"]),
    Section("sonar", 10, 19, ["sonar"]),
    Section("regression-tests", 20, 29, ["regression-test"])
]

color_mapping = {None: [0, 0, 255],
                 'ABORTED': [255, 0, 255],
                 'SUCCESS': [0, 255, 0],
                 'UNSTABLE': [255, 255, 0],
                 'FAILURE': [255, 0, 0]}
