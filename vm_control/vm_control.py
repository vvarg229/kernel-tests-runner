from abc import ABC, abstractmethod


class VMControl(ABC):
    """
    An abstract base class for managing virtual machines.
    Defines a common interface for all VM management classes.
    """

    @abstractmethod
    def start_vm(self, vm_name):
        """
        Start a virtual machine with the given name.

        :param vm_name: The name of the virtual machine.
        """
        pass

    @abstractmethod
    def stop_vm(self, vm_name):
        """
        Stop a virtual machine with the given name.

        :param vm_name: The name of the virtual machine.
        """
        pass

    @abstractmethod
    def restart_vm(self, vm_name):
        """
        Restart a virtual machine with the given name.

        :param vm_name: The name of the virtual machine.
        """
        pass

    @abstractmethod
    def create_vm(self, vm_name, **kwargs):
        """
        Create a virtual machine with the given name and parameters.

        :param vm_name: The name of the virtual machine.
        :param kwargs: Additional parameters for the virtual machine.
        """
        pass

    @abstractmethod
    def delete_vm(self, vm_name):
        """
        Delete a virtual machine with the given name.

        :param vm_name: The name of the virtual machine.
        """
        pass

    @abstractmethod
    def get_vm_status(self, vm_name):
        """
        Get the status of a virtual machine with the given name.

        :param vm_name: The name of the virtual machine.
        :return: The status of the virtual machine.
        """
        pass
