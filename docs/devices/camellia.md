# Redmi Note 10 5G (camellia)

A community device port for MT6833.

- [stanveyjiang/UniXNU-camellia](https://github.com/stanveyjiang/UniXNU-camellia)

## State

The board provides a bootstrap defconfig, iPadOS 17.7.11 identity, prelink roots and a diagnostic package for MT6833 early boot. The kernel recipe reuses shared prelink and diagnostic helpers.

Target firmware, native storage, display, input, GPU and power integration require their own build and device records. Use the device README for the bootstrap kernel inputs.

## Use this port

1. Read the pinned instructions and records below. Prepare the firmware, system inputs and build tools they specify.
2. Clone the device sources and prepare the matching core and firmware checkouts described by its README:

```sh
git clone --branch main https://github.com/stanveyjiang/UniXNU-camellia.git
cd UniXNU-camellia
git checkout 7b83a3b41e4ae906130837cac37fdd718a258e4b
git submodule update --init --recursive
```

3. Run the build from the working directory specified by that revision's instructions. Check its documented outputs and remaining inputs.
4. Follow the [bring-up order](/porting/bring-up), save [logs](/porting/log-capture) and complete the [porting record](/porting/records). See [porting steps](/porting/steps) for board structure and component selection.

## Sources

- [README: stanveyjiang/UniXNU-camellia](https://github.com/stanveyjiang/UniXNU-camellia/blob/7b83a3b41e4ae906130837cac37fdd718a258e4b/README.md)
