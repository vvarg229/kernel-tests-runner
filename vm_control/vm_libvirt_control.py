import libvirt
from vm_control.vm_control import VMControl


class VMLibvirtControl(VMControl):
    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        self.conn = libvirt.open()
        if self.conn is None:
            raise Exception("Failed to open connection to the hypervisor")

    def start_vm(self, vm_name):
        try:
            dom = self.conn.lookupByName(vm_name)
            if dom is None:
                raise Exception(f"VM {vm_name} does not exist")
            if dom.create() < 0:
                raise Exception(f"Failed to start VM {vm_name}")
            print(f"VM {vm_name} started successfully")
        except libvirt.libvirtError as e:
            raise Exception(f"Error starting VM {vm_name}: {e}")

    def stop_vm(self, vm_name):
        try:
            dom = self.conn.lookupByName(vm_name)
            if dom is None:
                raise Exception(f"VM {vm_name} does not exist")
            if dom.destroy() < 0:
                raise Exception(f"Failed to stop VM {vm_name}")
            print(f"VM {vm_name} stopped successfully")
        except libvirt.libvirtError as e:
            raise Exception(f"Error stopping VM {vm_name}: {e}")

    def restart_vm(self, vm_name):
        self.stop_vm(vm_name)
        self.start_vm(vm_name)

    def create_vm(self, vm_name, **kwargs):
        pass

    def delete_vm(self, vm_name):
        pass

    def get_vm_status(self, vm_name):
        try:
            dom = self.conn.lookupByName(vm_name)
            if dom is None:
                raise Exception(f"VM {vm_name} does not exist")
            info = dom.info()
            return info[0]
        except libvirt.libvirtError as e:
            raise Exception(f"Error getting status of VM {vm_name}: {e}")
