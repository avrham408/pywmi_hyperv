import logging
from wmi import WMI
from wmi import _wmi_object
from pywmi_hyperv.win.enums import VmState, ChangeVmStateResponse
from pywmi_hyperv.exceptions import UnknownRc
from pywmi_hyperv.job import wait_for_job_complete


logger = logging.getLogger(__name__)


class Vm:
    def __init__(
            self,
            client: WMI,
            vm_name: str,
            guid: str,
    ):
        self._client = client
        self.vm_name = vm_name
        self.guid = guid

    @property
    def _computer_system(self):  # Msvm_ComputerSystem
        try:
            return self._client.Msvm_ComputerSystem(ElementName=self.vm_name)[0]
        except IndexError:
            raise Exception(f"Vm {self.vm_name} is not exist any more")

    @property
    def _information_system(self):  # Msvm_SummaryInformation
        try:
            return self._client.Msvm_SummaryInformation(ElementName=self.vm_name)[0]
        except IndexError:
            raise Exception(f"Vm {self.vm_name} is not exist any more")

    @property
    def vm_state(self):
        try:
            return VmState(self._computer_system.EnabledState)
        except ValueError as error:
            raise UnknownRc from error

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
