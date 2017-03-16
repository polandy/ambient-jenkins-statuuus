from model import Section

jenkins_url = "https://jenkins.example.com"
jenkins_username = "jenkins_user"
jenkins_password = "top_secret"

sections = [
    Section("development", 0, 9, ["dev", "dev-test"]),
    Section("sonar", 10, 19, ["sonar"]),
    Section("regression-tests", 20, 29, ["regression-test"])
]

color_mapping = {'ok': [0, 255, 0],
                 'warning': [255, 255, 0],
                 'error': [255, 0, 0]}
