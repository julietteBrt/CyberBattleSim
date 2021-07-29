#!/usr/bin/env python

from pyptables import default_tables, restore
from pyptables.rules import Rule, Accept, Reject, Drop, CompositeRule
import subprocess

# get a default set of tables and chains
tables = default_tables()

def append_rule_to_chain_table(target, chain, protocol, source = None, port = None, table = 'filter'):
    table = tables[table][chain]
    try:
        if(target == 'Accept'):
            if(port):
                table.append(Accept(proto = protocol, dport = port))
            elif(source):
                table.append(Accept(s = source))
        elif(target == 'Reject'):
            if(port):
                table.append(Reject(proto = protocol, dport = port))
            elif(source):
                table.append(Reject(s = source))
        elif(target == 'Drop'):
            if(port):
                table.append(Drop(proto = protocol, dport = port))
            elif(source):
                table.append(Drop(s = source))
        else:
            return False
    except:
        return False
    restore(tables)
    return tables.to_iptables()


print(append_rule_to_chain_table('Reject', 'FORWARD', 'tcp', source = '1.1.2.1', port = None, table = 'filter'))

service = "mysql"

def get_service_status(service):
    running = False
    output, err = subprocess.Popen(["sudo", "service", service, "status"], stdout=subprocess.PIPE).communicate()
    output = output.decode('utf-8')
    if(err):
        return err.decode('utf-8')
    elif('stopped' not in output):
        running = True
    return output, running

def start_service(service):
    out, running = get_service_status(service)
    if (not running):
        output, err = subprocess.Popen(["sudo", "service", service, "start"], stdout=subprocess.PIPE).communicate()
        if(err):
            return err.decode('utf-8')
        return output.decode('utf-8')
    else:
        return out

def stop_service(service):
    #assert 'stopped' not in get_service_status(service), f'Cannot stop {service}, it is not running.'
    out, running = get_service_status(service)
    if(running):
        output, err = subprocess.Popen(["sudo", "service", service, "stop"], stdout=subprocess.PIPE).communicate()
        if(err):
            return err.decode('utf-8')
        return output.decode('utf-8')
    else:
        return out
