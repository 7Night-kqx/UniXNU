# Redmi K30 Pro Zoom Edition (lmipro)

A community device port for SM8250.

- [yang232138/UniXNU-lmipro-v2](https://github.com/yang232138/UniXNU-lmipro-v2)
- [yang232138/UniXNU-lmipro](https://github.com/yang232138/UniXNU-lmipro)
- [FFT-infra/UniXNU-sm8250-common](https://github.com/FFT-infra/UniXNU-sm8250-common)

## State

The format 2 repository selects shared SM8250 support, iPadOS 17.7.11 and generic CPU, timer, platform and crypto components. Its DTS memory banks and splash reservations come from the handset's live FDT.

The format 1 kernel repository provides a separate format 1 recipe. Firmware, payload, boot-image and peripheral inputs remain to be completed and qualified for the target device.

## Use this port

1. Read the pinned instructions and records below. Prepare the firmware, system inputs and build tools they specify.
2. Clone the device sources and prepare the matching core and firmware checkouts described by its README:

```sh
git clone --branch main https://github.com/yang232138/UniXNU-lmipro-v2.git
cd UniXNU-lmipro-v2
git checkout 07c2d714a1b02dba7264c9c0120bb66588714908
git submodule update --init --recursive
```

3. Run the build from the working directory specified by that revision's instructions. Check its documented outputs and remaining inputs.
4. Follow the [bring-up order](/porting/bring-up), save [logs](/porting/log-capture) and complete the [porting record](/porting/records). See [porting steps](/porting/steps) for board structure and component selection.

## Sources

- [README: yang232138/UniXNU-lmipro-v2](https://github.com/yang232138/UniXNU-lmipro-v2/blob/07c2d714a1b02dba7264c9c0120bb66588714908/README.md)
