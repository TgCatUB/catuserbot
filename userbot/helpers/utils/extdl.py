from subprocess import PIPE, Popen


def install_pip(pipfile):
    pip_cmd = ["pip", "install", f"{pipfile}"]
    process = Popen(pip_cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return stdout
