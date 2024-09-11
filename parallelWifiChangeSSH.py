import paramiko
from multiprocessing import Pool
import time

username = ""
password = ""

def read_pw_from_file(pw):
    with open(pw, 'r') as file:
        return file.read().strip()

# IP addresses of the 20 Raspberry Pis
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
    "192.168.8.201",
    "192.168.8.102",
    "192.168.8.171",
    "192.168.8.228",
    "192.168.8.204"
]

commands1 = [
    "sudo nmcli dev wifi list",
    'sudo nmcli dev wifi connect "routernameGeneral" password ""'
]
wifi_pw = read_pw_from_file('pw.txt')

commands2 = [
    "sudo nmcli dev wifi list",
    f'sudo nmcli dev wifi connect "routernameGeneral" password "{wifi_pw}"'
]

def ssh_command(host):
    max_retries = 3
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)
        
        success = False
        for retry in range(max_retries):
            for command in commands1:
                stdin, stdout, stderr = client.exec_command(command)
                stdout.channel.recv_exit_status()
                output = stdout.read().decode('utf-8').strip()
                error = stderr.read().decode('utf-8').strip()
                
                if output:
                    print(f"Device {host} - Command Output: {output}")
                if error:
                    print(f"Device {host} - Error: {error}")

            # Check connection status
            stdin, stdout, stderr = client.exec_command('nmcli -t -f active,ssid dev wifi | egrep "^yes"')
            wifi_info = stdout.read().decode().strip()
            if wifi_info and "router" in wifi_info:
                print(f"Device {host} successfully connected to router")
                success = True
                break
            else:
                print(f"Device {host} failed to connect to router, retrying...")
                time.sleep(5)  # Wait before retrying

        if not success:
            print(f"Device {host} could not connect to router after {max_retries} retries")

        client.close()

    except Exception as e:
        print(f"Failed to connect to device {host} or execute commands: {str(e)}")

if __name__ == "__main__":
    with Pool(len(hosts)) as pool:
        pool.map(ssh_command, hosts)
