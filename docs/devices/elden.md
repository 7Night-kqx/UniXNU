# Lenovo Legion Y700 Gen 4 (elden)

A community port for SM8750P, maintained by jerry-2009.

- [jerry-2009/UNIXNU_elden](https://github.com/jerry-2009/UNIXNU_elden)

## State

TB322FC passes repeated RAM boots of the menu, 1904x3040 GOP display, volume keys and FAT payload. The format 2 configuration, live FDT, memory reservations, ADT and boot-CPU inputs pass host review.

The 4 KiB XNU kernel, prelinked `kernel.macho` and host ADT are generated and audited. The next device stage is the 56 MiB RAM payload transport, followed by DarwinBoot and XNU entry.

## Use this port

1. Read the pinned source and validation records below. Prepare the required firmware and system inputs.
2. Clone the device repository and follow its build guide from the checkout:

```sh
git clone --branch main https://github.com/jerry-2009/UNIXNU_elden.git
cd UNIXNU_elden
git checkout c591b1a0a471f24978aba25c56c8f6ec9bd06668
git submodule update --init --recursive
```

3. Complete the build for that revision, follow the [bring-up order](/porting/bring-up), and use [log capture](/porting/log-capture) to record the last confirmed stage.
4. Save results in the [porting record](/porting/records). See [Port a device](/porting/steps) for board structure and component selection.

## Sources

- [README: jerry-2009/UNIXNU_elden](https://github.com/jerry-2009/UNIXNU_elden/blob/57e68be133c407ef9fa7dc6b4f10f1bd4cd3aedd/README.md)
- [Kernel inputs: jerry-2009/UNIXNU_elden](https://github.com/jerry-2009/UNIXNU_elden/blob/57e68be133c407ef9fa7dc6b4f10f1bd4cd3aedd/docs/PHASE2.2-STATUS.md)
