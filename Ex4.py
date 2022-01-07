import subprocess
import sys

from client_python.student_code import main
if len(sys.argv) > 1:
    try:
        subprocess.Popen(["powershell.exe", "java -jar Ex4_Server_v0.0.jar", sys.argv[1]])
    except("ERR"):
        print("The server is already running")
else:
    try:
        subprocess.Popen(["powershell.exe", "java -jar Ex4_Server_v0.0.jar 11"])
    except("ERR"):
        print("The server is already running")
main()
