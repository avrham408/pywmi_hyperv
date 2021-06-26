from enum import Enum


class VmState(Enum):
    Enabled = 2
    Disabled = 3
    Quiesce = 9
    Reboot = 10
    Reset = 11
    Paused = 32768
    Resuming = 32777
    Suspended = 32769


class ChangeVmStateResponse(Enum):
    CompletedWithNoError = 0
    DMTFReserved = 74095
    Transition_Started = 4096  # Method Parameters Checked Transition Started - started async job
    Failed = 32768
    AccessDenied = 32769
    NotSupported = 32770
    StatusIsUnknown = 32771
    Timeout = 32772
    InvalidParameter = 32773
    SystemIsInUse = 32774
    InvalidStateForThisOperation = 32775
    IncorrectData = 32776
    SystemIsNotAvailable = 32777
    OutOfMemory = 32778


class JobState(Enum):
    New = 2  # The job has never been started.
    Starting = 3  # The job is moving from the 2 (New), 5 (Suspended), or 11 (Service) states into the 4 (Running) state.
    Running = 4  # The job is running.
    Suspended = 5  # The job is stopped, but it can be restarted in a seamless manner.
    Shutting_Down = 6  # The job is moving to a 7 (Completed), 8 (Terminated), or 9 (Killed) state.
    Completed = 7  # The job has completed normally.
    Terminated = 8  # The job has been stopped by a "Terminate" state change request. The job and all its underlying processes are ended and can be restarted only as a new job. The requirement that the job be restarted only as a new job is job-specific.
    Killed = 9 	# The job has been stopped by a "Kill" state change request. Underlying processes may still be running, and a clean-up might be required to free up resources.
    Job_Exception = 10  # The job is in an abnormal state that might be indicative of an error condition. The actual status of the job might be available through job-specific objects.
    Service = 11  # The job is in a vendor-specific state that supports problem discovery, or resolution, or both.
