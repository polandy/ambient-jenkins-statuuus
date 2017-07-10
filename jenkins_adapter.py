import config
import jenkins
import traceback

server = jenkins.Jenkins(config.jenkins_url, username=config.jenkins_username, password=config.jenkins_password)


def get_build_state(job):
    last_build = job['lastBuild']
    if last_build is not None:
        if last_build['building'] and last_build['number'] > 0:
            last_completed_build = job['lastCompletedBuild']
            if last_completed_build is not None:
                return last_completed_build['result'] + '_building'
        else:
            return last_build['result']


def get_build_states(job):
    build_states = []

    if job.pipeline:
        for child_job in server.get_job_info(job.name, 2)['jobs']:
            state = get_build_state(child_job)
            if state is not None:
                build_states.append(state)
    else:
        jenkins_job = server.get_job_info(job.name, 1)
        state = get_build_state(jenkins_job)
        if state is not None:
            build_states.append(state)

    return build_states


def status_to_numbers(argument):
    switcher = {
        "FAILURE_building": -4,
        "FAILURE": -3,
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
        for job in section.jobs:
            try:
                build_states = get_build_states(job)
                for state in build_states:
                    if section in section_state:
                        section_state[section] = state if status_to_numbers(state) < status_to_numbers(section_state[section]) else section_state[section]
                    else:
                        section_state[section] = state
            except jenkins.NotFoundException:
                print 'WARNING: configured job "%s" for section "%s" not found' % (job.name, section.name)
            except jenkins.JenkinsException:
                print '\t ----------------WARNING: error occured (JenkinsException):---------------------- '
                print traceback.print_exc()
                print '\t --------------------------------------------------------------------------------- '
    return section_state

# get_section_state_dict()