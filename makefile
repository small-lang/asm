TARGET = prg/fib.small

run: compile
	./vm build

compile:
	./asm.py $(TARGET)


