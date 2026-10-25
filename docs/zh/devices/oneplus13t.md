# 一加 13T（oneplus13t）

搭载 SM8750 的社区设备移植。当前状态依据下方固定版本的维护者记录。

| 仓库 | 维护者 |
| --- | --- |
| [UniXNU-Pagani_SM8750](https://github.com/IssacL04/UniXNU-Pagani_SM8750) | [IssacL04](https://github.com/IssacL04) |
| [UniXNU-sm8750-common](https://github.com/IssacL04/UniXNU-sm8750-common) | [IssacL04](https://github.com/IssacL04) |
| [UniXNU-Pagani-Drivers](https://github.com/IssacL04/UniXNU-Pagani-Drivers) | [IssacL04](https://github.com/IssacL04) |

## 当前状态

已验证的实机配置可通过 UFS 读取根卷并使用 CPU 帧缓冲呈现 iPadOS 界面，Data 使用易失的内存种子。

格式 2 内核、固件、负载和镜像通过宿主机构建。当前源码包含 S3910 触控、物理按键及 DSI 亮度/显示关闭，内核链接、预链接和 HID/背光 ABI 检查通过。迁移后的镜像和这些外设改动待实机验证，GPU、网络、音频和完整电源管理待完成。

## 来源

- [README: IssacL04/UniXNU-Pagani_SM8750](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/fcab49e2ea2f9ddfaa08ee6e8109ba7ed67029ac/README.md)

## 双系统存储

以下布局来自 256 GB 型号的实测记录。

| 项目 | 采集值 |
| --- | --- |
| Recovery 内核 | `6.6.118-android15-8-o-g4d611c32bedc-enc3l-4k` |
| 磁盘 / 逻辑扇区 | `/dev/block/sda` / 4096 字节 |
| 剩余 userdata | 分区 15，LBA 4020972 到 44928767 |
| UniXNU 分区 | 分区 16，LBA 44928768 到 61705983 |
| F2FS 缩容请求 / 预期结果 | 40907264 / 40907535 个 4096 字节块 |

按[双系统分区指南](/zh/porting/dual-system-partition)计算并检查目标布局。选择分区边界前先测量所连接的设备。

## 使用此移植

1. 阅读上方仓库的构建说明和固定版本记录，准备对应的固件、系统镜像和板级输入。
2. 按该仓库的命令构建，通用配置见[构建与启动](/zh/building)。
3. 按[启动验证顺序](/zh/porting/bring-up)逐项验证，通过[日志抓取](/zh/porting/log-capture)保存结果。
4. 更新[移植记录](/zh/porting/records)，记录实际使用的源码版本及最后确认的阶段。
