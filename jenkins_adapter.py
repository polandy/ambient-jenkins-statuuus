import config
import jenkins
import copy
import traceback
from datetime import datetime

from model import SectionState

server = jenkins.Jenkins(config.jenkins_url, username=config.jenkins_username, password=config.jenkins_password)




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


def get_section_state_dict():
    global section
    section_state = dict()
    for section in copy.deepcopy(config.sections):
        for job in section.jobs:
            try:
                build_states = get_build_states(job)
                for state in build_states:
                    current_state = SectionState(state, job.building)
                    if section in section_state:
                        previous_state = section_state[section]
                        section_state[section] = current_state if current_state.intValue < previous_state.intValue else section_state[section]
                        if job.building:
                            section_state[section].building = True
                    else:
                        section_state[section] = current_state
            except jenkins.NotFoundException:
                print '%s WARNING: configured job "%s" for section "%s" not found' % (str(datetime.now()), job.name, section.name)
            except jenkins.JenkinsException:
                print '\t ----------------WARNING: error occured (JenkinsException):---------------------- '
                print traceback.print_exc()
                print '\t --------------------------------------------------------------------------------- '
    return section_state

# get_section_state_dict()