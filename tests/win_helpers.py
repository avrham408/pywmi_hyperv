import subprocess


def run_ps_command(cmd) -> str:
    res = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    if res.returncode != 0:
        raise Exception(f"something went wrong with powershell command {cmd} error code {res.returncode} and stderr -  {res.stderr}")
    return res.stdout.decode().strip()
