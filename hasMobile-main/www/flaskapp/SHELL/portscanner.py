import sys
import socket
import datetime

# Adding a basic banner
print("-" * 50)
print("Time started: " + str(datetime.datetime.now()))
print("-" * 50)

# Function to scan ports and write to files
def scan_ports(target, start_port, end_port):
    print(f"Scanning target: {target}")
    try:
        with open("açık-port.txt", "a") as open_ports_file, open("kapalı-port.txt", "a") as closed_ports_file:
            for port in range(start_port, end_port + 1):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(1)
                result = s.connect_ex((target, port))

                if result == 0:
                    print(f"Port {port} open on {target}")
                    open_ports_file.write(f"{target}:{port}\n")
                else:
                    print(f"Port {port} closed on {target}")
                    closed_ports_file.write(f"{target}:{port}\n")
                s.close()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit()
    except socket.gaierror:
        print("The hostname couldn't be resolved.")
        sys.exit()
    except socket.error:
        print("Couldn't connect to the server.")
        sys.exit()

if len(sys.argv) not in [3, 4]:
    print("Invalid amount of arguments!")
    print("Syntax for file mode: python3 portscanner.py d=<filename> <initial port #> <end port #>")
    print("Syntax for single IP mode: python3 portscanner.py i=<ip>")
    sys.exit()

mode, value = sys.argv[1].split('=')

if mode == 'd' and len(sys.argv) == 4:
    try:
        with open(value, 'r') as file:
            ip_addresses = file.readlines()
        start_port = int(sys.argv[2])
        end_port = int(sys.argv[3])
        for ip in ip_addresses:
            ip = ip.strip()
            target = socket.gethostbyname(ip)
            scan_ports(target, start_port, end_port)
    except FileNotFoundError:
        print(f"File {value} not found.")
    except ValueError:
        print("Please provide valid port numbers.")
elif mode == 'i' and len(sys.argv) == 2:
    try:
        target = socket.gethostbyname(value)
        scan_ports(target, 3389, 3389)
    except socket.gaierror:
        print("The hostname couldn't be resolved.")
    except ValueError:
        print("Please provide a valid IP address.")
else:
    print("Invalid mode or number of arguments!")
    print("Syntax for file mode: python3 portscanner.py d=<filename> <initial port #> <end port #>")
    print("Syntax for single IP mode: python3 portscanner.py i=<ip>")

