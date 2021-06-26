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
        if self.vm_state == state:
            return
        response = self._computer_system.RequestStateChange(state.value)
        try:
            change_state_response = ChangeVmStateResponse(response[1])
        except ValueError as error:
            raise UnknownRc from error
        if change_state_response == ChangeVmStateResponse.Transition_Started:
            logger.info(f"Started async job for {state.name} vm")
            res = wait_for_job_complete(self._client, response[0])
            if res[0] != 0:
                raise Exception(f"Change vm state failed with rc {res[0]} and stderr {res[1]}")
        else:
            raise NotImplementedError("We only support async job for change vm state for now")

    def start_vm(self):
        raise NotImplementedError

    def stop_vm(self):
        raise NotImplementedError

    def create_checkpoint(self):
        raise NotImplementedError

    def restore_checkpoint(self):
        raise NotImplementedError
