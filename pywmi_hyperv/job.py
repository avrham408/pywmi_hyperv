from typing import Tuple
import logging
from wmi import WMI
from pywmi_hyperv.win.enums import JobState
from pywmi_hyperv.util import _parse_job_id
from pywmi_hyperv.exceptions import JobNotExist, UnknownState
import time


logger = logging.getLogger(__name__)


def wait_for_job_complete(connection: WMI, job_res: str, timeout: int = 300) -> Tuple[int, str]:
    job_id = _parse_job_id(job_res)
    start_time = time.time()
    while time.time() - start_time < timeout:
        logger.info(f"job res - {job_res} job id = {job_id}")
        job = connection.Msvm_ConcreteJob(InstanceID=job_id)
        if not job:
            raise JobNotExist(f"we got {job_res} we parsed the job id - {job_id} and the job not exist")
        job = job[0]
        try:
            job_state = JobState(int(job.JobState))
        except ValueError as error:
            raise UnknownState from error
        if job_state in [JobState.New, JobState.Starting, JobState.Running, JobState.Shutting_Down]:
            time.sleep(1)
        elif job_state in [JobState.Suspended, JobState.Terminated, JobState.Killed]:
            raise Exception(f"The job {job_state.name}")
        elif job_state == JobState.Job_Exception:
            return job.ErrorCode, job.ErrorDescription
        elif job_state == JobState.Completed:
            return 0, "The job has completed normally"  # from completed enumerator meaning in msvm-concretejob.JobState
        else:
            raise NotImplementedError(f"The job state is not supported {job_state}")
    raise TimeoutError(f"Waiting for async job(Msvm_ConcreteJob) {job_id} failed after {timeout} seconds")