# The Small assembler

This is an assembler for targeting the Small instructions set.
It generates 16-bit aligned bytecode.
Preprocessor directive include:

- `use` for importing libraries
- `lab` for defining labels

Variables are supported, inferred at generation-time
and bump allocated linearly. These act as the primary
memory managment technique, replacing conventional
assembler memory managment pracitces.


