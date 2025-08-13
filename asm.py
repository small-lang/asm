#!/usr/bin/python3

import argparse







def main():
    parser = argparse.ArgumentParser(
        prog='Small Assembler',
        description='Assembler for the Small assembly language',
        epilog=':3'
    ) 

    parser.add_argument('path')
    parser.add_argument('-o', '--output', default='build')

    args = parser.parse_args()

    print(args)


if __name__ == '__main__':
    main()


