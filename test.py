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
    
def run(cmd, enable_output = False):
    if enable_output:
        result = subprocess.run(cmd)
    else:
        result = subprocess.run(cmd, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    if result.returncode != 0:
        log_failed(cmd)
        return False
    else:
        log_passed(cmd)
        return True

print("\n\n\n")
print("Running factory module tests...")
success = True
success = success and run(["python", "-m", "dsp_bp_generator.factory_generator.factory_block"])
success = success and run(["python", "-m", "dsp_bp_generator.factory_generator.factory_line"])
success = success and run(["python", "-m", "dsp_bp_generator.factory_generator.factory_router"])
success = success and run(["python", "-m", "dsp_bp_generator.factory_generator.factory_section"])
success = success and run(["python", "-m", "dsp_bp_generator.factory_generator.factory"])

if success:
    exit(0)
else:
    exit(1)
#print("Running other tests...")
#run(["python3", "examples/buildings.py"])
#run(["python3", "examples/generate_factory.py"])
#run(["python3", "examples/oil_refinary.py"])
#run(["python3", "examples/parse_edit_and_serialize.py", "--if=input.bp"])
#run(["python3", "examples/parse.py", "--if=input.bp"])
#run(["python3", "examples/sorter_example.py"])
