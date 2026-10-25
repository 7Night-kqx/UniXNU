# Xiaomi Mi 8 SE (sirius)

Xiaomi Mi 8 SE (sirius) is a SDM710 device. The port below is an independent community project. The UniXNU organization does not maintain it.

| Repository | Maintainer |
| --- | --- |
| [UniXNU-sirius](https://github.com/57UU/UniXNU-sirius) | [57UU](https://github.com/57UU) |
| [UniXNU-sdm710-common](https://github.com/57UU/UniXNU-sdm710-common) | [57UU](https://github.com/57UU) |

## State

The format 2 port selects shared SDM710 support. U-Boot UEFI, the payload, XNU entry probes, MMU, the 19.2 MHz timer, PSCI reset and the panel console have device results.

IOKit currently selects AppleARMCPU from the kernelcache, which panics in `_validateConfiguration()`. Native ArmCpu matching and the eMMC root driver remain pending.

## Maintenance

The maintainer owns the repository and its release decisions. UniXNU documentation lists the port and its state; it does not take over maintenance.

## Sources

- [README: 57UU/UniXNU-sirius](https://github.com/57UU/UniXNU-sirius/blob/e51069a970f81a3c48588041a0caa3087a1ebbbc/README.md)
