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
    else:
        log_passed(cmd)

print("\n\n\n")
print("Running factory module tests...")
run(["python", "-m", "dsp_bp_generator.factory_generator.factory_block"])
run(["python", "-m", "dsp_bp_generator.factory_generator.factory_line"])
run(["python", "-m", "dsp_bp_generator.factory_generator.factory_router"])
run(["python", "-m", "dsp_bp_generator.factory_generator.factory_section"])
run(["python", "-m", "dsp_bp_generator.factory_generator.factory"])

#print("Running other tests...")
#run(["python3", "examples/buildings.py"])
#run(["python3", "examples/generate_factory.py"])
#run(["python3", "examples/oil_refinary.py"])
#run(["python3", "examples/parse_edit_and_serialize.py", "--if=input.bp"])
#run(["python3", "examples/parse.py", "--if=input.bp"])
#run(["python3", "examples/sorter_example.py"])
