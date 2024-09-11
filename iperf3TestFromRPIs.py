import paramiko
from multiprocessing import Pool

hosts = [
    "192.168.8.228", 
    "192.168.8.160",
    "192.168.8.201",
    "192.168.8.154",
    "192.168.8.174",
    "192.168.8.198",
    "192.168.8.102",
    "192.168.8.190",
    "192.168.8.117",
    "192.168.8.171",
    "192.168.8.120",
    "192.168.8.138",
    "192.168.8.173",
    "192.168.8.226"
]

username = ""
password = ""
base_port = 5201 

def ssh_command(args):
    host, port = args
    client = None
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)

        command = f'iperf3 -c 192.168.8.217 -p {port} -t 10 -b 1M -P 100'
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()

        if error:
            result = error
        else:
            result = output

        return (host, result)
    except Exception as e:
        return (host, str(e))
    finally:
        if client:
            client.close()

if __name__ == "__main__":
    try:
        with Pool(len(hosts)) as p:
            host_port_pairs = [(hosts[i], base_port + i) for i in range(len(hosts))]
            results = p.map(ssh_command, host_port_pairs)

        for host, result in results:
            print(f"Host: {host}")
            print(result)
            print("-" * 40)
    except Exception as e:
        print(f"Error occurred: {str(e)}")
