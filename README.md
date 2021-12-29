**Logic_Simulator**

This is 5-valued Logic Simulator for digital circuits implemented in python. 
5 values are: (0, 1, X, D, Dbar)

Note: D and Dbar represents stuck at 0 and stuck at 1 fault respectively.

Netlist and inputvector need to be provided as input text file and based on the circuit described(in netlist) and inputvector provided, logic simulator will generate output value at the output nodes.

Sample Netlist and inputvector file is added.

**Netlist:**

![image](https://user-images.githubusercontent.com/96716544/147666551-ddd75cef-1f80-408b-96e8-c3dcc8ea6f9c.png)

Here, first and last line indicates input and output node number.
Second line describes NOR gate with input at node 1 and 4, output as node 7. Similarly, other lines can be interpreted. 

**Inputvector:**

![image](https://user-images.githubusercontent.com/96716544/147666854-aeeba66b-e270-44cc-9aae-8a0f33489263.png)

**Output for above netlist and inputvector:**

![image](https://user-images.githubusercontent.com/96716544/147666398-067aa38c-7321-4af6-88fc-43eb5fb5a9ae.png)

Final logic value lists value at each node in the circuit for given input.

Dictionary is a collection of nodes in the circuit. It has all information about that nodes - node number, it's gate type, how many inputs/outputs are connected to that gate and input/output node number, level of gate in circuit, value at it's output and whether gate is evaluated or not in the simulation is taken care by the done flag.
