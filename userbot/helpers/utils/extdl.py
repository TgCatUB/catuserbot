from subprocess import PIPE, Popen


def install_pip(pipfile):
    print(f"installing {pipfile}")
    pip_cmd = ["pip", "install", f"{pipfile}"]
    process = Popen(pip_cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return stdout
