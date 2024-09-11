import paramiko
from multiprocessing import Pool
import re

hosts = [
    "192.168.8.173", 
    "192.168.8.138",
    "192.168.8.160",
    "192.168.8.198",
    "192.168.8.154",
    "192.168.8.226",
    "192.168.8.174",
    "192.168.8.117",
    "192.168.8.190",
    "192.168.8.207",
    "192.168.8.244",
    "192.168.8.215",
    "192.168.8.105",
    "192.168.8.120",
    "192.168.8.123", 
    "192.168.8.201",
    "192.168.8.102",
    "192.168.8.171",
    "192.168.8.228",
    "192.168.8.204"
]

username = ""
password = ""

def ssh_command(host):
    client = None
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)

        stdin, stdout, stderr = client.exec_command('hostname')
        hostname = stdout.read().decode().strip()
        
        stdin, stdout, stderr = client.exec_command('nmcli -t -f active,ssid dev wifi | egrep "^yes"')
        wifi_info = stdout.read().decode().strip()
        if wifi_info:
            ssid = wifi_info.split(":")[1]
        else:
            ssid = "N/A"

        return (host, hostname, "online", ssid)
    except Exception as e:
        return (host, "N/A", "offline", "N/A")
    finally:
        if client:
            client.close()

def extract_pi_number(hostname):
    match = re.search(r'test-pi-(\d+)', hostname)
    if match:
        return int(match.group(1))
    return float('inf')

if __name__ == "__main__":
    try:
        with Pool(len(hosts)) as p:
            results = p.map(ssh_command, hosts)

        results.sort(key=lambda x: extract_pi_number(x[1]))

        print(f"{'IP Address':<15} {'Hostname':<20} {'Status':<10} {'Connected Wi-Fi':<20}")
        print("-" * 65)

        for host, hostname, status, ssid in results:
            print(f"{host:<15} {hostname:<20} {status:<10} {ssid:<20}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
