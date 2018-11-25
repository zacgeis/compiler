# Simple Compiler

## TODO

- Come up with different name
- Add better test coverage on parser and lexxer
- Optimize local call temp storage to use registers
- Update lexxer and parser to allow newlines as semicolons
  - Given that newlines are going to be in many locations, we'll need a way
optionally skipping them.
  - An example of this is when you break the function definition across multiple
lines

## Goals

- Target x86_64 assembly with Intel syntax
- Explore type systems
- Explore compilation
- Support templated generics (also reqiures overloading)
- Explore language features
- Allow for different backends
- Target CPU written on FPGA?
- Maybe write an assembler?
- Maybe write a linker?
- Initial python is simple enough that self hosting is an option

## Usage

TODO

## Notes

- Start with most basic subset - always easier to expand later (tracer bullet style)
- `gcc -masm=intel -S -O2 test.c` produces somewhat readable assembly for
reference.
- Went back over the AST and really considered if each node was necessary. Ended
up getting rid of infix and prefix and combining them into call. Good exercise
in refactoring.

## Inspirations

- [Selfie](https://github.com/cksystemsteaching/selfie)
- [Programming from the Ground
Up](https://download-mirror.savannah.gnu.org/releases/pgubook/ProgrammingGroundUp-1-0-booksize.pdf)
-
[Compilers](https://www.amazon.com/Compilers-Principles-Techniques-Tools-2nd/dp/0321486811/ref=sr_1_2?ie=UTF8&qid=1543189355&sr=8-2&keywords=compilers)
- [From Nand to Tetris](https://www.nand2tetris.org/)
