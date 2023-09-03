"""Find the IPs for all adapters on the system."""

import ifaddr

adapters = ifaddr.get_adapters()

for adapter in adapters:
    for ip in adapter.ips:
        if (not ip.is_IPv6):
            print(ip.ip)