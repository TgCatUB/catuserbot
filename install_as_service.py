import logging
import os
import pwd
from pathlib import Path
import subprocess
import sys

# Logger = = = = =
logger = logging.getLogger("Service Setup")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

# Constants = = = = =
UV_BIN_DIR = Path.home() / ".local" / "bin"
SUBPROCESS_ENV = {**os.environ, "PATH": f"{UV_BIN_DIR}:{os.environ.get('PATH', '')}"}

COMMANDS_STAGE_1 = [
    (["chmod", "+x", "uv-installer.sh"], None),
    (["./uv-installer.sh"], None),
    (["uv", "venv", "--python", "3.11"], {"UV_PYTHON_INSTALL_DIR": "/opt/uv-python"}),
    (["uv", "pip", "install", "-r", "requirements.txt"], {"UV_PYTHON_INSTALL_DIR": "/opt/uv-python"}),
    (["apt-get", "install", "-y", "postgresql", "postgresql-contrib"], None),
]

COMMANDS_STAGE_3 = [
    "systemctl enable catuserbot.service",
    "systemctl start catuserbot.service",
    "systemctl status catuserbot.service",

]


# Helper functions = = = = =
def setup_database(db_name="catuserbot", user="postgres", env_file=".env"):
    """Create database"""
    try:
        result = subprocess.run(
            ["sudo", "-u", "postgres", "psql", "-tAc",
             f"SELECT 1 FROM pg_database WHERE datname='{db_name}';"],
            check=True,
            capture_output=True,
            text=True
        )
        db_exists = result.stdout.strip() == "1"

        if db_exists:
            logger.info(f"\nDatabase '{db_name}' already exists.")
            logger.info("  [1] Keep existing database and continue")
            logger.info("  [2] Drop and recreate (ALL DATA WILL BE LOST)")
            choice = input("Enter choice (1/2): ").strip()

            if choice == "2":
                confirm = input(f"Are you sure you want to delete '{db_name}'? Type YES to confirm: ").strip()
                if confirm.lower() == "yes":
                    password = input(f"Enter new password for user '{user}': ").strip()
                    subprocess.run(
                        ["sudo", "-u", "postgres", "dropdb", db_name], 
                        check=True
                        )
                    logger.info("Dropped existing database '%s'.", db_name)
                    subprocess.run(
                        ["sudo", "-u", "postgres", "psql", "-c", f"ALTER USER {user} WITH PASSWORD '{password}';"],
                        check=True
                    )
                    subprocess.run(["sudo", "-u", "postgres", "createdb", db_name, "-O", user], check=True)
                    logger.info("Database '%s' recreated with new password.", db_name)
                else:
                    logger.info("Drop cancelled. Keeping existing database.")
                    password = input(f"Enter current password for user '{user}': ").strip()
            else:
                password = input(f"Enter current password for user '{user}': ").strip()
                subprocess.run(
                    ["sudo", "-u", "postgres", "psql", "-c", f"ALTER USER {user} WITH PASSWORD '{password}';"],
                    check=True
                )
                logger.info("Keeping existing database '%s' with updated password.", db_name)

        else:
            password = input(f"Enter password for new user '{user}': ").strip()
            subprocess.run(
                ["sudo", "-u", "postgres", "psql", "-c", f"ALTER USER {user} WITH PASSWORD '{password}';"],
                check=True
            )
            subprocess.run(["sudo", "-u", "postgres", "createdb", db_name, "-O", user], check=True)
            logger.info("Database '%s' created with user '%s'.", db_name, user)

        db_url = f"postgresql://{user}:{password}@localhost:5432/{db_name}"

        if os.path.exists(env_file):
            with open(env_file, "r") as f:
                lines = f.readlines()
            with open(env_file, "w") as f:
                updated = False
                for line in lines:
                    if line.startswith("DATABASE_URL = "):
                        f.write(f"DATABASE_URL = \"{db_url}\"\n")
                        updated = True
                    else:
                        f.write(line)
                if not updated:
                    f.write(f"DATABASE_URL = \"{db_url}\"\n")
        else:
            raise FileNotFoundError(".env file dosent exists")

        logger.info("Database URL updated in '%s'.", env_file)
        logger.info(f"\nDatabase URL: {db_url}")

    except subprocess.CalledProcessError as e:
        logger.error("Database setup failed: %s", e, exc_info=True)
        raise

def is_database_operational(db_name="catuserbot", user="postgres"):
    try:
        subprocess.run(
            ["psql", "-U", user, "-d", db_name, "-c", "SELECT 1;"],
            check=True,
            capture_output=True,
            text=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        logger.error(e, exc_info=True)
        return False
    except Exception as e:
        logger.error(e, exc_info=True)
        return False


# Stages = = = = =
def stage_1():
    """Installing the necessary things"""
    for cmd, env_vars in COMMANDS_STAGE_1:
        env = SUBPROCESS_ENV.copy()
        if env_vars:
            env.update(env_vars)
        logger.info("Running: %s", cmd)
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                env=env,
            )
            if result.stdout:
                logger.info(result.stdout)
            if result.stderr:
                logger.warning(result.stderr)
        except subprocess.CalledProcessError as e:
            logger.error("Command failed: %s\n%s", cmd, e.stderr, exc_info=True)
            raise

    setup_database()


def stage_2(catuserbot_path: Path):
    """Config var check"""
    venv_python = catuserbot_path / ".venv" / "bin" / "python3"
    checker_script = catuserbot_path / "_install_checker.py"
    result = subprocess.run(
        [str(venv_python), str(checker_script)],
        text=True,
        cwd=str(catuserbot_path),
    )
    if result.returncode != 0:
        raise RuntimeError("Stage 2 checks failed — see errors above.")
    logger.info("All stage 2 checks passed.")


def stage_3():
    """Converting into service"""
    user = os.environ.get("SUDO_USER") or pwd.getpwuid(os.getuid()).pw_name

    current_file = Path(__file__)
    catuserbot_path = current_file.parent
    venv_python_path = catuserbot_path / ".venv" / "bin" / "python3"
    service_file = f"""
[Unit]
Description="A simple Telegram userbot based on Telethon "
Requires=network.target
After=network.target

[Service]
User={user}
Type=simple
ExecStart={venv_python_path} -m userbot
WorkingDirectory={catuserbot_path}
Restart=always

# Logging
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
"""
    file = open("/etc/systemd/system/catuserbot.service","w")
    file.write(service_file)
    file.close()

    subprocess.run(
        ["chown", "-R", f"{user}:{user}", str(catuserbot_path / ".venv")],
        check=True,
        text=True
    )

    for cmd in COMMANDS_STAGE_3:
        logger.info("Running: %s", cmd)
        try:
            subprocess.run(
                cmd.split(),
                check=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            logger.error("Command failed: %s\n%s", cmd, e.stderr, exc_info=True)
            raise


# Main function
def main():
    catuserbot_path = Path(__file__).parent
    stage_1()
    stage_2(catuserbot_path)
    stage_3()


# Entry point
if __name__ == "__main__":
    if os.getegid() != 0:
        logger.info("Use sudo to run this script,\nthis script makes a new service thats why sudo permission is essential.\nCheck install_as_service.py and _install_checker.py if you are concerned about security.\nThank you!")
    else:
        #not installing venv twice
        if Path(".venv").exists() and sys.argv[1] != "--force":
            for i in range(3):
                COMMANDS_STAGE_1.pop(0)
        main()

#End of the universe :)