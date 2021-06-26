import subprocess
from typing import Tuple


def run_ps_command(cmd) -> Tuple[int, str]:
    res = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    if res.returncode != 0:
        return res.returncode, res.stderr.decode().strip()
    return res.returncode, res.stdout.decode().strip()
