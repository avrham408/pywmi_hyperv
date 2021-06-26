from typing import Tuple
import pytest
from pywmi_hyperv import Client
from pywmi_hyperv.exceptions import VmNotFound, ConnectToWmiError


@pytest.mark.skip(reason="Problem with azure ad fix in another env")
def test_connect_wmi_client_with_permssions(host_name: str, auth: Tuple[str, str]) -> None:
    user = auth[0]
    password = auth[1]
    client = Client(host_name, user=user, password=password)
    assert client.connection


def test_connect_wmi_client(host_name: str) -> None:
    client = Client(host_name)
    assert client.connection


def test_not_exist_host_name():
    client = Client("Not exist host name")
    with pytest.raises(ConnectToWmiError):
        client.connection


def test_get_vm_for_exist_vm(hyperv_client: Client, vm_name: str) -> None:
    assert hyperv_client.get_vm(vm_name)


def test_get_vm_for_not_exist_vm(hyperv_client):
    with pytest.raises(VmNotFound):
        hyperv_client.get_vm("not exist vm")
