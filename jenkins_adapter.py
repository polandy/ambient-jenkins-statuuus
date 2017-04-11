import config
import jenkins
import traceback
from datetime import datetime

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
        build_info = server.get_build_info(project_name, build_number)
        if build_info['building'] and build_number > 0:
            build_info = server.get_build_info(project_name, build_number-1)
            build_results.append(build_info['result'] + '_building')
        build_results.append(build_info['result'])
    return build_results


def status_to_numbers(argument):
    switcher = {
        "FAILED_building" : -4,
        "FAILED" : -3,
        "UNSTABLE_building": -2,
        "UNSTABLE": -1,
        "SUCCESS_building": 0,
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
            except jenkins.JenkinsException:
                print '\t ----------------WARNING: error occured (JenkinsException):---------------------- '
                print 'INFO: datetime: %s' % (str(datetime.date()))
                print traceback.print_exc()
                print '\t --------------------------------------------------------------------------------- '
    return section_state

# get_section_state_dict()