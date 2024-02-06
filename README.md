# ghidra-nanomips

nanoMIPS module for Ghidra.

## Setup

### Build

```console
$ ./gradlew -PGHIDRA_INSTALL_DIR=/opt/ghidra_11.0.1
```

### Install

The Gradle build task creates a ZIP file in the `dist` directory.
Install it with `File > Install Extensions` in the main Ghidra project window.
