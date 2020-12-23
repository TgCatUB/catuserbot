from subprocess import PIPE, Popen


def install_pip(pipfile):
    process = Popen(["pip", "install", f"{pipfile}"], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return stdout
