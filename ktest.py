import os
import shutil
import sys
import argparse
import logging
import libvirt
import tempfile
import subprocess

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Control and manage light VM for run kernel modules testing. ctrl+] can be used to stop the VM .ktest file is sourced in current directory and can be used to predefine parameters."
    )
    parser.add_argument("kernel", help="Kernel image to use with the VM", nargs="?")
    parser.add_argument("-x", "--debug", action="store_true", help="Trace execution")
    parser.add_argument(
        "--debug-libvirt", metavar="LEVEL", help="Set LIBVIRT_DEBUG to LEVEL"
    )
    parser.add_argument(
        "--disable-console",
        action="store_true",
        help="Don't connect to VM console after start",
    )
    parser.add_argument(
        "--disable-kdump", action="store_true", help="Don't setup kdump"
    )
    parser.add_argument("-f", "--force", action="store_true", help="Stop running VM")
    parser.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help="Remove kernel and initramfs volumes after VM shutdown",
    )
    parser.add_argument(
        "-G", "--gdb", metavar="[HOST]:PORT", help="Enable QEMU GDB stub via HOST:PORT"
    )
    parser.add_argument("-k", "--kopt", action="append", help="Pass a kernel option")
    parser.add_argument(
        "-K", "--keep", action="store_true", help="Don't shutdown VM immediately"
    )
    parser.add_argument(
        "--kmoddir", help="A directory where to look for kernel modules"
    )
    parser.add_argument("--fwdir", help="A directory where to find firmware")
    parser.add_argument("--vcpu", type=int, help="Specify number of virtual CPUs")
    parser.add_argument(
        "-M",
        "--memory",
        type=int,
        default=512,
        help="Specify amount of memory in megabytes",
    )
    parser.add_argument(
        "-m", "--module", action="append", help="Install a kernel module into initramfs"
    )
    parser.add_argument(
        "-d",
        "--directory",
        action="append",
        metavar="LOCAL:REMOTE",
        help="Pass a directory and mount it under a path",
    )
    parser.add_argument(
        "-D",
        "--disk",
        action="append",
        metavar="NAME:<scsi|blk>:SIZE",
        help="Make virtio-scsi/virtio-blk disk that's available from the VM. Where NAME is alphanumeric that'll be used as disk serial, SIZE is a number following G, M or K suffix (Gigabytes, Megabytes or Kilobytes, respectively).",
    )
    parser.add_argument(
        "-n",
        "--net",
        action="append",
        metavar="<bridge=NAME|network=NAME|ovs=NAME|user>[:mac=ADDR][:dhcp]",
        help="Configure a virtio-net interface",
    )
    parser.add_argument("-o", "--output", help="A directory to store results")
    parser.add_argument(
        "-e", "--entry-point", help="Start an executable after init is completed"
    )
    parser.add_argument(
        "-i", "--install", action="append", help="Install PROGRAM into initramfs"
    )
    parser.add_argument(
        "-I",
        "--include",
        action="append",
        metavar="SRC[:DST]",
        help="Include a file or directory into initramfs. Destination in initramfs can be specified in DST.",
    )
    parser.add_argument("--docker-image", help="Docker image to build initramfs")
    parser.add_argument("--uri", help="Set URI to hypervisor")
    parser.add_argument(
        "--pool", default="default", help="Pool to store the kernel and initramfs"
    )
    parser.add_argument("--owner", default=os.getlogin(), help="Owner of the VM")
    parser.add_argument("-t", "--timeout", type=int, default=600, help="VM timeout")
    parser.add_argument(
        "--kdump-timeout",
        type=int,
        default=180,
        help="Specifies time limit for kernel dump.",
    )
    parser.add_argument(
        "--crashdrive-size", default="5G", help="Is the crash drive SIZE in bytes."
    )
    args = parser.parse_args()

    # Check for kernel argument
    if not args.kernel:
        parser.error("The kernel argument is required")

    return args


def check_deps(deps: list[str]):
    for dep in deps:
        if not is_tool(dep):
            logging.error(f"{dep} is not installed")
            sys.exit(f"{dep} is not installed")
    logging.debug(f"All dependencies are installed")


def is_tool(name: str):
    return shutil.which(name) is not None


def main():
    deps = ["socat", "xml", "virsh", "bc"]
    check_deps(deps)

    # Parse command line arguments
    args = parse_args()
    logging.debug(f"Command line arguments: {args}")

    if args.debug:
        logging.debug("Debug mode is enabled.")

    # Setup environment variables and config
    os.environ["LANG"] = "C"
    config = os.environ.get("CONFIG", ".ktest")
    if not os.environ.get("NO_CONFIG") and os.path.isfile(config):
        logging.debug(f"Loading config from {config}")
        exec(open(config).read())
    else:
        logging.debug(f"Config {config} not found, running with command line arguments")

    logging.info(f"Starting VM with kernel: {args.kernel}")


if __name__ == "__main__":
    main()
