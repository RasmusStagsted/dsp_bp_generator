import subprocess
from colorama import Fore, Style

def log_passed(cmd):
    mes = Fore.GREEN + "Passed" + Style.RESET_ALL + ":"
    for word in cmd:
        mes += " " + word
    print(mes)
    
def log_failed(cmd):
    mes = Fore.RED + "Failed" + Style.RESET_ALL + ":"
    for word in cmd:
        mes += " " + word
    print(mes)
    
def run(cmd):
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode != 0:
        log_failed(cmd)
    else:
        log_passed(cmd)

run(["python3", "parse.py", "--if=input.bp"])
run(["python3", "parse_edit_and_serialize.py", "--if=input.bp"])
run(["python3", "generate_and_serialize.py"])
run(["python3", "generate_factory.py"])
