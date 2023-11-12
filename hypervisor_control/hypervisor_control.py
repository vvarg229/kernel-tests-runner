from abc import ABC, abstractmethod


class HypervisorControlBase(ABC):
    """
    An abstract base class for managing hypervisor.
    """

    @abstractmethod
    def hypervisor_lock(self):
        """
        Lock a hypervisor.
        """
        pass

    @abstractmethod
    def hypervisor_unlock(self):
        """
        Unlock a hypervisor.
        """
        pass

    @abstractmethod
    def hypervisor_finish(self):
        """
        Finish working with the hypervisor.
        """
        pass

    @abstractmethod
    def hypervisor_clean(self):
        """
        Clean temporary ktest files and volumes on hypervisor.
        """
        pass
