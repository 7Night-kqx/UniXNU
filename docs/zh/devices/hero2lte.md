# 三星 Galaxy S7 Edge（hero2lte）

Exynos 8890 社区设备移植。

- [DokuroMitsukai/UniXNU-hero2lte](https://github.com/DokuroMitsukai/UniXNU-hero2lte)
- [DokuroMitsukai/UniXNU-exynos8890-common](https://github.com/DokuroMitsukai/UniXNU-exynos8890-common)

## 当前状态

格式 2 设备树选择共享 Exynos 8890 支持，包含 GIC-400、PSCI 和 26 MHz 定时器，当前启用 CPU0。Mu-Silicium 固件可构建，固件卷包含 UniXNU、内存负载驱动和 DarwinBoot，BootShim 与按键宿主机检查通过。

实机启动和负载验证待完成。所选 ArmCpu 路径需要补齐 GICv2 支持后才能启动 XNU，存储、显示、输入和电源驱动需要板级集成。

## 使用此移植

1. 阅读下方固定版本的说明和记录，准备对应的固件、系统输入与构建工具。
2. 克隆设备源码，并按其 README 准备匹配的主仓库和固件源码：

```sh
git clone --branch main https://github.com/DokuroMitsukai/UniXNU-hero2lte.git
cd UniXNU-hero2lte
git checkout 53ccc853aefa388215504ddc75ca8f602917e6e3
git submodule update --init --recursive
```

3. 在该版本说明指定的工作目录执行构建，核对其记录的输出和未完成输入。
4. 按[启动验证顺序](/zh/porting/bring-up)逐项确认，通过[日志抓取](/zh/porting/log-capture)保存结果，并填写[适配记录](/zh/porting/records)。板级结构和组件选择见[移植步骤](/zh/porting/steps)。

## 来源

- [README: DokuroMitsukai/UniXNU-hero2lte](https://github.com/DokuroMitsukai/UniXNU-hero2lte/blob/53ccc853aefa388215504ddc75ca8f602917e6e3/README.md)
