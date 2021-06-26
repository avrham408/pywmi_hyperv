import logging
from wmi import WMI
from pywmi_hyperv.win.enums import VmState
from wmi import _wmi_object

logger = logging.getLogger(__name__)


class Vm:
    def __init__(
            self,
            client: WMI,
            vm_name: str,
            guid: str,
            vm_object: _wmi_object
    ):
        self._client = client
        self.vm_name = vm_name
        self.guid = guid
        self._vm_wmi_object: _wmi_object = vm_object  #  Msvm_ComputerSystem instance

    def _change_vm_state(self, state: VmState):
        self._vm_wmi_object.RequestStateChange(state.value)

    def start_vm(self):
        pass
        # job_res, rc = vm.RequestStateChange(state.value)
        # if rc == RequestedStateRes.Transition_Started.value:  # asyn start
        #     # check_if_job_succced
        #     if __handle_job_response(client, job_res):
        #         return vm
        # else:
        #     raise infra_exceptions.ChangeVmStateError(f"RequestStateChange for vm {vm_name} returned with code {rc}")

    def stop_vm(self):
        pass

    def create_checkpoint(self):
        pass

    def restore_checkpoint(self):
        pass
