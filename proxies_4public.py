import subprocess
import os
import pyfiglet
import colorama
from colorama import Fore, Style, Back
import time

# Initialize colorama
colorama.init()

# Set the URL for the socks4 list, HTTP, and a fresh proxychains.conf file.
socks4_url = "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt"
http_url = "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"

# Download the socks4 list using curl
subprocess.run(["curl", socks4_url, "-o", "socks4.txt"])
subprocess.run(["curl", http_url, "-o", "http.txt"])

# Reformat the socks4 list and save it to a new file
with open("socks4.txt") as f:
    lines = f.readlines()

formatted_lines = []
for line in lines:
    parts = line.strip().split(":")
    ip_address = parts[0]
    port = parts[1]
    formatted_line = f"socks4 {ip_address} {port}"
    formatted_lines.append(formatted_line)

with open("socks4_formatted.txt", "w") as f:
    for line in formatted_lines:
        f.write(line + "\n")

# Reformat the socks4 list and save it to a new file
with open("http.txt") as f:
    lines = f.readlines()

formatted_lines = []
for line in lines:
    parts = line.strip().split(":")
    ip_address = parts[0]
    port = parts[1]
    formatted_line = f"http {ip_address} {port}"
    formatted_lines.append(formatted_line)

with open("http_formatted.txt", "w") as f:
    for line in formatted_lines:
        f.write(line + "\n")

# Concatenate the contents of socks4_formatted.txt to the end of proxy.txt
result = subprocess.run(["cat", "socks4_formatted.txt"],
                        stdout=subprocess.PIPE, encoding="utf-8")

with open("proxySocks4.conf", "a") as f:
    f.write(result.stdout)

# Concatenate the contents of socks4_formatted.txt to the end of proxy.txt
result = subprocess.run(["cat", "http_formatted.txt"],
                        stdout=subprocess.PIPE, encoding="utf-8")

with open("proxyHttp.conf", "a") as f:
    f.write(result.stdout)


# The new lines to be inserted at the top of the file
new_lines = [
    "[ProxyList] \n",
    "tcp_connect_timeout 10000 \n",
    "tcp_read_timeout 18000 \n",
    "remote_dns_subnet 224 \n",
    "#strict_chain = 1 \n",
    "#dynamic_chain \n",
    "proxy_dns \n",
    "random_chain \n",
]

# Open the file in read mode
with open("proxyHttp.conf", "r") as f:
    # Read the contents of the file into a list of lines
    lines = f.readlines()

# Insert the new lines as the first elements in the list
for new_line in new_lines:
    lines.insert(0, new_line)

# Open the file in write mode
with open("proxyHttp.conf", "w") as f:
    # Write the modified list of lines back to the file
    for line in lines:
        f.write(line)

# Open the file in read mode
with open("proxySocks4.conf", "r") as f:
    # Read the contents of the file into a list of lines
    lines = f.readlines()

# Insert the new lines as the first elements in the list
for new_line in new_lines:
    lines.insert(0, new_line)

# Open the file in write mode
with open("proxySocks4.conf", "w") as f:
    # Write the modified list of lines back to the file
    for line in lines:
        f.write(line)


# Delete the socks4.txt file
try:
    os.remove("socks4.txt")
except FileNotFoundError:
    pass

# Delete the http.txt file
try:
    os.remove("http.txt")
except FileNotFoundError:
    pass

# Delete the socks4_formatted.txt file
try:
    os.remove("socks4_formatted.txt")
except FileNotFoundError:
    pass

# Delete the http_formatted.txt file
try:
    os.remove("http_formatted.txt")
except FileNotFoundError:
    pass

output_directory = input("Output directory for config files: \n")

# Sleep timer to make sure it's finished running before it moves them
time.sleep(5)
subprocess.run(['mv', 'proxySocks4.conf', f"{output_directory}/proxySocks4.conf"])
subprocess.run(['mv', 'proxyHttp.conf', f"{output_directory}/proxyHttp.conf"])

text = pyfiglet.figlet_format("Finished \n Example: proxychains4 -f proxySocks4.conf curl http://googles.evil", 
font="small")
print(text)