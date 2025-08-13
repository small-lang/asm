#!/usr/bin/python3

import argparse
import sys
from dataclasses import dataclass



def error(i, p, m):
    print(f"Error at line {i} in file {p}: \n\t{m}")
    sys.exit(1)


@dataclass
class inst:
    _name  : str
    _arg  : str | None
    index : int
    path  : str

    @classmethod
    def parse(cls, line, src_index, src_path):
        comps = list(filter(lambda x: len(x) > 0, line.split(' ')))
        base_args = (comps + [None])[:2]
        return cls(*base_args, src_index, src_path)

    def name(self):
        return self._name

    def arg(self):
        if self._arg is not None:
            return self._arg

        else:
            error(self.index, self.path, f"Instruction {self._name} should have argument")







def parse(path):
    with open(path) as f:
        lines = f.readlines()

    insts = []
    for index, line_raw in enumerate(lines):
        line = line_raw.strip('\n\t ')
        if len(line) == 0:
            continue
        
        insts.append(inst.parse(line, index, path))
    
    return insts

def preprocess(insts):
    addr = 0
    map = {}

    for inst in insts: 
        if inst.name() == 'lab':
            map[inst.arg()] = addr
        else:
            addr += 1

    return map




def assemble(path):
    insts = parse(path)
    labels = preprocess(insts)

    print(labels)

    




def main():
    parser = argparse.ArgumentParser(
        prog='Small Assembler',
        description='Assembler for the Small assembly language',
        epilog=':3'
    ) 

    parser.add_argument('path')
    parser.add_argument('-o', '--output', default='build')

    args = parser.parse_args()

    assemble(args.path)

if __name__ == '__main__':
    main()


