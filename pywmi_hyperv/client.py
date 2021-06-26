import logging
from typing import Optional
import wmi
import pywintypes
from pywmi_hyperv.vm import Vm
from pywmi_hyperv.exceptions import VmNotFound, ConnectToWmiError


logger = logging.getLogger(__name__)


def connect_to_wmi(
		server: str,
		user: str = "",
		password: str = "",
		namespace: str = r"root\virtualization\v2",
) -> wmi.WMI:
	try:
		conn = wmi.connect_server(
			server,
			namespace=namespace,
			user=user,
			password=password
		)
	except pywintypes.com_error as error:
		raise ConnectToWmiError("Connect to wmi failed") from error
	return wmi.WMI(wmi=conn)


class Client:
	def __init__(
			self,
			server: str,
			user: str = "",
			password: str = "",
			namespace: str = r"root\virtualization\v2"
	):
		self.server = server
		self.namespace = namespace
		self.user = user
		self.password = password
		self._connection: Optional[wmi.WMI] = None

	@property
	def connection(self):
		if not self._connection:
			self._connection = connect_to_wmi(
				self.server,
				self.user,
				self.password,
				self.namespace,
			)
		return self._connection

	def get_vm(self, vm_name: str) -> Optional[Vm]:
		logger.info(f"Trying to get {vm_name}")
		machine = self.connection.Msvm_ComputerSystem(ElementName=vm_name)
		if not machine:
			raise VmNotFound(f"{vm_name} not found")
		machine = machine[0]
		logger.info(f"vm {vm_name} found with guid {machine.Name}")
		return Vm(self.connection, machine.ElementName, machine.Name.lower())

