# Redmi K30 Pro 变焦版（lmipro）

SM8250 社区设备移植。

- [yang232138/UniXNU-lmipro-v2](https://github.com/yang232138/UniXNU-lmipro-v2)
- [yang232138/UniXNU-lmipro](https://github.com/yang232138/UniXNU-lmipro)
- [FFT-infra/UniXNU-sm8250-common](https://github.com/FFT-infra/UniXNU-sm8250-common)

## 当前状态

格式 2 仓库选择共享 SM8250 支持、iPadOS 17.7.11 及通用 CPU、定时器、平台和密码学组件。DTS 内存区域和 splash 保留区来自该手机的 live FDT。

格式 1 内核仓库提供独立配方。固件、负载、启动镜像和外设输入仍需针对目标设备补齐并验证。

## 使用此移植

1. 阅读下方固定版本的说明和记录，准备对应的固件、系统输入与构建工具。
2. 克隆设备源码，并按其 README 准备匹配的主仓库和固件源码：

```sh
git clone --branch main https://github.com/yang232138/UniXNU-lmipro-v2.git
cd UniXNU-lmipro-v2
git checkout 07c2d714a1b02dba7264c9c0120bb66588714908
git submodule update --init --recursive
```

3. 在该版本说明指定的工作目录执行构建，核对其记录的输出和未完成输入。
4. 按[启动验证顺序](/zh/porting/bring-up)逐项确认，通过[日志抓取](/zh/porting/log-capture)保存结果，并填写[适配记录](/zh/porting/records)。板级结构和组件选择见[移植步骤](/zh/porting/steps)。

## 来源

- [README: yang232138/UniXNU-lmipro-v2](https://github.com/yang232138/UniXNU-lmipro-v2/blob/07c2d714a1b02dba7264c9c0120bb66588714908/README.md)
