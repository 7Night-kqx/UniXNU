# Samsung Galaxy S7 Edge (hero2lte)

A community device port for Exynos 8890.

- [DokuroMitsukai/UniXNU-hero2lte](https://github.com/DokuroMitsukai/UniXNU-hero2lte)
- [DokuroMitsukai/UniXNU-exynos8890-common](https://github.com/DokuroMitsukai/UniXNU-exynos8890-common)

## State

The format 2 tree selects shared Exynos 8890 support: GIC-400, PSCI and the 26 MHz timer, with CPU0 enabled. Mu-Silicium firmware builds with UniXNU, the RAM payload driver and DarwinBoot in the firmware volume. BootShim and keypad host checks pass.

Hardware boot and payload validation remain pending. The selected ArmCpu path needs GICv2 support before XNU startup; storage, display, input and power drivers require board integration.

## Use this port

1. Read the pinned instructions and records below. Prepare the firmware, system inputs and build tools they specify.
2. Clone the device sources and prepare the matching core and firmware checkouts described by its README:

```sh
git clone --branch main https://github.com/DokuroMitsukai/UniXNU-hero2lte.git
cd UniXNU-hero2lte
git checkout 53ccc853aefa388215504ddc75ca8f602917e6e3
git submodule update --init --recursive
```

3. Run the build from the working directory specified by that revision's instructions. Check its documented outputs and remaining inputs.
4. Follow the [bring-up order](/porting/bring-up), save [logs](/porting/log-capture) and complete the [porting record](/porting/records). See [porting steps](/porting/steps) for board structure and component selection.

## Sources

- [README: DokuroMitsukai/UniXNU-hero2lte](https://github.com/DokuroMitsukai/UniXNU-hero2lte/blob/53ccc853aefa388215504ddc75ca8f602917e6e3/README.md)
