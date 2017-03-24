import config
import jenkins

for section in config.sections:
    print(section.name)


server = jenkins.Jenkins(config.jenkins_url, username=config.jenkins_username, password=config.jenkins_password)


def get_last_build_number(project_name):
    project_last_build_number = dict()
    for project in server.get_job_info_regex(project_name):
        if project['lastBuild'] is not None:
            project_last_build_number[project['displayName']] = project['lastBuild']['number']
    return project_last_build_number


def get_build_status(project_name):
    build_numbers = get_last_build_number(project_name)
    build_results = []
    for project_name, build_number in build_numbers.iteritems():
        build_results.append(server.get_build_info(project_name, build_number)['result'])
    return build_results


def status_to_numbers(argument):
    switcher = {
        "FAILED" : -1,
        "UNSTABLE": 0,
        "SUCCESS": 1,
    }
    return switcher.get(argument, -1)


def get_section_state_dict():
    global section
    section_state = dict()
    for section in config.sections:
        for project_name in section.project_names:
            try:
                build_states = get_build_status(project_name)
                for state in build_states:
                    if section in section_state:
                        section_state[section] = state if status_to_numbers(state) < status_to_numbers(section_state[section]) else section_state[section]
                    else:
                        section_state[section] = state
            except jenkins.NotFoundException:
                print 'WARNING: configured project "%s" for section "%s" not found' % (project_name, section.name)
    return section_state

get_section_state_dict()