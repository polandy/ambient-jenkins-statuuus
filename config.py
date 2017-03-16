from model import Section

sections = [
    Section("development", 0, 9, ["dev", "dev-test"]),
    Section("sonar", 10, 19, ["sonar"]),
    Section("regression-tests", 20, 29, ["regression-test"])
]

color_mapping = {'ok': [0, 255, 0],
                 'warning': [255, 255, 0],
                 'error': [255, 0, 0]}
