# 小米 8 SE（sirius）

小米 8 SE（sirius） 是搭载 SDM710 的设备。下面的移植是独立的社区项目，UniXNU 组织不维护它。

| 仓库 | 维护者 |
| --- | --- |
| [UniXNU-sirius](https://github.com/57UU/UniXNU-sirius) | [57UU](https://github.com/57UU) |
| [UniXNU-sdm710-common](https://github.com/57UU/UniXNU-sdm710-common) | [57UU](https://github.com/57UU) |

## 当前状态

格式 2 移植选择共享 SDM710 支持。U-Boot UEFI、负载、XNU 入口探针、MMU、19.2 MHz 定时器、PSCI 重启和屏幕控制台已有实机记录。

IOKit 当前选择了 kernelcache 中的 AppleARMCPU，并在 `_validateConfiguration()` 中 panic。原生 ArmCpu 匹配和 eMMC 根卷驱动待完成。

## 维护

维护者拥有仓库和发布决定。UniXNU 文档记录移植及其状态，不接管维护。

## 来源

- [README: 57UU/UniXNU-sirius](https://github.com/57UU/UniXNU-sirius/blob/e51069a970f81a3c48588041a0caa3087a1ebbbc/README.md)
