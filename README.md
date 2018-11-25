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

## Notes

- Inspired by [Selfie](https://github.com/cksystemsteaching/selfie)
- Start with most basic subset - always easier to expand later (tracer bullet style)
- `gcc -masm=intel -S -O2 test.c` produces somewhat readable assembly for
reference.
