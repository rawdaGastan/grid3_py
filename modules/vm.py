"""
Grid virtual machine module
"""

from dataclasses import dataclass


@dataclass
class VM:
    """VM class for grid virtual machine module"""

    name: str
    flist: str
    flist_check_sum: str
    public_ip: str
    public_ip6: str
    planetary: str
    corex: str
    computed_ip: str
    computed_ip6: str
    ygg_ip: str
    ip: str
    description: str
    cpu: int
    memory: int
    rootfs_size: int
    entry_point: str
    mounts: list
    zlogs: list
    env_vars: map
    network_name: str
