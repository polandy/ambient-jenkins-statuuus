import config
import jenkins
import traceback
from datetime import datetime

server = jenkins.Jenkins(config.jenkins_url, username=config.jenkins_username, password=config.jenkins_password)

states = {
    "FAILURE_building": -4,
    "FAILURE": -3,
    "UNSTABLE_building": -2,
    "UNSTABLE": -1,
    "SUCCESS_building": 0,
    "SUCCESS": 1,
}


def get_build_state(jenkins_job, job):
    last_build = jenkins_job['lastBuild']
    if last_build is not None:
        if last_build['building'] and last_build['number'] > 0:
            job.building = True
            last_completed_build = jenkins_job['lastCompletedBuild']
            if last_completed_build is not None:
                return last_completed_build['result']
        else:
            return last_build['result']


def get_build_states(job):
    build_states = []

    if job.pipeline:
        for child_job in server.get_job_info(job.name, 2)['jobs']:
            state = get_build_state(child_job, job)
            if state is not None:
                build_states.append(state)
    else:
        jenkins_job = server.get_job_info(job.name, 1)
        state = get_build_state(jenkins_job, job)
        if state is not None:
            build_states.append(state)

    return build_states


def state_to_numbers(state, building=False):
    switch_statement = state + "_building" if building else state
    return states.get(switch_statement, -1)


def number_to_state(number):
    for key, value in states.iteritems():
        if number == value:
            return key


def get_section_state_dict():
    global section
    section_state = dict()
    for section in config.sections:
        for job in section.jobs:
            try:
                build_states = get_build_states(job)
                for state in build_states:
                    current_state = state_to_numbers(state, job.building)
                    if section in section_state:
                        previous_state = state_to_numbers(section_state[section])
                        section_state[section] = number_to_state(current_state) if current_state < previous_state else section_state[section]
                    else:
                        section_state[section] = number_to_state(current_state)
            except jenkins.NotFoundException:
                print '%s WARNING: configured job "%s" for section "%s" not found' % (str(datetime.now()), job.name, section.name)
            except jenkins.JenkinsException:
                print '\t ----------------WARNING: error occured (JenkinsException):---------------------- '
                print traceback.print_exc()
                print '\t --------------------------------------------------------------------------------- '
    return section_state

get_section_state_dict()