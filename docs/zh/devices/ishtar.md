# 小米 13 Ultra（ishtar）

SM8550 社区设备移植。

- [peter8889/UniXNU-ishtar](https://github.com/peter8889/UniXNU-ishtar)
- [markakash/UniXNU-ishtar](https://github.com/markakash/UniXNU-ishtar)

## 当前状态

peter8889 的格式 2 移植选择共享 SM8550 支持和 iPadOS 17.7.11，内核、负载和镜像构建通过宿主机检查。存储、显示、输入和 GPU 的设备验证待完成。

独立的 markakash 移植以 XNU 11215 和 iPhone XR iOS 18.7.8 为目标，固件菜单已在实机运行，内核补丁应用检查通过，首个内核构建待完成。按所选实现使用对应的 OS 输入和固件。

## 使用此移植

1. 阅读下方固定版本的说明和记录，准备对应的固件、系统输入与构建工具。
2. 克隆设备源码，并按其 README 准备匹配的主仓库和固件源码：

```sh
git clone --branch main https://github.com/peter8889/UniXNU-ishtar.git
cd UniXNU-ishtar
git checkout 65592496e814ede46cc89721ee792b31912d38bd
git submodule update --init --recursive
```

3. 在该版本说明指定的工作目录执行构建，核对其记录的输出和未完成输入。
4. 按[启动验证顺序](/zh/porting/bring-up)逐项确认，通过[日志抓取](/zh/porting/log-capture)保存结果，并填写[适配记录](/zh/porting/records)。板级结构和组件选择见[移植步骤](/zh/porting/steps)。

## 来源

- [README: peter8889/UniXNU-ishtar](https://github.com/peter8889/UniXNU-ishtar/blob/65592496e814ede46cc89721ee792b31912d38bd/README.md)
- [适配记录: peter8889/UniXNU-ishtar](https://github.com/peter8889/UniXNU-ishtar/blob/65592496e814ede46cc89721ee792b31912d38bd/porting.toml)
- [iOS 18 移植: markakash/UniXNU-ishtar](https://github.com/markakash/UniXNU-ishtar/blob/e9ffc3f413375f11c365b7f03837ebcdb08913c5/README.md)
