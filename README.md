# Simple Compiler

## TODO

- Come up with different name
- Add better test coverage on parser and lexxer

## Goals

- Explore type systems
- Explore compilation
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
