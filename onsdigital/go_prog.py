import util

def install(prog_name):
    get_url = util.go_get_url(prog_name)
    util.execute_command_and_ignore_failure('go get %s' % get_url)