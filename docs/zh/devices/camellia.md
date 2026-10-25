# Redmi Note 10 5G（camellia）

MT6833 社区设备移植。

- [stanveyjiang/UniXNU-camellia](https://github.com/stanveyjiang/UniXNU-camellia)

## 当前状态

板级仓库提供 MT6833 早期启动所需的 bootstrap defconfig、iPadOS 17.7.11 身份、预链接根和诊断包，内核配方复用共享预链接与诊断工具。

目标固件、原生存储、显示、输入、GPU 和电源集成仍需各自的构建及设备记录。bootstrap 内核输入按设备 README 准备。

## 使用此移植

1. 阅读下方固定版本的说明和记录，准备对应的固件、系统输入与构建工具。
2. 克隆设备源码，并按其 README 准备匹配的主仓库和固件源码：

```sh
git clone --branch main https://github.com/stanveyjiang/UniXNU-camellia.git
cd UniXNU-camellia
git checkout 7b83a3b41e4ae906130837cac37fdd718a258e4b
git submodule update --init --recursive
```

3. 在该版本说明指定的工作目录执行构建，核对其记录的输出和未完成输入。
4. 按[启动验证顺序](/zh/porting/bring-up)逐项确认，通过[日志抓取](/zh/porting/log-capture)保存结果，并填写[适配记录](/zh/porting/records)。板级结构和组件选择见[移植步骤](/zh/porting/steps)。

## 来源

- [README: stanveyjiang/UniXNU-camellia](https://github.com/stanveyjiang/UniXNU-camellia/blob/7b83a3b41e4ae906130837cac37fdd718a258e4b/README.md)
