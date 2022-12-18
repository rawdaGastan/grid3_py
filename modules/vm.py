"""
Grid virtual machine module
"""

from dataclasses import dataclass


class VM:
    """VM class for grid virtual machine module"""

    def __init__(
        self,
        name: str,
        flist: str,
        flist_check_sum: str,
        public_ip: str,
        public_ip6: str,
        planetary: str,
        corex: str,
        computed_ip: str,
        computed_ip6: str,
        ygg_ip: str,
        ip: str,
        description: str,
        cpu: int,
        memory: int,
        rootfs_size: int,
        entry_point: str,
        mounts: list,
        zlogs: list,
        env_vars: map,
        network_name: str,
    ):
        self.name = name
        self.flist = flist
        self.flist_check_sum = flist_check_sum
        self.public_ip = public_ip
        self.public_ip6 = public_ip6
        self.planetary = planetary
        self.corex = corex
        self.computed_ip = computed_ip
        self.computed_ip6 = computed_ip6
        self.ygg_ip = ygg_ip
        self.ip = ip
        self.description = description
        self.cpu = cpu
        self.memory = memory
        self.rootfs_size = rootfs_size
        self.entry_point = entry_point
        self.mounts = mounts
        self.zlogs = zlogs
        self.env_vars = env_vars
        self.network_name = network_name
