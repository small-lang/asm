#!/usr/bin/python3

import argparse
import struct
import itertools
import sys
from dataclasses import dataclass
from dataclasses import field



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
    def parse(cls, comps, src_index, src_path):
        base_args = (comps + [None])[:2]
        return cls(*base_args, src_index, src_path)

    def name(self):
        return self._name

    def arg(self):
        if self._arg is not None:
            return self._arg

        else:
            error(self.index, self.path, f"Instruction {self._name} should have argument")





imported = set()
def parse(path):
    #make sure library only gets imported once
    if path in imported:
        return []

    imported.add(path)


    with open(path) as f:
        lines = f.readlines()

    insts = []
    for index, line_raw in enumerate(lines):
        line = line_raw.strip('\n\t ')
        #emtpy line
        if len(line) == 0:
            continue

        #comment
        if line[0] == '"':
            continue

        comps = list(filter(lambda x: len(x) > 0, line.split(' ')))
        if comps[0] == 'use':
            if len(comps) < 2:
                error(index, path, "Use directive without path")

            insts += parse(comps[1].strip("'"))

        else:
            insts.append(inst.parse(comps, index, path))
    
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

@dataclass
class output:
    buffer : bytearray = field(default_factory=lambda: bytearray())

    def __call__(self, code, arg = 0):
        inst = struct.pack('<HH', code, arg)
        self.buffer.extend(inst)

    def emit(self, path):
        with open(path, "wb") as f:
            f.write(self.buffer)


@dataclass
class config:
    code : int | None
    label : bool = False #argument needs to be label
    expr  : bool = False #argument is expression (either variable or immediate)
    only  : bool = False #no argument to be provided


def assemble(path):
    insts = parse(path)
    labels = preprocess(insts)

    print(labels)

    mapper = {
        "hlt": config( 0, only  = True),
        "ldi": config( 1, expr  = True),
        "shr": config( 2, expr  = True),
        "shl": config( 3, expr  = True),
        "nad": config( 4, expr  = True),
        "jmp": config( 5, label = True),
        "jmz": config( 6, label = True),
        "cal": config( 7, label = True),
        "ret": config( 8, only  = True),
        "lda": config( 9, expr  = True),
        "sta": config(10, expr  = True),
        "pha": config(11, only  = True),
        "pla": config(12, only  = True),
        "out": config(13, only  = True),
        "inp": config(14, only  = True),
        "res": config(15, only  = True),

        "lab": config(None)
    }

    buffer = output()

    vars = {}
    var_alloc = itertools.count(0)

    for inst in insts:
        cfg = mapper[inst.name()]

        if cfg.only: 
            buffer(cfg.code, 0)
            if inst._arg is not None:
                error(inst.index, inst.path, f"Instruction {inst.name()} should not have argument")

        if cfg.expr:
            arg = inst.arg()

            #immediate
            if arg.isdigit():
                buffer(cfg.code, int(arg))

            #variable
            else:
                if arg not in vars:
                    vars[arg] = next(var_alloc)

                buffer(cfg.code, vars[arg])

        if cfg.label:
            if inst.arg() not in labels:
                error(inst.index, inst.path, f"Undeclared label {inst.arg()}")

            buffer(cfg.code, labels[inst.arg()])


    print(vars)

    return buffer

    




def main():
    parser = argparse.ArgumentParser(
        prog='Small Assembler',
        description='Assembler for the Small assembly language',
        epilog=':3'
    ) 

    parser.add_argument('path')
    parser.add_argument('-o', '--output', dest="out", default='build')

    args = parser.parse_args()

    assemble(args.path).emit(args.out)

if __name__ == '__main__':
    main()


