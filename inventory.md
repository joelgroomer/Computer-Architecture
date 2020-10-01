# Inventory

Computer-Architecture

| dir            | file              | desc                                                                       | implemented     |
| -------------- | ----------------- | -------------------------------------------------------------------------- | --------------- |
| /              |                   |                                                                            |                 |
|                | .gitignore        | gitignore file                                                             | n/a             |
|                | FAQ.md            | FAQ                                                                        | n/a             |
|                | inventory.md      | this document                                                              | n/a             |
|                | LS8-cheatsheet.md | ???                                                                        | n/a             |
|                | LS8-spec.md       | specification for LS-8 machine                                             | n/a             |
|                | README.md         | timeline for proj                                                          | n/a             |
| /asm/          |                   |                                                                            |                 |
|                | asm.js            | DEPRECATED: use asm.py instead                                             | n/a             |
|                | asm.py            | This takes LS-8 assembler source and converts it into .ls8 "binary" files. | yes?            |
|                | buildall          | builds something                                                           | yes?            |
|                | call.asm          | Demonstrate calls                                                          | YES             |
|                | interrupts.asm    | Hook the timer interrupt                                                   | YES             |
|                | keyboard.asm      | A simple program to test the keyboard and echo to console.                 | YES             |
|                | mult.asm          | Multiplies 8 and 9 and resturns 72                                         | YES             |
|                | print8.asm        | Prints 8 from register 0                                                   | YES             |
|                | printstr.asm      | Declares a subroutine that prints a string at a given address              | YES             |
|                | README.md         | duh                                                                        | n/a             |
|                | sctest.asm        | Code to test the Sprint Challenge                                          | YES             |
|                | stack.asm         | Stack tester                                                               | YES             |
|                | stackoverflow.asm | I guess it causes an overflow?                                             | yes?            |
| /ls8/          |
|                | cpu.py            | CPU functionality.                                                         |                 |
|                |                   |                                                                            | class CPU:      |
|                |                   |                                                                            | \* load: NO     |
|                |                   |                                                                            | \* alu: partial |
|                |                   |                                                                            | \* trace: YES   |
|                |                   |                                                                            | \* run: NO      |
|                | ls8.py            | Loads and runs the CPU class                                               | yes?            |
|                | README.md         | Instructions for this project                                              | n/a             |
| /ls8/examples/ |                   |
|                | call.ls8          | Demonstrate calls (bytecode)                                               | YES             |
|                | interrupts.ls8    | Hook the timer interrupt (bytecode)                                        | YES             |
|                | keyboard.ls8      | A simple program to test the keyboard and echo to console. (bytecode)      | YES             |
|                | mult.ls8          | Multiplies 8 and 9 and resturns 72 (bytecode)                              | YES             |
|                | print8.ls8        | Prints 8 from register 0 (bytecode)                                        | YES             |
|                | printstr.ls8      | Declares a subroutine that prints a string at a given address (bytecode)   | YES             |
|                | sctest.ls8        | Code to test the Sprint Challenge (bytecode)                               | YES             |
|                | stack.ls8         | Stack tester (bytecode)                                                    | YES             |
|                | stackoverflow.ls8 | I guess it causes an overflow? (bytecode)                                  | YES             |
