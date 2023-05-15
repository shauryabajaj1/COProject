binaryopcode = {'add': '00000', 'sub': '00001', 'mov1': '00010', 'mov2': '00011', 'ld': '00100', 'st': '00101', 'mul': '00110', 'div': '00111', 'rs': '01000', 'ls': '01001', 'xor': '01010', 'or': '01011', 'and': '01100', 'not': '01101', 'cmp': '01110',
           'jmp': '01111', 'jlt': '11100', 'jgt': '11101', 'je': '11111', 'hlt': '11010', 'mov': '0'}

instructiontype = {'add': '3reg', 'sub': '3reg', 'mov1': 'regimm', 'mov2': '2reg', 'ld': 'regmem', 'st': 'regmem', 'mul': '3reg', 'div': '2reg',
                'rs': 'regimm', 'ls': 'regimm', 'xor': '3reg', 'or': '3reg', 'and': '3reg', 'not': '2reg', 'cmp': '2reg',
                'jmp': 'memaddr', 'jlt': 'memaddr', 'jgt': 'memaddr', 'je': 'memaddr', 'hlt': 'end', 'mov': '2reg'}

extrabits = {'3reg': '00', 'regimm': '0', '2reg':'00000', 'regmem': '0', 'memaddress': '0000', 'end': '00000000000'}

regs = {'R0': '000', 'R1': '001', 'R2': '010', 'R3': '011', 'R4': '100', 'R5': '101', 'R6':'110', 'FLAGS': '111'}

registervalues = {'R0': 0, 'R1': 0, 'R2': 0, 'R3': 0, 'R4': 0, 'R5': 0, 'R6': 0, 'FLAGS': 0}

variables = {}

hltcheck = 0

binarycode = []

errorcode = []

labels = {}

labellinecount = 0

initial_line_count = 1

with open('stdin.txt', 'r') as f:
    data = f.readlines()
    for line in data:
        line = line.strip()
        instruction = line.split()
        if instruction[0] == 'var' or len(instruction) == 0:
            pass
        else:
            initial_line_count += 1

with open('stdin.txt', 'r') as f:
    data = f.readlines()
    for line in data:
        line = line.strip()
        instruction = line.split()
        if instruction[0] == 'var' or len(instruction) == 0:
            continue
        if instruction[0][-1] == ':':
            labels[instruction[0][:-1]] = format(labellinecount, '07b')
        labellinecount += 1

labellinecount += 1

with open('stdin.txt', 'r') as f:
    data = f.readlines()
    vars=[]
    for line in data:
        line = line.strip()
        instruction = line.split()
        errorline = []
        if instruction[0] == 'var':
            vars.append(instruction[1])
        else:
            break

z = 1

for i in vars:
    variables[i] = format(labellinecount - len(vars) + z, '07b')
    z += 1

linecount = 1 + len(variables)

registers = ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6']


with open('stdin.txt', 'r') as f:
    data = f.readlines()
    for line in data[len(variables):]:
        line = line.strip()
        instruction = line.split()
        errorline = []
        binaryline = []
        if len(instruction) == 0:
            continue
        if instruction[0][-1] == ':':
            instruction = instruction[1:]
        if hltcheck == 1:
            errorline = 'Error on line ' + str(linecount) + ': Instructions after hlt can\'t be executed'
            errorcode.append(errorline)
            linecount += 1
            continue
        elif instruction[0] not in binaryopcode.keys() and instruction[0] != 'var':
            errorline = 'Error on line ' + str(linecount) + ': Illegal instruction'
            errorcode.append(errorline)
            linecount += 1
            continue
        elif instruction[0] == 'var':
            errorline = 'Error on line ' + str(linecount) + ': Variables must be declared at the beginning'
            errorcode.append(errorline)
            linecount += 1
            continue
        elif instruction[0] in binaryopcode.keys():
            if instructiontype[instruction[0]] == '3reg':
                if len(instruction) != 4:
                    errorline = 'Error on line ' + str(linecount) + ': ' + instruction[0] + ' requires 3 parameters'
                    errorcode.append(errorline)
                    linecount += 1
                    continue
                elif instruction[1] not in registers or instruction[2] not in registers or instruction[3] not in registers:
                    errorline = 'Error on line ' + str(linecount) + ': Illegal register used'
                    errorcode.append(errorline)
                    linecount += 1
                    continue
                else:
                    binaryline = binaryopcode[instruction[0]] + extrabits[instructiontype[instruction[0]]] + regs[instruction[1]] + regs[instruction[2]] + regs[instruction[3]]
                    binarycode.append(binaryline)
                    linecount += 1
                    continue
            elif instructiontype[instruction[0]] == '2reg':
                if len(instruction) != 3:
                    errorline = 'Error on line ' + str(linecount) + ': ' + instruction[0] + ' requires 2 parameters'
                    errorcode.append(errorline)
                    linecount += 1
                    continue
                elif instruction[0] == 'mov': #special check for mov
                    if instruction[1] not in regs.keys():
                        errorline = 'Error on line ' + str(linecount) + ': Illegal register used'
                        errorcode.append(errorline)
                        linecount += 1
                        continue
                    elif instruction[2] in regs.keys():
                        binaryline = binaryopcode['mov2'] + extrabits['2reg'] + regs[instruction[1]] + regs[instruction[2]]
                        binarycode.append(binaryline)
                        linecount += 1
                        continue
                    elif instruction[2][0] == '$':
                        if instruction[2][1:].isdigit() == False:
                            errorline = 'Error on line ' + str(linecount) + ': Not an integer'
                            errorcode.append(errorline)
                            linecount += 1
                            continue
                        elif int(instruction[2][1:]) > 127 or int(instruction[2][1:]) < 0:
                                errorline = 'Error on line ' + str(linecount) + ': Illegal immediate value'
                                errorcode.append(errorline)
                                linecount += 1
                                continue
                        else:
                            binaryline = binaryopcode['mov1'] + extrabits['regimm'] + regs[instruction[1]] + format(int(instruction[2][1:]), '07b')
                            binarycode.append(binaryline)
                            linecount += 1
                            continue
                elif instruction[0] == 'div':
                    if instruction[1] not in registers or instruction[2] not in registers:
                        errorline = 'Error on line ' + str(linecount) + ': Illegal register used'
                        errorcode.append(errorline)
                        linecount += 1
                        continue
                    elif registervalues[instruction[2]] == 0:
                        registervalues[instruction[1]] = 0
                        registervalues[instruction[2]] = 0
                        registervalues['FLAGS'] = '0000000000001000'
                        binaryline = binaryopcode['div'] + regs[instruction[1]] + regs[instruction[2]]
                        binarycode.append(binaryline)
                        linecount += 1
                        continue
                    else:
                        registervalues['R0'] = registervalues[instruction[1]]/registervalues[instruction[2]]
                        registervalues['R1'] = registervalues[instruction[1]] % registervalues[instruction[2]]
                        errorline = binaryopcode['div'] + regs[instruction[1]] + regs[instruction[2]]
                        binarycode.append(binaryline)
                        linecount += 1
                        continue
                else:
                    if instruction[1] not in registers or instruction[2] not in registers:
                        errorline = 'Error on line ' + str(linecount) + ': Illegal register used'
                        errorcode.append(errorline)
                        linecount += 1
                        continue
                    else:
                        binaryline = binaryopcode[instruction[0]] + extrabits['2reg'] + regs[instruction[1]] + regs[instruction[2]]
                        binarycode.append(binaryline)
                        linecount += 1
                        continue
            elif instructiontype[instruction[0]] == 'regimm':
                if len(instruction) != 3:
                    errorline = 'Error on line ' + str(linecount) + ': ' + instruction[0] + ' requires 2 parameters'
                    errorcode.append(errorline)
                    linecount += 1
                    continue
                elif instruction[1] not in registers:
                    errorline = 'Error on line ' + str(linecount) + ': Illegal register used'
                    errorcode.append(errorline)
                    linecount += 1
                    continue
                elif instruction[2][0] == '$':
                        if instruction[2][1:].isdigit() == False:
                            errorline = 'Error on line ' + str(linecount) + ': Not an integer'
                            errorcode.append(errorline)
                            linecount += 1
                            continue
                        if int(instruction[2][1:]) > 127 or int(instruction[2][1:]) < 0:
                                errorline = 'Error on line ' + str(linecount) + ': Illegal immediate value'
                                errorcode.append(errorline)
                                linecount += 1
                                continue
                        else:
                            binaryline = binaryopcode['mov1'] + extrabits['regimm'] + regs[instruction[1]] + format(int(instruction[2][1:]), '07b')
                            binarycode.append(binaryline)
                            linecount += 1
                            continue
            elif instructiontype[instruction[0]] == 'regmem':
                if len(instruction) != 3:
                    errorline = 'Error on line ' + str(linecount) + ': ' + instruction[0] + ' requires 2 parameters'
                    errorcode.append(errorline)
                    linecount += 1
                    continue
                elif instruction[1] not in registers:
                    errorline = 'Error on line ' + str(linecount) + ': Illegal register used'
                    errorcode.append(errorline)
                    linecount += 1
                    continue
                elif instruction[2] not in variables.keys():
                    errorline = 'Error on line ' + str(linecount) + ': Use of undefined variable'
                    errorcode.append(errorline)
                    linecount += 1
                    continue
                else:
                    binaryline = binaryopcode[instruction[0]] + extrabits['regmem'] + regs[instruction[1]] + variables[instruction[2]]
                    binarycode.append(binaryline)
                    linecount += 1
                    continue
            elif instructiontype[instruction[0]] == 'memaddr':
                if len(instruction) != 2:
                    errorline = 'Error on line ' + str(linecount) + ' ' + instruction[0] + ' requires 1 parameter'
                    errorcode.append(errorline)
                    linecount += 1
                    continue
                elif instruction[1] not in labels.keys():
                    errorline = 'Error on line ' + str(linecount) + ': Use of undefined label'
                    errorcode.append(errorline)
                    linecount += 1
                    continue
                else:
                    binaryline = binaryopcode[instruction[0]] + extrabits['memaddress'] + labels[instruction[1]]
                    binarycode.append(binaryline)
                    linecount += 1
                    continue
            elif instructiontype[instruction[0]] == 'end':
                hltcheck = 1
                binaryline = binaryopcode['hlt'] + extrabits['end']
                binarycode.append(binaryline)
                linecount += 1
                continue
            
if hltcheck == 0:
    errorcode[-1] = 'Error: Missing hlt instruction'


print(errorcode)
with open('stdout.txt', 'w') as file:
    if len(errorcode) != 0:
        for i in errorcode:
            file.write(i)
            file.write('\n')
    else:
        for i in binarycode:
            file.write(i)
            file.write('\n')


