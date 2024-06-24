from iic2343 import Basys3
import os
import sys
from typing import Union

data = []
code = []
jump_labels = {}
is_data_section = True
pc = 1
# ----------- Inicio de declaracion de funciones auxiliares ------------------
def decimal_a_binario_16bits(valor):
    if not (-32768 <= valor <= 32767):
        raise ValueError("El valor debe estar en el rango de -32768 a 32767 para un entero de 16 bits con signo.")
    if valor < 0:
        valor = valor + (1 << 16)
    binario = bin(valor)[2:]
    binario_16bits = binario.zfill(16)
    return binario_16bits

def parse_code_section(line, pc, instrucciones, jump_labels, data):
    line = line.replace(' ', '')
    line= line.strip('\n')
    ins = []
    add = True
    if 'MOV' in line:
        line = line[3:]
        ins.append('MOV')
        line = line.split(',')
        value = decimal_a_binario_16bits(0)
        for i in range (0, len(line)):
            if 'A' not in line[i] and 'B' not in line[i] and '(' not in line[i]:
                try: 
                    value = decimal_a_binario_16bits(int(line[i]))
                except ValueError:
                    value = decimal_a_binario_16bits(data[line[i]])
                line[i] = 'LIT'
            elif '(' in line[i] and '(B)' != line[i]:
                value = line[i].strip('()')
                try:
                    value = decimal_a_binario_16bits(int(value))
                except ValueError:
                    value = decimal_a_binario_16bits(data[value])
                line[i] = 'MEM'           
        ins.append(line)
        ins.append(value)
        pc += 1
        ins.append(pc)
    elif 'ADD' in line:
        pc += 1
        line = line[3:]
        ins.append('ADD')
        line = line.split(',')
        value = decimal_a_binario_16bits(0)
        for i in range (0, len(line)):
            if 'A' not in line[i] and 'B' not in line[i] and '(' not in line[i]:
                try: 
                    value = decimal_a_binario_16bits(int(line[i]))
                except ValueError:
                    value = decimal_a_binario_16bits(data[line[i]])
                line[i] = 'LIT'
            elif '(' in line[i] and '(B)' != line[i]:
                value = line[i].strip('()')
                try:
                    value = decimal_a_binario_16bits(int(value))
                except ValueError:
                    value = decimal_a_binario_16bits(data[value])
                line[i] = 'MEM'
        ins.append(line)
        ins.append(value)           
        ins.append(pc)
    elif 'SUB' in line:
        pc += 1
        line = line[3:]
        ins.append('SUB')
        line = line.split(',')
        value = decimal_a_binario_16bits(0)
        for i in range (0, len(line)):
            if 'A' not in line[i] and 'B' not in line[i] and '(' not in line[i]:
                try: 
                    value = decimal_a_binario_16bits(int(line[i]))
                except ValueError:
                    value = decimal_a_binario_16bits(data[line[i]])
                line[i] = 'LIT'
            elif '(' in line[i] and '(B)' != line[i]:
                value = line[i].strip('()')
                try:
                    value = decimal_a_binario_16bits(int(value))
                except ValueError:
                    value = decimal_a_binario_16bits(data[value])
                line[i] = 'MEM'           
        ins.append(line)
        ins.append(value)
        ins.append(pc)
    elif 'AND' in line:
        pc += 1
        line = line[3:]
        ins.append('AND')
        line = line.split(',')
        value = decimal_a_binario_16bits(0)
        for i in range (0, len(line)):
            if 'A' not in line[i] and 'B' not in line[i] and '(' not in line[i]:
                try: 
                    value = decimal_a_binario_16bits(int(line[i]))
                except ValueError:
                    value = decimal_a_binario_16bits(data[line[i]])
                line[i] = 'LIT'
            elif '(' in line[i] and '(B)' != line[i]:
                value = line[i].strip('()')
                try:
                    value = decimal_a_binario_16bits(int(value))
                except ValueError:
                    value = decimal_a_binario_16bits(data[value])
                line[i] = 'MEM'           
        ins.append(line)
        ins.append(value)
        ins.append(pc)
    elif 'OR' in line and 'XOR' not in line:
        pc += 1
        line = line[2:]
        ins.append('OR')
        line = line.split(',')
        value = decimal_a_binario_16bits(0)
        for i in range (0, len(line)):
            if 'A' not in line[i] and 'B' not in line[i] and '(' not in line[i]:
                try: 
                    value = decimal_a_binario_16bits(int(line[i]))
                except ValueError:
                    value = decimal_a_binario_16bits(data[line[i]])
                line[i] = 'LIT'
            elif '(' in line[i] and '(B)' != line[i]:
                value = line[i].strip('()')
                try:
                    value = decimal_a_binario_16bits(int(value))
                except ValueError:
                    value = decimal_a_binario_16bits(data[value])
                line[i] = 'MEM'           
        ins.append(line)
        ins.append(value)
        ins.append(pc)
    elif 'XOR' in line:
        pc += 1
        line = line[3:]
        ins.append('XOR')
        line = line.split(',')
        value = decimal_a_binario_16bits(0)
        for i in range (0, len(line)):
            if 'A' not in line[i] and 'B' not in line[i] and '(' not in line[i]:
                try: 
                    value = decimal_a_binario_16bits(int(line[i]))
                except ValueError:
                    value = decimal_a_binario_16bits(data[line[i]])
                line[i] = 'LIT'
            elif '(' in line[i] and '(B)' != line[i]:
                value = line[i].strip('()')
                try:
                    value = decimal_a_binario_16bits(int(value))
                except ValueError:
                    value = decimal_a_binario_16bits(data[value])
                line[i] = 'MEM'           
        ins.append(line)
        ins.append(value)
        ins.append(pc)
    elif 'NOT' in line:
        pc += 1
        line = line[3:]
        ins.append('NOT')
        line = line.split(',')
        value = decimal_a_binario_16bits(0)
        for i in range (0, len(line)):
            if 'A' not in line[i] and 'B' not in line[i] and '(' not in line[i]:
                value = decimal_a_binario_16bits(int(line[i]))
                line[i] = 'LIT'
            elif '(' in line[i] and '(B)' != line[i]:
                value = line[i].strip('()')
                try:
                    value = decimal_a_binario_16bits(int(value))
                except ValueError:
                    value = decimal_a_binario_16bits(data[value])
                line[i] = 'MEM'           
        ins.append(line)
        ins.append(value)
        ins.append(pc)
    elif 'SHL' in line:
        pc += 1
        line = line[3:]
        ins.append('SHL')
        line = line.split(',')
        value = decimal_a_binario_16bits(0)
        for i in range (0, len(line)):
            if 'A' not in line[i] and 'B' not in line[i] and '(' not in line[i]:
                value = decimal_a_binario_16bits(int(line[i]))
                line[i] = 'LIT'
            elif '(' in line[i] and '(B)' != line[i]:
                value = line[i].strip('()')
                try:
                    value = decimal_a_binario_16bits(int(value))
                except ValueError:
                    value = decimal_a_binario_16bits(data[value])
                line[i] = 'MEM'           
        ins.append(line)
        ins.append(value)
        ins.append(pc)
    elif 'SHR' in line:
        pc += 1
        line = line[3:]
        ins.append('SHR')
        line = line.split(',')
        value = decimal_a_binario_16bits(0)
        for i in range (0, len(line)):
            if 'A' not in line[i] and 'B' not in line[i] and '(' not in line[i]:
                value = decimal_a_binario_16bits(int(line[i]))
                line[i] = 'LIT'
            elif '(' in line[i] and '(B)' != line[i]:
                value = line[i].strip('()')
                try:
                    value = decimal_a_binario_16bits(int(value))
                except ValueError:
                    value = decimal_a_binario_16bits(data[value])
                line[i] = 'MEM'           
        ins.append(line)
        ins.append(value)
        ins.append(pc)
    elif 'INC' in line:
        pc += 1
        line = line[3:]
        ins.append('INC')
        line = line.split(',')
        value = decimal_a_binario_16bits(0)
        for i in range (0, len(line)):
            if 'A' in line[i]:
                value = decimal_a_binario_16bits(1)
            elif 'A' not in line[i] and 'B' not in line[i] and '(' not in line[i]:
                value = decimal_a_binario_16bits(int(line[i]))
                line[i] = 'LIT'
            elif '(' in line[i] and '(B)' != line[i]:
                value = line[i].strip('()')
                try:
                    value = decimal_a_binario_16bits(int(value))
                except ValueError:
                    value = decimal_a_binario_16bits(data[value])
                line[i] = 'MEM'           
        ins.append(line)
        ins.append(value)
        ins.append(pc)
    elif 'DEC' in line:
        pc += 1
        ins.append('DEC')
        ins.append(['A'])
        ins.append(decimal_a_binario_16bits(1))
        ins.append(pc)
    elif 'CMP' in line:
        pc += 1
        line = line[3:]
        ins.append('CMP')
        line = line.split(',')
        value = decimal_a_binario_16bits(0)
        for i in range (0, len(line)):
            if 'A' not in line[i] and 'B' not in line[i] and '(' not in line[i]:
                try: 
                    value = decimal_a_binario_16bits(int(line[i]))
                except ValueError:
                    value = decimal_a_binario_16bits(data[line[i]])
                line[i] = 'LIT'
            elif '(' in line[i] and '(B)' != line[i]:
                value = line[i].strip('()')
                try:
                    value = decimal_a_binario_16bits(int(value))
                except ValueError:
                    value = decimal_a_binario_16bits(data[value])
                line[i] = 'MEM'           
        ins.append(line)
        ins.append(value)
        ins.append(pc)
    elif 'JMP' in line:
        pc += 1
        line = line[3:]
        ins.append('JMP')
        ins.append([line])
        ins.append(pc)
    elif 'JEQ' in line:
        pc += 1
        line = line[3:]
        ins.append('JEQ')
        ins.append([line])
        ins.append(pc)
    elif 'JNE' in line:
        pc += 1
        line = line[3:]
        ins.append('JNE')
        ins.append([line])
        ins.append(pc)
    elif 'JGT' in line:
        pc += 1
        line = line[3:]
        ins.append('JGT')
        ins.append([line])
        ins.append(pc)
    elif 'JGE' in line:
        pc += 1
        line = line[3:]
        ins.append('JGE')
        ins.append([line])
        ins.append(pc)
    elif 'JLT' in line:
        pc += 1
        line = line[3:]
        ins.append('JLT')
        ins.append([line])
        ins.append(pc)
    elif 'JLE' in line:
        pc += 1
        line = line[3:]
        ins.append('JLE')
        ins.append([line])
        ins.append(pc)
    elif 'JCR' in line:
        pc += 1
        line = line[3:]
        ins.append('JCR')
        ins.append([line])
        ins.append(pc)
    elif 'NOP' in line:
        pc += 1
        ins.append('NOP')
        ins.append([])
        ins.append(decimal_a_binario_16bits(0))
        ins.append(pc)
    elif 'PUSH' in line:
        pc += 1
        line = line[4:]
        ins.append('PUSH')
        ins.append([line])
        ins.append(decimal_a_binario_16bits(0))
        ins.append(pc)
    elif 'POP' in line:
        pc += 1
        line = line[3:]
        ins.append('POP')
        ins.append([line])
        ins.append(decimal_a_binario_16bits(0))
        ins.append(pc)
        pc += 1
    elif 'CALL' in line:
        pc += 1
        line = line[4:]
        ins.append('CALL')
        ins.append([line])
        ins.append(pc)
    elif 'RET' in line:
        pc += 1
        ins.append('RET')
        ins.append([])
        ins.append(decimal_a_binario_16bits(0))
        ins.append(pc)
        pc += 1
    elif line != '':
        jump_labels[line[:len(line)-1]] = pc+1
        add = False
    else:
        add = False
    if add:
        instrucciones.append(ins)
    return pc

def concat(dict:dict)->dict: # esto entrega el opcode
    concat_values = ''.join(map(str, dict.values()))
    return concat_values

def reset(dict:dict)->dict:
    for key in dict:
        dict[key] = 0

def build_opcode(ins, args, signals):
    if len(args) > 1:
        first = args[0]
        second = args[1]
    elif len(args) == 1:
        first = args[0]
        second = None
    else:
        first = None
        second = None

    if ins == "MOV":
        if first == 'A' and second == 'B':
            signals['sel_Add0'] = 1
            signals['enA'] = 1
            signals['selB0'] = 1
        elif first == 'B' and second == 'A':
            signals['sel_Add0'] = 1
            signals['enB'] = 1
            signals['selA1'] = 1
        elif first == 'A' and second == 'LIT':
            signals['sel_Add0'] = 1
            signals['enA'] = 1
            signals['selB1'] = 1
            signals['selB0'] = 1
        elif first == 'B' and second == 'LIT':
            signals['sel_Add0'] = 1
            signals['enB'] = 1
            signals['selB1'] = 1
            signals['selB0'] = 1
        elif first == 'A' and second == 'MEM':
            signals['sel_Add0'] = 1
            signals['enA'] = 1
            signals['selB1'] = 1
        elif first == 'B' and second == 'MEM':
            signals['sel_Add0'] = 1
            signals['enB'] = 1
            signals['selB1'] = 1
        elif first == 'MEM' and second == 'A':
            signals['sel_Add0'] = 1
            signals['selA1'] = 1
            signals['w'] = 1
        elif first == 'MEM' and second == 'B':
            signals['sel_Add0'] = 1
            signals['selB0'] = 1
            signals['w'] = 1
        elif first == 'A' and second == '(B)':
            signals['sel_Add1'] = 1
            signals['enA'] = 1
            signals['selB1'] = 1
        elif first == 'B' and second == '(B)':
            signals['sel_Add1'] = 1
            signals['enB'] = 1
            signals['selB1'] = 1
        elif first == '(B)' and second == 'A':
            signals['sel_Add1'] = 1
            signals['selA1'] = 1
            signals['w'] = 1
        elif first == '(B)' and second == 'LIT':
            signals['sel_Add1'] = 1
            signals['selB1'] = 1
            signals['selB0'] = 1
            signals['w'] = 1
        return(concat(signals))

    elif ins == "ADD":
        if first == 'A' and second == 'B':
            signals['sel_Add0'] = 1
            signals['enA'] = 1
            signals['selA1'] = 1
            signals['selB0'] = 1
        elif first == 'B' and second == 'A':
            signals['sel_Add0'] = 1
            signals['enB'] = 1
            signals['selA1'] = 1
            signals['selB0'] = 1
        elif first == 'A' and second == 'LIT':
            signals['sel_Add0'] = 1
            signals['enA'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
            signals['selB0'] = 1
        elif first == 'B' and second == 'LIT':
            signals['sel_Add0'] = 1
            signals['enB'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
            signals['selB0'] = 1
        elif first == 'A' and second == 'MEM':
            signals['sel_Add0'] = 1
            signals['enA'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
        elif first == 'B' and second == 'MEM':
            signals['sel_Add0'] = 1
            signals['enB'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
        elif first == 'MEM' and second == None:
            signals['sel_Add0'] = 1
            signals['selA1'] = 1
            signals['selB0'] = 1
            signals['w'] = 1
        elif first == 'A' and second == '(B)':
            signals['sel_Add1'] = 1
            signals['enA'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
        elif first == 'B' and second == '(B)':
            signals['sel_Add1'] = 1
            signals['enB'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1

        


        return(concat(signals))

    elif ins == "SUB":
        signals['selALU0'] = 1

        if first == 'A' and second == 'B':
            signals['sel_Add0'] = 1
            signals['enA'] = 1
            signals['selA1'] = 1
            signals['selB0'] = 1
        elif first == 'B' and second == 'A':
            signals['sel_Add0'] = 1
            signals['enB'] = 1
            signals['selA1'] = 1
            signals['selB0'] = 1
        elif first == 'A' and second == 'LIT':
            signals['sel_Add0'] = 1
            signals['enA'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
            signals['selB0'] = 1
        elif first == 'B' and second == 'LIT':
            signals['sel_Add0'] = 1
            signals['enB'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
            signals['selB0'] = 1
        elif first == 'A' and second == 'MEM':
            signals['sel_Add0'] = 1
            signals['enA'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
        elif first == 'B' and second == 'MEM':
            signals['sel_Add0'] = 1
            signals['enB'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
        elif first == 'MEM' and second == None:
            signals['sel_Add0'] = 1
            signals['selA1'] = 1
            signals['selB0'] = 1
            signals['w'] = 1
        elif first == 'A' and second == '(B)':
            signals['sel_Add1'] = 1
            signals['enA'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
        elif first == 'B' and second == '(B)':
            signals['sel_Add1'] = 1
            signals['enB'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1


        return(concat(signals))

    elif ins == "AND":

        signals['selALU1'] = 1

        if first == 'A' and second == 'B':
            signals['sel_Add0'] = 1
            signals['enA'] = 1
            signals['selA1'] = 1
            signals['selB0'] = 1
        elif first == 'B' and second == 'A':
            signals['sel_Add0'] = 1
            signals['enB'] = 1
            signals['selA1'] = 1
            signals['selB0'] = 1
        elif first == 'A' and second == 'LIT':
            signals['sel_Add0'] = 1
            signals['enA'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
            signals['selB0'] = 1
        elif first == 'B' and second == 'LIT':
            signals['sel_Add0'] = 1
            signals['enB'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
            signals['selB0'] = 1
        elif first == 'A' and second == 'MEM':
            signals['sel_Add0'] = 1
            signals['enA'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
        elif first == 'B' and second == 'MEM':
            signals['sel_Add0'] = 1
            signals['enB'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
        elif first == 'MEM' and second == None:
            signals['sel_Add0'] = 1
            signals['selA1'] = 1
            signals['selB0'] = 1
            signals['w'] = 1
        elif first == 'A' and second == '(B)':
            signals['sel_Add1'] = 1
            signals['enA'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
        elif first == 'B' and second == '(B)':
            signals['sel_Add1'] = 1
            signals['enB'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1



        return(concat(signals))

    elif ins == "OR":

        signals['selALU1'] = 1
        signals['selALU0'] = 1

        if first == 'A' and second == 'B':
            signals['sel_Add0'] = 1
            signals['enA'] = 1
            signals['selA1'] = 1
            signals['selB0'] = 1
        elif first == 'B' and second == 'A':
            signals['sel_Add0'] = 1
            signals['enB'] = 1
            signals['selA1'] = 1
            signals['selB0'] = 1
        elif first == 'A' and second == 'LIT':
            signals['sel_Add0'] = 1
            signals['enA'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
            signals['selB0'] = 1
        elif first == 'B' and second == 'LIT':
            signals['sel_Add0'] = 1
            signals['enB'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
            signals['selB0'] = 1
        elif first == 'A' and second == 'MEM':
            signals['sel_Add0'] = 1
            signals['enA'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
        elif first == 'B' and second == 'MEM':
            signals['sel_Add0'] = 1
            signals['enB'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
        elif first == 'MEM' and second == None:
            signals['sel_Add0'] = 1
            signals['selA1'] = 1
            signals['selB0'] = 1
            signals['w'] = 1
        elif first == 'A' and second == '(B)':
            signals['sel_Add1'] = 1
            signals['enA'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
        elif first == 'B' and second == '(B)':
            signals['sel_Add1'] = 1
            signals['enB'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1



        return(concat(signals))

    elif ins == "XOR":

        signals['selALU2'] = 1

        if first == 'A' and second == 'B':
            signals['sel_Add0'] = 1
            signals['enA'] = 1
            signals['selA1'] = 1
            signals['selB0'] = 1
        elif first == 'B' and second == 'A':
            signals['sel_Add0'] = 1
            signals['enB'] = 1
            signals['selA1'] = 1
            signals['selB0'] = 1
        elif first == 'A' and second == 'LIT':
            signals['sel_Add0'] = 1
            signals['enA'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
            signals['selB0'] = 1
        elif first == 'B' and second == 'LIT':
            signals['sel_Add0'] = 1
            signals['enB'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
            signals['selB0'] = 1
        elif first == 'A' and second == 'MEM':
            signals['sel_Add0'] = 1
            signals['enA'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
        elif first == 'B' and second == 'MEM':
            signals['sel_Add0'] = 1
            signals['enB'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
        elif first == 'MEM' and second == None:
            signals['sel_Add0'] = 1
            signals['selA1'] = 1
            signals['selB0'] = 1
            signals['w'] = 1
        elif first == 'A' and second == '(B)':
            signals['sel_Add1'] = 1
            signals['enA'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
        elif first == 'B' and second == '(B)':
            signals['sel_Add1'] = 1
            signals['enB'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
        return(concat(signals))

    elif ins == "NOT":


        signals['selALU2'] = 1
        signals['selALU0'] = 1

        if first == 'A' and second == None:
            signals['sel_Add0'] = 1
            signals['enA'] = 1
            signals['selA1'] = 1

        elif first == 'B' and second == 'A':
            signals['sel_Add0'] = 1
            signals['enB'] = 1
            signals['selA1'] = 1

        elif first =='MEM' and second == 'A':
            signals['sel_Add0'] = 1
            signals['selA1'] = 1
            signals['w'] = 1
        
        elif first == '(B)' and second == 'A' :
            signals['sel_Add1'] = 1
            signals['selA1'] = 1
            signals['w'] = 1


        return(concat(signals))

    elif ins == "SHR":


        signals['selALU2'] = 1
        signals['selALU1'] = 1

        if first == 'A' and second == None:
            signals['sel_Add0'] = 1
            signals['enA'] = 1
            signals['selA1'] = 1

        elif first == 'B' and second == 'A':
            signals['sel_Add0'] = 1
            signals['enB'] = 1
            signals['selA1'] = 1

        elif first =='MEM' and second == 'A':
            signals['sel_Add0'] = 1
            signals['selA1'] = 1
            signals['w'] = 1
        
        elif first == '(B)' and second == 'A' :
            signals['sel_Add1'] = 1
            signals['selA1'] = 1
            signals['w'] = 1


        return(concat(signals))

    elif ins == "SHL":


        signals['selALU2'] = 1
        signals['selALU1'] = 1
        signals['selALU0'] = 1

        if first == 'A' and second == None:
            signals['sel_Add0'] = 1
            signals['enA'] = 1
            signals['selA1'] = 1

        elif first == 'B' and second == 'A':
            signals['sel_Add0'] = 1
            signals['enB'] = 1
            signals['selA1'] = 1

        elif first =='MEM' and second == 'A':
            signals['sel_Add0'] = 1
            signals['selA1'] = 1
            signals['w'] = 1
        
        elif first == '(B)' and second == 'A' :
            signals['sel_Add1'] = 1
            signals['selA1'] = 1
            signals['w'] = 1


        return(concat(signals))

    elif ins == "INC":

        if first == 'A':
            signals['sel_Add0'] = 1
            signals['enA'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
            signals['selB0'] = 1

        elif first == 'B':
            signals['sel_Add0'] = 1
            signals['enB'] = 1
            signals['selA0'] = 1
            signals['selB0'] = 1

        elif first == 'MEM':
            signals['sel_Add0'] = 1
            signals['selA0'] = 1
            signals['selB1'] = 1
            signals['w'] = 1

        elif first == '(B)':
            signals['sel_Add1'] = 1
            signals['selA0'] = 1
            signals['selB1'] = 1
            signals['w'] = 1
        
        return(concat(signals))

    elif ins == "DEC":

        signals['sel_Add0'] = 1
        signals['enA'] = 1
        signals['selA1'] = 1
        signals['selB1'] = 1
        signals['selB0'] = 1
        signals['selALU0'] = 1

        return(concat(signals))

    elif ins == "CMP":

        signals['selALU0'] = 1

        if first == 'A' and second == 'B':
            signals['sel_Add0'] = 1
            signals['selA1'] = 1
            signals['selB0'] = 1

        elif first == 'A' and second == 'LIT':
            signals['sel_Add0'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
            signals['selB0'] = 1

        elif first == 'A' and second == 'MEM':
            signals['sel_Add0'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1
        
        elif first == 'A' and second == '(B)':
            signals['sel_Add1'] = 1
            signals['selA1'] = 1
            signals['selB1'] = 1



        return(concat(signals))

    elif ins == "JMP":
        signals['sel_Add0'] = 1
        signals['loadPC'] = 1
        return(concat(signals))

    elif ins == "JEQ":
        signals['sel_Add0'] = 1
        signals['sel_jump0'] = 1
        signals['loadPC'] = 1
        return(concat(signals))

    elif ins == "JNE":
        signals['sel_Add0'] = 1
        signals['sel_jump1'] = 1
        signals['loadPC'] = 1
        return(concat(signals))

    elif ins == "JGT":
        signals['sel_Add0'] = 1
        signals['sel_jump0'] = 1
        signals['sel_jump1'] = 1
        signals['loadPC'] = 1
        return(concat(signals))

    elif ins == "JGE":
        signals['sel_Add0'] = 1
        signals['sel_jump2'] = 1
        signals['loadPC'] = 1
        return(concat(signals))

    elif ins == "JLT":
        signals['sel_Add0'] = 1
        signals['sel_jump2'] = 1
        signals['sel_jump0'] = 1
        signals['loadPC'] = 1
        return(concat(signals))

    elif ins == "JLE":
        signals['sel_Add0'] = 1
        signals['sel_jump2'] = 1
        signals['sel_jump1'] = 1
        signals['loadPC'] = 1
        return(concat(signals))

    elif ins == "JCR":
        signals['sel_Add0'] = 1
        signals['sel_jump0'] = 1
        signals['sel_jump1'] = 1
        signals['sel_jump2'] = 1
        signals['loadPC'] = 1
        return(concat(signals))

    elif ins == "PUSH":
        if first == 'A':
            signals['dec_Sp'] = 1
            signals['selA1'] = 1
            signals['w'] = 1
        elif first == 'B':
            signals['dec_Sp'] = 1
            signals['selB0'] = 1
            signals['w'] = 1
        return(concat(signals))

    elif ins == "POP":
        if first == 'A':
            signals['enA'] = 1
            signals['selB1'] = 1
        elif first == 'B':
            signals['enB'] = 1
            signals['selB1'] = 1
        return(concat(signals))

    elif ins == "CALL":
        signals['sel_Din'] = 1
        signals['dec_Sp'] = 1
        signals['loadPC'] = 1
        signals['w'] = 1
        return(concat(signals))


    elif ins == "NOP":
        return(concat(signals))

    elif ins == "CODE:":
        pass



rom_programmer = Basys3()
rom_programmer.begin(3)

opcode_aux_2 = "000001000001000000010000000000000000"
opcode_aux_2 = int(opcode_aux_2, 2)
aux_bytes_2 = opcode_aux_2.to_bytes(5, "big")
rom_programmer.write(0,bytearray(aux_bytes_2))

file_path = sys.argv[1]

signals = {
    'sel_Add1': 0,
    'sel_Add0': 0,
    'sel_Din': 0,
    'sel_Pc': 0,
    'inc_Sp': 0,
    'dec_Sp': 0,
    'sel_jump2': 0,
    'sel_jump1': 0,
    'sel_jump0': 0,
    'enA': 0,
    'enB': 0,
    'selA1': 0,
    'selA0': 0,
    'selB1': 0,
    'selB0': 0,
    'selALU2': 0,
    'selALU1': 0,
    'selALU0': 0,
    'loadPC': 0,
    'w': 0,
    }

instructions = [
    'MOV',
    'ADD',
    'SUB',
    'AND',
    'OR',
    'XOR',
    'NOT',
    'SHL',
    'SHR',
    'INC',
    'DEC',
    'CMP',
    'JMP',
    'JEQ',
    'JNE',
    'JGT',
    'JGE',
    'JLT',
    'JLE',
    'JCR',
    'NOP',
    'PUSH',
    'POP',
    'CALL',
    'RET'
]


def parse_data_section(data: list, pc, direccion, code) -> list:

    for value in data:

        reset(signals)
        value_binario = (value).zfill(16)
        code.append(['MOV', ['A', 'LIT'], value_binario, pc])
        direccion_binario = decimal_a_binario_16bits(direccion)
        code.append(['MOV', ['MEM', 'A'], direccion_binario, pc+1])
        pc += 2
        direccion += 1

    return pc


def parse_value(value: str) -> Union[int, str]:
    try:
        if value[len(value) - 1] == 'd':
            num_value = bin(int(value[:len(value) - 1]))[2:]
            return num_value
        elif value[len(value) - 1] == 'h':
            num_value = bin(int(value[:len(value) - 1], 16))[2:]
            return num_value
        elif value[len(value) - 1] == 'b':
            return value[:-1]
        else:
            return bin(int(value))[2:]
    except:
        return value

def create_code(code, signals, rom_programmer):
    for line in code:
        reset(signals)
        ins = line[0]
        args = line[1]
        lit = line[2]
        pc = line[3] 
        opcode_aux = "000010000000000000000000000000000000"
        opcode_aux = opcode_aux.zfill(36)
        if ins == "POP":
            opcode_aux = int(opcode_aux, 2)
            aux_bytes = opcode_aux.to_bytes(5, "big")
            rom_programmer.write(pc,bytearray(aux_bytes))
            #ESCRIBIR EN PALCA
            opcode = build_opcode(ins, args, signals)
            opcode = (opcode + lit).zfill(36)
            opcode_int = int(opcode, 2)
            opcode_bytes = opcode_int.to_bytes(5, "big")
            rom_programmer.write(pc+1,bytearray(opcode_bytes))
            #ESCRIBIR EN PLACA
            pass
        elif ins == "RET":
            opcode_aux = int(opcode_aux, 2)
            aux_bytes = opcode_aux.to_bytes(5, "big")
            rom_programmer.write(pc,bytearray(aux_bytes))
            #ESCRIBIR EN PALCA
            opcode_aux_2 = "000100000000000000100000000000000000"
            opcode_aux_2 = opcode_aux_2.zfill(36)
            opcode_aux_2 = int(opcode_aux_2, 2)
            aux_bytes_2 = opcode_aux_2.to_bytes(5, "big")
            rom_programmer.write(pc+1,bytearray(aux_bytes_2))
            #ESCRIBIR EN PALCA
        else:
            opcode = build_opcode(ins, args, signals)
            opcode = (opcode + lit).zfill(36)
            opcode_int = int(opcode, 2)
            opcode_bytes = opcode_int.to_bytes(5, "big")
            rom_programmer.write(pc,bytearray(opcode_bytes))
            #ESCRIBIR EN PLACA
data_diccionary = {}
direccion = 8 #parte del 8 porque los primeros 8 lugares esta reservados
direccion_parse = 8

if os.path.exists(file_path):
    literal = "0"
    zero = 0
    zero_bytes = zero.to_bytes(2, byteorder="big")
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            if '//' in line:
                line = line[:line.index('//')]
            # AQUI LIMPIAR LAS LINEAS, CREAR 2 FUNCIONES PARA ESCRIBIR DATA Y ESCRIBIR CODIGO
            reset(signals)
            literal = "0"

            if 'DATA:' in line:
                is_data_section = True

            if 'CODE:' in line:
                is_data_section = False
            
            if is_data_section and 'DATA:' not in line:
                l = line.strip('\n')
                l = l.split(' ')
                l[0] = l[0].replace(' ', '')
                if l[0] != '':
                    print(direccion)
                    print(line)
                    data_diccionary[l[0]] = direccion
                    direccion += 1

            if is_data_section and 'DATA:' not in line:
                #data section can be array, string or integer (in different formats)
                line = line.split()
                if len(line) > 1:
                    value = parse_value(line[1])
                    data.append(value)
                elif len(line) == 1:
                    value = parse_value(line[0])
                    data.append(value)

else:
    print('The specified file does NOT exist')
print('\n' + 'Data:')
print(data_diccionary)
print('\n' + 'Instrucciones:')
pc = parse_data_section(data, pc, direccion_parse, code)
pc_desfase = pc
pc -=1

if os.path.exists(file_path):
    literal = "0"
    zero = 0
    zero_bytes = zero.to_bytes(2, byteorder="big")
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            if '//' in line:
                line = line[:line.index('//')]
            # AQUI LIMPIAR LAS LINEAS, CREAR 2 FUNCIONES PARA ESCRIBIR DATA Y ESCRIBIR CODIGO
            reset(signals)
            literal = "0"

            if 'DATA:' in line:
                is_data_section = True

            if 'CODE:' in line:
                is_data_section = False
            
            if not is_data_section and 'CODE:' not in line:
                pc = parse_code_section(line, pc, code, jump_labels, data_diccionary)
            # print(opcode + literal)

else:
    print('The specified file does NOT exist')

for i in range (0, len(code)):
        if 'J' in code[i][0] or 'CALL' in code[i][0]:
            label = code[i][1][0]
            try :
                value = decimal_a_binario_16bits(int(label)+pc_desfase)
            except ValueError:
                jump_value = jump_labels[label]
                value = decimal_a_binario_16bits(jump_value)
            code[i] = [code[i][0], ['LIT'], value, code[i][2] ]

for ins in code:
    print(ins)
print('\n' + 'Labels:')
print(jump_labels)
create_code(code, signals, rom_programmer)
rom_programmer.end()

