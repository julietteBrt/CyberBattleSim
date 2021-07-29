import subprocess, ctypes, os, sys
from subprocess import Popen, DEVNULL

def check_admin():
    """ Force to start application with admin rights """
    try:
        isAdmin = ctypes.windll.shell32.IsUserAnAdmin()
    except AttributeError:
        isAdmin = False
    if not isAdmin:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

def add_rule(rule_name, file_path):
    """ Add rule to Windows Firewall """
    subprocess.call(
        f"netsh advfirewall firewall add rule name={rule_name} dir=out action=block enable=no program={file_path}", 
        shell=True, 
        stdout=DEVNULL, 
        stderr=DEVNULL
    )
    print(f"Rule {rule_name} for {file_path} added")

def modify_rule(rule_name, enabled=True):
    """Enable or Disable a specific rule"""
    subprocess.run(
        [
            'netsh', 'advfirewall', 'firewall',
            'set', 'rule', f'name={rule_name}',
            'new', f'enable={"yes" if enabled else "no"}',
        ],
        check=True,
        stdout=DEVNULL,
        stderr=DEVNULL
    )
    print(f"Rule {rule_name} {message}")

if __name__ == '__main__':
    check_admin()
    add_rule("RULE_NAME", "PATH_TO_FILE")
    modify_rule("RULE_NAME", 1)