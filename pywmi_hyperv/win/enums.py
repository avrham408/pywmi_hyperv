from enum import Enum


class VmState(Enum):
    Other = 1
    Enabled = 2
    Disabled = 3
    ShutDown = 4
    Offline = 6
    Test = 7
    Defer = 8
    Quiesce = 9
    Reboot = 10
    Reset = 11
    Saving = 32773
    Pausing = 32776
    Resuming = 32777
    FastSaved = 32779
    FastSaving = 32780
    RunningCritical = 32781
    OffCritical = 32782
    StoppingCritical = 32783
    SavedCritical = 32784
    PausedCritical = 32785
    StartingCritical = 32786
    ResetCritical = 32787
    SavingCritical = 32788
    PausingCritical = 32789
    ResumingCritical = 32790
    FastSavedCritical = 32791
    FastSavingCritical = 32792
