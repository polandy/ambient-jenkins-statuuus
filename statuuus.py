import config
import jenkins

for section in config.sections:
    print(section.name)


server = jenkins.Jenkins(config.jenkins_url, username=config.jenkins_username, password=config.jenkins_password)


def get_last_build_number(project_name):
    return server.get_job_info(project_name)['lastBuild']['number']


def get_build_status(project_name):
    build_number = get_last_build_number(project_name)
    return server.get_build_info(project_name, build_number)['result']


def status_to_numbers(argument):
    switcher = {
        "FAILED" : -1,
        "UNSTABLE" : 0,
        "SUCCESS": 1,
    }
    return switcher.get(argument, -1)


def get_section_state_dict():
    global section
    section_state = dict()
    for section in config.sections:
        for project_name in section.project_names:
            try:
                build_status = get_build_status(project_name)
                if section in section_state:
                    section_state[section] = build_status if status_to_numbers(build_status) <  status_to_numbers(section_state[section]) else section_state[section]
                else:
                    section_state[section] = build_status
            except jenkins.NotFoundException:
                print 'WARNING: configured project "%s" for section "%s" not found' % (project_name, section.name)
    return section_state