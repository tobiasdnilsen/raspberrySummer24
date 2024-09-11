import paramiko
from multiprocessing import Pool

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

        command = "/usr/sbin/ifconfig | grep -A 1 wlan0 | awk '/inet /{print $2}'"
        stdin, stdout, stderr = client.exec_command(command)
        wlan0_ip = stdout.read().decode().strip()
        error_output = stderr.read().decode().strip()

        if error_output:
            print(f"Error output from {host}:\n{error_output}")

        return host, wlan0_ip if wlan0_ip else "N/A"
    except Exception as e:
        print(f"Error for {host}: {str(e)}")
        return host, "N/A"
    finally:
        if client:
            client.close()

if __name__ == "__main__":
    try:
        with Pool(processes=len(hosts)) as pool:
            results = pool.map(ssh_command, hosts)

        with open('rpi_wlan0_ips.txt', 'w') as file:
            for host, wlan0_ip in results:
                file.write(f"{host}: {wlan0_ip}\n")
                print(f"{host}: {wlan0_ip}")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
