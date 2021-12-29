from collections import defaultdict
import itertools            #complex iterators

###################################################### lists ###########################################################
from typing import Union, List, Any

input_vector = []
primary_input_pins = []
primary_output_pins = []
output_vector = []
logic_values = []

##################################################### Dictionary #########################################################
nodes_dict = {}
node_num = 0

################################## Reading all sets of input in input_vector list ######################################

if __name__ == '__main__':
    # Reading inputvector
    f1 = open('inputvector.txt', 'r')
    while (1):
        node_num = 0
        input_file = f1.readline()
        line = input_file.strip()
        input_vector = line.split()
        if not input_vector:
            break
        print("Input vector is:", input_vector)

################################ Reading netlist file to identify primary i/p o/p nodes ################################

        f2 = open('Netlist.txt','r')
        num_gates = 0
        num_outputs = 0
        for data in f2:
            data = data.strip()         
            node_data = data.split()    
            ######################################### INPUT pins #######################################################
            if node_data[0] == 'INPUT':
                i = 0
                primary_input_pins = node_data[1:-1]
                print("Primary input pins are:",primary_input_pins)
                if(len(primary_input_pins) != len(input_vector)):
                    print("Input vector length does not match!")
                    exit()
                ############################ Adding i/p pins to dictionary #############################################
                else:
                    while(1):
                        node_num = node_data[1 + i]
                        nodes_dict[node_num] = {}
                        nodes_dict[node_num]['Gate Type'] = "INPUT"
                        nodes_dict[node_num]['num_inp'] = -1
                        nodes_dict[node_num]['num_out'] = -1
                        nodes_dict[node_num]['inputs'] = ""
                        nodes_dict[node_num]['outputs'] = ""
                        nodes_dict[node_num]['level'] = 0
                        nodes_dict[node_num]['value'] = input_vector[i]
                        nodes_dict[node_num]['done'] = 1
                        i = i + 1
                        if(i >= len(primary_input_pins)):
                            break

            ######################################### OUTPUT pins #######################################################
            elif node_data[0] == 'OUTPUT':
                num_outputs = num_outputs + 1
                i = 1
                while(node_data[i] != '-1'):
                    primary_output_pins.append(node_data[i])
                    node_num = node_data[i]
                    i += 1
                print("Primary output pins:",primary_output_pins)

            ######################################### Other nodes #####################################################
            else:
                num_gates = num_gates + 1
                ################################# Adding other nodes in dictionary #####################################
                k = 0
                while(k < num_gates):
                    node_num = node_data[-1]
                    nodes_dict[node_num] = {}
                    nodes_dict[node_num]['Gate Type'] = node_data[0]
                    nodes_dict[node_num]['num_inp'] = len(node_data[1:-1])
                    nodes_dict[node_num]['num_out'] = 1
                    nodes_dict[node_num]['inputs'] = [node_data[1], node_data[2]]
                    nodes_dict[node_num]['outputs'] = [node_data[-1]]
                    if nodes_dict[node_num]['num_inp'] == 1:
                        nodes_dict[node_num]['level'] = 1 + int(nodes_dict[nodes_dict[node_num]['inputs'][0]]['level'])
                    else:
                        nodes_dict[node_num]['level'] = 1 + max(
                            int(nodes_dict[nodes_dict[node_num]['inputs'][0]]['level']),
                            int(nodes_dict[nodes_dict[node_num]['inputs'][1]]['level']))
                    nodes_dict[node_num]['value'] = 'x'
                    nodes_dict[node_num]['done'] = 0
                    k = k + 1

        f2.close()
        x = num_outputs + num_gates + len(input_vector)
        
        ############################################## Simulation ######################################################
        logic_values = [0] * x

        f3 = open('Netlist.txt', 'r')
        nets_done = primary_input_pins
        for gates in f3:
            gates = gates.strip();
            gates_data = gates.split();
            net_indices = []
            net_indices_str = []

            if (gates_data[0] == 'INPUT' or gates_data[0] == 'OUTPUT'):
                pass
            else:
                net_indices_str = gates_data[1:]
                net_indices = list(map(int, net_indices_str))

            if gates_data[0] == 'INV':
                if (gates_data[1] in nets_done):
                    if nodes_dict[str(gates_data[1])]['value'] == '1':
                        nodes_dict[str(gates_data[2])]['value'] = '0'
                    elif nodes_dict[str(gates_data[1])]['value'] == '0':
                        nodes_dict[str(gates_data[2])]['value'] = '1'
                    elif nodes_dict[str(gates_data[1])]['value'] == 'D':
                        nodes_dict[str(gates_data[2])]['value'] = 'Dbar'
                    elif nodes_dict[str(gates_data[1])]['value'] == 'Dbar':
                        nodes_dict[str(gates_data[2])]['value'] = 'D'
                    else:
                        nodes_dict[str(gates_data[2])]['value'] = 'x'

                    nodes_dict[str(gates_data[2])]['done'] = '1'
                    nets_done.append(gates_data[2])

            if gates_data[0] == 'XOR':
                if (gates_data[1] in nets_done) and (gates_data[2] in nets_done):
                    if nodes_dict[str(gates_data[1])]['value'] == '0':
                        nodes_dict[str(gates_data[3])]['value'] =  nodes_dict[str(gates_data[2])]['value']
                    elif nodes_dict[str(gates_data[1])]['value'] == 'x':
                        nodes_dict[str(gates_data[3])]['value'] = 'x'
                    else:
                        if nodes_dict[str(gates_data[2])]['value'] == 'x':
                            nodes_dict[str(gates_data[3])]['value'] = 'x'
                        else:
                            nodes_dict[str(gates_data[3])]['value'] =int( not int(nodes_dict[str(gates_data[2])]['value']))

                    nodes_dict[str(gates_data[3])]['done'] = '1'
                    nets_done.append(gates_data[3])

            if gates_data[0] == 'XNOR':
                if (gates_data[1] in nets_done) and (gates_data[2] in nets_done):
                    if nodes_dict[str(gates_data[1])]['value'] == '0':
                        nodes_dict[str(gates_data[3])]['value'] =  nodes_dict[str(gates_data[2])]['value']
                    elif nodes_dict[str(gates_data[1])]['value'] == 'x':
                        nodes_dict[str(gates_data[3])]['value'] = 'x'
                    else:
                        if nodes_dict[str(gates_data[2])]['value'] == 'x':
                            nodes_dict[str(gates_data[3])]['value'] = 'x'
                        else:
                            nodes_dict[str(gates_data[3])]['value'] =int( not int(nodes_dict[str(gates_data[2])]['value']))

                    if nodes_dict[str(gates_data[3])]['value'] == 'x' :
                        pass
                    else:
                        if nodes_dict[str(gates_data[3])]['value']== '0':
                            nodes_dict[str(gates_data[3])]['value']='1'
                        else:
                            nodes_dict[str(gates_data[3])]['value'] = '0'

                    nodes_dict[str(gates_data[3])]['done'] = '1'
                    nets_done.append(gates_data[3])

            if gates_data[0] == 'AND':
                 if (gates_data[1] in nets_done) and (gates_data[2] in nets_done):
                     if nodes_dict[str(gates_data[1])]['value'] == '1':
                         nodes_dict[str(gates_data[3])]['value'] = nodes_dict[str(gates_data[2])]['value']
                     elif nodes_dict[str(gates_data[1])]['value'] == '0':
                         nodes_dict[str(gates_data[3])]['value'] = '0'
                     elif nodes_dict[str(gates_data[1])]['value'] == 'D':
                         if nodes_dict[str(gates_data[2])]['value'] == '0':
                             nodes_dict[str(gates_data[3])]['value'] = '0'
                         elif nodes_dict[str(gates_data[2])]['value'] == 'x':
                            nodes_dict[str(gates_data[3])]['value'] = 'x'
                         else:
                            nodes_dict[str(gates_data[3])]['value'] = 'D'
                     elif nodes_dict[str(gates_data[1])]['value'] == 'Dbar':
                         if nodes_dict[str(gates_data[2])]['value'] == '0':
                            nodes_dict[str(gates_data[3])]['value'] = '0'
                         elif nodes_dict[str(gates_data[2])]['value'] == 'x':
                            nodes_dict[str(gates_data[3])]['value'] = 'x'
                         else:
                            nodes_dict[str(gates_data[3])]['value'] = 'Dbar'
                     elif nodes_dict[str(gates_data[2])]['value'] == '0':
                          nodes_dict[str(gates_data[3])]['value'] = '0'
                     else:
                         nodes_dict[str(gates_data[3])]['value'] = 'x'
                     nodes_dict[str(gates_data[3])]['done'] = '1'
                     nets_done.append(gates_data[3])

            if gates_data[0] == 'NAND':
                if (gates_data[1] in nets_done) and (gates_data[2] in nets_done):
                    if nodes_dict[str(gates_data[1])]['value'] == '1':
                        nodes_dict[str(gates_data[3])]['value'] = nodes_dict[str(gates_data[2])]['value']
                    elif nodes_dict[str(gates_data[1])]['value'] == '0':
                        nodes_dict[str(gates_data[3])]['value'] = '0'
                    elif nodes_dict[str(gates_data[1])]['value'] == 'D':
                        if nodes_dict[str(gates_data[2])]['value'] == '0':
                            nodes_dict[str(gates_data[3])]['value'] = '0'
                        elif nodes_dict[str(gates_data[2])]['value'] == 'x':
                            nodes_dict[str(gates_data[3])]['value'] = 'x'
                        else:
                            nodes_dict[str(gates_data[3])]['value'] = 'D'
                    elif nodes_dict[str(gates_data[1])]['value'] == 'Dbar':
                        if nodes_dict[str(gates_data[2])]['value'] == '0':
                            nodes_dict[str(gates_data[3])]['value'] = '0'
                        elif nodes_dict[str(gates_data[2])]['value'] == 'x':
                            nodes_dict[str(gates_data[3])]['value'] = 'x'
                        else:
                            nodes_dict[str(gates_data[3])]['value'] = 'Dbar'
                    elif nodes_dict[str(gates_data[2])]['value'] == '0':
                        nodes_dict[str(gates_data[3])]['value'] = '0'
                    else:
                        nodes_dict[str(gates_data[3])]['value'] = 'x'
                    if nodes_dict[str(gates_data[3])]['value'] == 'x' :
                        pass
                    elif nodes_dict[str(gates_data[3])]['value'] == 'D' :
                        nodes_dict[str(gates_data[3])]['value'] = 'Dbar'
                    elif nodes_dict[str(gates_data[3])]['value'] == 'Dbar' :
                        nodes_dict[str(gates_data[3])]['value'] = 'D'
                    else:
                        if nodes_dict[str(gates_data[3])]['value']== '0':
                            nodes_dict[str(gates_data[3])]['value']='1'
                        else:
                            nodes_dict[str(gates_data[3])]['value'] = '0'
                    nodes_dict[str(gates_data[3])]['done'] = '1'
                    nets_done.append(gates_data[3])


            if gates_data[0] == 'OR':
                if (gates_data[1] in nets_done) and (gates_data[2] in nets_done):
                    if nodes_dict[str(gates_data[1])]['value'] == '0':
                        nodes_dict[str(gates_data[3])]['value'] = nodes_dict[str(gates_data[2])]['value']
                    elif nodes_dict[str(gates_data[1])]['value'] == '1':
                        nodes_dict[str(gates_data[3])]['value'] = '1'
                    elif (nodes_dict[str(gates_data[1])]['value'] == 'D') or (
                            nodes_dict[str(gates_data[1])]['value'] == 'Dbar'):
                        if nodes_dict[str(gates_data[2])]['value'] == '0':
                            nodes_dict[str(gates_data[3])]['value'] = nodes_dict[str(gates_data[1])]['value']
                        else:
                            nodes_dict[str(gates_data[3])]['value'] = nodes_dict[str(gates_data[2])]['value']
                    elif nodes_dict[str(gates_data[2])]['value'] == '1':
                        nodes_dict[str(gates_data[3])]['value'] = '1'
                    else:
                        nodes_dict[str(gates_data[3])]['value'] = 'x'

                    nodes_dict[str(gates_data[3])]['done'] = '1'
                    nets_done.append(gates_data[3])

            if gates_data[0] == 'NOR':
                if (gates_data[1] in nets_done) and (gates_data[2] in nets_done):
                    if nodes_dict[str(gates_data[1])]['value'] == '0':
                        nodes_dict[str(gates_data[3])]['value'] = nodes_dict[str(gates_data[2])]['value']
                    elif nodes_dict[str(gates_data[1])]['value'] == '1':
                        nodes_dict[str(gates_data[3])]['value'] = '1'
                    elif (nodes_dict[str(gates_data[1])]['value'] == 'D') or (
                            nodes_dict[str(gates_data[1])]['value'] == 'Dbar'):
                        if nodes_dict[str(gates_data[2])]['value'] == '0':
                            nodes_dict[str(gates_data[3])]['value'] = nodes_dict[str(gates_data[1])]['value']
                        else:
                            nodes_dict[str(gates_data[3])]['value'] = nodes_dict[str(gates_data[2])]['value']
                    elif nodes_dict[str(gates_data[2])]['value'] == '1':
                        nodes_dict[str(gates_data[3])]['value'] = '1'
                    else:
                        nodes_dict[str(gates_data[3])]['value'] = 'x'

                    if nodes_dict[str(gates_data[3])]['value'] == 'x':
                        pass
                    elif nodes_dict[str(gates_data[3])]['value'] == 'D':
                        nodes_dict[str(gates_data[3])]['value'] = 'Dbar'
                    elif nodes_dict[str(gates_data[3])]['value'] == 'Dbar':
                        nodes_dict[str(gates_data[3])]['value'] = 'D'
                    else:
                        if nodes_dict[str(gates_data[3])]['value'] == '0':
                            nodes_dict[str(gates_data[3])]['value'] = '1'
                        else:
                            nodes_dict[str(gates_data[3])]['value'] = '0'
                    nodes_dict[str(gates_data[3])]['done'] = '1'
                    nets_done.append(gates_data[3])

        nets_done_sorted = []
        nets_done_sorted = [int(i) for i in nets_done]
        nets_done_sorted.sort()
        j = 0
        print("Final logic values:", end=" ")
        for j in nets_done:
            print(j, ":", nodes_dict[j]['value'], "    ", end=" ")
        print(" ")

        i = 0
        print("Output logic values:")
        while( i < num_outputs + 1):
            print(str(nodes_dict[str(primary_output_pins[i])]['value']))
            i += 1
        print("Dictionary final:", nodes_dict)
    f1.close()
