from typing import Tuple
import pytest
from pytest import fixture
from _pytest.fixtures import SubRequest
import platform
from pywmi_hyperv import Client
from tests.win_helpers import run_ps_command


def pytest_addoption(parser) -> None:  # type: ignore
    parser.addoption("--vm_name", action="store", default="test_vm")


@fixture(scope="function")
def host_name() -> str:
    return platform.uname()[1]


@fixture(scope="function")
def auth() -> Tuple[str, str]:
    return "user", "Welcome01"


@fixture(scope="function")
def vm_name(request: SubRequest) -> str:
    return request.config.option.vm_name


@fixture(scope="function")
def hyperv_client() -> Client:
    return Client(platform.uname()[1])


@fixture(scope="session",  autouse=True)
def validate_permission() -> None:
    """
        we don't support in test now remote hyper-v
        connection even if the client in potential can work with remote
    """
    res = run_ps_command(
        "(New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent()))"
        ".IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)"
    )
    if res[0] != 0:
        raise Exception(f"While trying to check if you is admin"
                        f" raised error from the powershell command -  {res[0]} error code with stderr: {res[1]}")
    if res[1] == "True":
        return
    elif res[1] == "False":
        pytest.exit("The user your running is not with admin rights the pytest run stoped!")
    else:
        raise Exception(f"validate permission failed the ps "
                        f"command didn't failed but the stdout is not right {res[1]}")
