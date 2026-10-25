# Xiaomi 13 Ultra (ishtar)

A community device port for SM8550.

- [peter8889/UniXNU-ishtar](https://github.com/peter8889/UniXNU-ishtar)
- [markakash/UniXNU-ishtar](https://github.com/markakash/UniXNU-ishtar)

## State

The peter8889 format 2 port selects shared SM8550 support and iPadOS 17.7.11. Kernel, payload and image builds pass host checks. Storage, display, input and GPU device qualification remain pending.

The independent markakash port targets XNU 11215 and iPhone XR iOS 18.7.8. Its firmware menu works on hardware; kernel patches pass application checks and the first kernel build remains pending. Use the OS inputs and firmware belonging to the selected implementation.

## Use this port

1. Read the pinned instructions and records below. Prepare the firmware, system inputs and build tools they specify.
2. Clone the device sources and prepare the matching core and firmware checkouts described by its README:

```sh
git clone --branch main https://github.com/peter8889/UniXNU-ishtar.git
cd UniXNU-ishtar
git checkout 65592496e814ede46cc89721ee792b31912d38bd
git submodule update --init --recursive
```

3. Run the build from the working directory specified by that revision's instructions. Check its documented outputs and remaining inputs.
4. Follow the [bring-up order](/porting/bring-up), save [logs](/porting/log-capture) and complete the [porting record](/porting/records). See [porting steps](/porting/steps) for board structure and component selection.

## Sources

- [README: peter8889/UniXNU-ishtar](https://github.com/peter8889/UniXNU-ishtar/blob/65592496e814ede46cc89721ee792b31912d38bd/README.md)
- [Porting record: peter8889/UniXNU-ishtar](https://github.com/peter8889/UniXNU-ishtar/blob/65592496e814ede46cc89721ee792b31912d38bd/porting.toml)
- [iOS 18 port: markakash/UniXNU-ishtar](https://github.com/markakash/UniXNU-ishtar/blob/e9ffc3f413375f11c365b7f03837ebcdb08913c5/README.md)
