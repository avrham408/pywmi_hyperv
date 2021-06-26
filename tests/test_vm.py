import time
import pytest
from pywmi_hyperv import Client
from win_helpers import run_ps_command
from pywmi_hyperv.win.enums import VmState


def test_vm_name(hyperv_client: Client, vm_name: str):
    vm = hyperv_client.get_vm(vm_name)
    assert vm.vm_name == vm_name


def test_vm_guid(hyperv_client: Client, vm_name: str):
    vm = hyperv_client.get_vm(vm_name)
    vm_guid = run_ps_command(f"(get-vm {vm_name}).VMId.Guid")
    assert vm.guid == vm_guid


@pytest.mark.timeout(120)
def test_change_vm_state_to_enabled(hyperv_client: Client, vm_name: str):
    run_ps_command(f"stop-vm {vm_name} -force")
    while run_ps_command("(get-vm test_vm).state") != "Off":
        time.sleep(3)
    vm = hyperv_client.get_vm(vm_name)
    vm._change_vm_state(VmState.Enabled)
    while run_ps_command("(get-vm test_vm).state") != "Running":
        time.sleep(1)


@pytest.mark.timeout(120)
def test_change_vm_state_to_disabled(hyperv_client: Client, vm_name: str):
    run_ps_command(f"start-vm {vm_name}")
    while run_ps_command("(get-vm test_vm).state") != "Running":
        time.sleep(3)
    vm = hyperv_client.get_vm(vm_name)
    vm._change_vm_state(VmState.Disabled)
    while run_ps_command("(get-vm test_vm).state") != "Off":
        time.sleep(1)


@pytest.mark.timeout(120)
@pytest.mark.skip("This operation is not async not implemented yet")
def test_change_vm_state_to_paused(hyperv_client: Client, vm_name: str):
    run_ps_command(f"start-vm {vm_name}")
    while run_ps_command("(get-vm test_vm).state") != "Running":
        time.sleep(3)
    vm = hyperv_client.get_vm(vm_name)
    vm._change_vm_state(VmState.Paused)
    time.sleep(3)
    import ipdb; ipdb.set_trace()
    assert run_ps_command("(get-vm test_vm).state") == "Paused"


@pytest.mark.timeout(120)
@pytest.mark.skip("This operation is not async not implemented yet")
def test_change_vm_state_to_resume(hyperv_client: Client, vm_name: str):
    run_ps_command(f"start-vm {vm_name}")
    while run_ps_command("(get-vm test_vm).state") != "Running":
        time.sleep(3)
    run_ps_command(f"Suspend-VM {vm_name}")
    while run_ps_command("(get-vm test_vm).state") != "Paused":
        time.sleep(3)
    import ipdb;ipdb.set_trace()
    vm = hyperv_client.get_vm(vm_name)
    vm._change_vm_state(VmState.Resuming)
    time.sleep(3)
    assert run_ps_command("(get-vm test_vm).state") == "Running"
