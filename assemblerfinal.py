binaryopcode = {'add': '00000', 'sub': '00001', 'mov1': '00010', 'mov2': '00011', 'ld': '00100', 'st': '00101', 'mul': '00110', 'div': '00111', 'rsl': '01000', 'lsl': '01001', 'xor': '01010', 'or': '01011', 'and': '01100', 'not': '01101', 'cmp': '01110',
           'jmp': '01111', 'jlt': '11100', 'jgt': '11101', 'je': '11111', 'hlt': '11010', 'mov': '0'}

instructiontype = {'add': '3reg', 'sub': '3reg', 'mov1': 'regimm', 'mov2': '2reg', 'ld': 'regmem', 'st': 'regmem', 'mul': '3reg', 'div': '2reg',
                'rsl': 'regimm', 'lsl': 'regimm', 'xor': '3reg', 'or': '3reg', 'and': '3reg', 'not': '2reg', 'cmp': '2reg',
                'jmp': 'memaddress', 'jlt': 'memaddr', 'jgt': 'memaddr', 'je': 'memaddr', 'hlt': 'end', 'mov': '0'}

extrabits = {'3reg': '00', 'regimm': '0', '2reg':'00000', 'regmem': '0', 'memaddress': '0000', 'end': '00000000000'}

regs = {'R0': '000', 'R1': '001', 'R2': '010', 'R3': '011', 'R4': '100', 'R5': '101', 'R6':'110', 'FLAGS': '111'}

registervalues = {'R0': 0, 'R1': 0, 'R2': 0, 'R3': 0, 'R4': 0, 'R5': 0, 'R6': 0, 'FLAGS': 0}

variables = {}

linecount = 1

binarycode = []

with open('stdin.txt', 'r') as f:
    data = f.readlines()
    for line in data:
        line = line.strip()
        instruction = line.split()
        binaryline = []
        if instruction[0] == 'var':
            variables[instruction[1]] == 0
        else:
            break

registers = ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6']


with open('stdin.txt', 'r') as f:
    data = f.readlines()
    for line in data:
        line = line.strip()
        instruction = line.split()
        binaryline = []
        if len(instruction) == 0:
            continue
        elif instruction[0] not in binaryopcode.keys() and instruction[0] != 'var':
            binaryline = 'Error on line ' + str(linecount) + ': Illegal instruction'
            binarycode.append(binaryline)
            linecount += 1
            continue
        elif instruction[0] == 'var':
            binaryline = 'Error on line ' + str(linecount) + ': Variables must be declared at the beginning'
            linecount += 1
            continue
        elif instruction[0] in binaryopcode.keys():
            if instructiontype[instruction[0]] == '3reg':
                if len(instruction) != 4:
                    binaryline = 'Error on line ' + str(linecount) + ': ' + instruction[0] + ' requires 3 parameters'
                    binarycode.append(binaryline)
                    linecount += 1
                    continue
                elif instruction[1] not in registers or instruction[2] not in registers or instruction[3] not in registers:
                    binaryline = 'Error on line ' + str(linecount) + ': Illegal register used'
                    binarycode.append(binaryline)
                    linecount += 1
                    continue
                else:
                    binaryline = binaryopcode[instruction[0]] + extrabits[instructiontype[instruction[0]]] + regs[instruction[1]] + regs[instruction[2]] + regs[instruction[3]]
                    binarycode.append(binaryline)
                    linecount += 1
                    continue
            elif instructiontype[instruction[0]] == '2reg':
                if len(instruction) != 3:
                    binaryline = 'Error on line ' + str(linecount) + ': ' + instruction[0] + ' requires 2 parameters'
                    continue
                elif instruction[0] == 'mov': #special check for mov
                    if instruction[1] not in regs.keys():
                        binaryline = 'Error on line ' + str(linecount) + ': Illegal register used'
                        binarycode.append(binaryline)
                        linecount += 1
                        continue
                    elif instruction[2] in regs.keys():
                        binaryline = binaryopcode['mov2'] + regs[instruction[1]] + regs[instruction[2]]
                        binarycode.append(binaryline)
                        linecount += 1
                        continue
                    elif instruction[2][0] == '$':
                        for i in instruction[1][1:]:
                            if i.isnumeric() == False:
                                binaryline = 'Error on line ' + str(linecount) + ': Not an integer'
                                binarycode.append(binaryline)
                                linecount += 1
                                break
                            else:
                                pass
                        if int(instruction[2][1:]) > 127 or int(instruction[2][1:]) < 0:
                                binaryline = 'Error on line ' + str(linecount) + ': Illegal immediate value'
                                binarycode.append(binaryline)
                                linecount += 1
                                continue
                        else:
                            binaryline = binaryopcode['mov1'] + regs[instruction[1]] + format(int(instruction[2]), '07b')
                            binarycode.append(binaryline)
                            linecount += 1
                            continue
                elif instruction[0] == 'div':
                    if instruction[1] not in registers or instruction[2] not in registers:
                        binaryline = 'Error on line ' + str(linecount) + ': Illegal register used'
                        binarycode.append(binaryline)
                        linecount += 1
                        continue
                    elif registervalues[instruction[2]] == 0:
                        registervalues[instruction[1]] = 0
                        registervalues[instruction[2]] = 0
                        registervalues['FLAGS'] = '0000000000001000'
                        binaryline = binaryopcode['div'] + regs[instruction[1]] + regs[instruction[2]]
                        linecount += 1
                        continue
                    else:
                        registervalues['R0'] = registervalues[instruction[1]]/registervalues[instruction[2]]
                        registervalues['R1'] = registervalues[instruction[1]] % registervalues[instruction[2]]
                        binaryline = binaryopcode['div'] + regs[instruction[1]] + regs[instruction[2]]
                        binarycode.append(binaryline)
                        linecount += 1
                        continue
                



                    


with open('stdout.txt', 'w') as file:
    for i in binarycode:
        file.write(i)
        file.write('\n')


