# Import modules
import os
import subprocess
import ipaddress

# TODO(gam4it) : Make ping.py as a module of a package called network-tools.
# TODO(gam4it) : Make a separate module (or package) for ANSI color.

# Prompt the user to input a network address
net_addr = input("Enter a network address in CIDR format(ex.192.168.1.0/24): ")

# Create the network
ip_net = ipaddress.ip_network(net_addr)

# Get all hosts on that network
all_hosts = list(ip_net.hosts())

# Configure subprocess to hide the console window
startup_info = None
if os.name == 'nt':
    startup_info = subprocess.STARTUPINFO()
    startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup_info.wShowWindow = subprocess.SW_HIDE

# For each IP address in the subnet, 
# run the ping command with subprocess.popen interface
print("\n\033[1;31;40m Y \033[0m: Response, \033[0;30;47m N \033[0m: No response\n")
for i in range(len(all_hosts)):
    if os.name == 'nt':
        output = subprocess.Popen(['ping', '-n', '1', '-w', '500', str(all_hosts[i])], stdout=subprocess.PIPE, startupinfo=startup_info).communicate()[0]
    else:
        output = subprocess.Popen(['ping', '-c', '3', '-t', '3', str(all_hosts[i])], stdout=subprocess.PIPE, startupinfo=startup_info).communicate()[0]
    
    if "Destination host unreachable" in output.decode('utf-8'):
        print(str(all_hosts[i]), "is N")
    elif "Request timed out" in output.decode('utf-8'):
        print(str(all_hosts[i]), "is N")
    elif "Request timeout" in output.decode('utf-8'):
        print(str(all_hosts[i]),"   \033[0;30;47m N \033[0m")
    else:
        if os.name == 'nt':
            print(str(all_hosts[i]), "   Y")
        else:
            print(str(all_hosts[i]), "   \033[1;31;40m Y \033[0m")
