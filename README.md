# ghidra-nanomips

nanoMIPS module for Ghidra.

## Setup

### Build

```console
$ ./gradlew -PGHIDRA_INSTALL_DIR=/opt/ghidra_11.0.3
```

### Install

The Gradle build task creates a ZIP file in the `dist` directory.
Install it with `File > Install Extensions` in the main Ghidra project window.


## Reference Material

* "MIPS Architecture Base: nanoMIPS32 Instruction Set Technical Reference Manual - Revision 01.01"
  * `MIPS_nanomips32_ISA_TRM_01_01_MD01247.pdf`
* "MIPS Architecture Base: 32-bit Privileged Resource Architecture Technical Reference Manual - Revision 06.09"
  * `MIPS_nanoMIPS32_PRA_06_09_MD01251.pdf`
* "MIPS Architecture Extension: nanoMIPS32 Multithreading Technical Reference Manual - Revision 1.17"
  * `MIPS_nanoMIPS32_MT_TRM_01_17_MD01255.pdf`


* "Codescape GNU tools for nanoMIPS: ELF ABI Supplement - Revision 1.3"
  * `MIPS_nanoMIPS_ABI_supplement_01_03_DN00179.pdf`


* "MIPS32 I7200 Multiprocessor Core Family - Revision 01.20"
  * `MIPS_I7200_Datasheet_01_20_MD01227.pdf`
* "MIPS32 I7200 Multiprocessing System Programmer's Guide - Revision 01.20"
  * `MIPS_I7200_Programmers_Guide_01_20_MD01232.pdf`
