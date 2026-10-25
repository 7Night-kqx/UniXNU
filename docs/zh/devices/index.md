# 设备

每个条目记录板级或虚拟目标、维护源码及报告的构建与启动结果。共享 SoC 的设备分别记录各自的板级配置和外设。

## 选择和使用设备

1. 在下方列表打开目标设备，确认产品型号、SoC 和维护仓库。
2. 阅读设备页面的输入、当前结果和未完成部分；使用它指定的固件、OS profile 和分区值。
3. 构建该移植时按[构建与启动](/zh/building)操作；适配新硬件时按[移植设备](/zh/porting/steps)操作；更新仓库格式时按[迁移指南](/zh/porting/migration)操作。
4. 按设备记录的检查点验证，保存实际使用的源码、固件和镜像版本。

## 组织维护的设备

| 设备 | SoC | 支持功能 | 设备仓库 | 固件 |
| --- | --- | --- | --- | --- |
| 小米平板 6S Pro（sheng） | SM8550 | [各部分的实现与证据](/zh/devices/sheng) | [UniXNU-sheng](https://github.com/UniXNU/UniXNU-sheng) | [uefi-sheng](https://github.com/UniXNU/uefi-sheng) |

## 社区移植

社区移植由表中维护者独立维护。各页面区分源码、宿主机构建和设备运行结果，并链接对应记录。检索覆盖 UniXNU 组织、`unixnu` topic、名称或描述包含 UniXNU 的公开仓库，以及已收录的源码链接。仓库收录依据目标板级配置和实现。

| 设备 | SoC | 状态 | 维护者 |
| --- | --- | --- | --- |
| [DroidVM 客户机（Gunyah 上的 crosvm）](/zh/devices/droidvm) | crosvm-gunyah | iPadOS 17 主屏幕，Metal widget 和图标，Keychain 和蓝牙，virtio-net 工作 | Droid-VM |
| [QEMU virt](/zh/devices/qemu) | QEMU virt | iPadOS 17 主屏幕和 Settings；使用 `--metal` 时在 Mac GPU 上运行 Metal | xVanTuring |
| [联想小新 Pad 2022（tb128fu）](/zh/devices/tb128fu) | SM6225 | 已到 iPadOS 17 主屏幕，触控可用；Metal 帧由 GPU 呈现；Adreno 610 已运行 | xVanTuring |
| [Galaxy Tab S7 FE Wi-Fi（SM-T733）](/zh/devices/sm-t733) | SM7325 | 桌面、触控、按键、亮度、关机、USB 诊断和持久化 Data 可用 | RigoLigoRLC |
| [一加 10 Pro 5G（negroni）](/zh/devices/negroni) | SM8450 | SpringBoard 和触控可用，独立 iOSPlus10 工作区记录了 Metal 合成结果 | pawlickerr, akshaynexus |
| [Nothing Phone (2)（pong）](/zh/devices/pong) | SM8475 | 已到 iOS 16.6.1 主屏幕，显示和触控可用；UFS 和 GPU 部分可用 | Chengdong-Yu |
| [小米 17 Pro（pandora）](/zh/devices/pandora) | SM8850 | GPU 合成界面、应用、触控和 CPU 调频可用，音频与网络待完成 | ShueiTsuki |
| [小米 8 SE（sirius）](/zh/devices/sirius) | SDM710 | 平台和屏幕控制台已运行，AppleARMCPU 匹配 panic，eMMC 待完成 | 57UU |
| [小米 13（fuxi）](/zh/devices/fuxi) | SM8550 | 内核可链接和预链接，阶段 B archive 链接近完成，未在真机运行 | matejkoo217, hanzi123-bilp, 0721GPT |
| [一加 7 Pro（guacamole）](/zh/devices/guacamole) | SM8150 | 已到达 iOS 16.7.16 用户态，GPU 待完成 | wochgn |
| [一加 Ace 5（giulia）](/zh/devices/giulia) | SM8650 | Hello/设置、显示、触控和按键可用，GPU、Wi-Fi 和音频待完成 | tycykp |
| [小米 10（umi）](/zh/devices/umi) | SM8250 | iPadOS 17.7.11 Hello／设置，触摸可用；CPU 显示、UFS 和持久化 Data | reAAAq |
| [小米 MIX 2（chiron）](/zh/devices/chiron) | SDM835 | 真机运行最小 4 KiB XNU 和 PID 1 心跳 | to-mid |
| [小米平板 7 / POCO Pad X1（uke）](/zh/devices/uke) | SM7675 | Apple 标志和早期用户态已运行，重启原因待查 | Allenwdk |
| [POCO X7 / Redmi Note 14 Pro 5G（malachite）](/zh/devices/malachite) | MT6878 | UEFI正常工作，UFS正常，XNU rootfs已加载，USB、触控等未实现 | ghidgdsr |
| [Brave Ark 平板（braveark）](/zh/devices/braveark) | SM8635 | 8 核 XNU BSD init；iPadOS 根卷进行中 | tattwamashi |
| [小米平板 8 Pro（piano）](/zh/devices/piano) | SM8750 | 内核在 CI 编译并预链接，未在平板上运行 | code002-2 |
| [小米 13 Pro（nuwa）](/zh/devices/nuwa) | SM8550 | 实机 XNU 已输出 IODTNVRAM，重启原因待查 | wh1stl3 |
| [一加 13T（oneplus13t）](/zh/devices/oneplus13t) | SM8750 | 实机基线已验证界面，格式 2 与外设构建待设备验证 | IssacL04 |
| [一加平板 2 Pro（erhai）](/zh/devices/erhai) | SM8750 | XNU 入口 bring-up，根和用户态未配置 | wally001012-cyber |
| [OPPO Find X7 Ultra（PHY120）](/zh/devices/phy120) | SM8650 | 启动管理器菜单工作，内核在 CI 构建 | peiyuesheng666 |
| [Sony Xperia 1 II（pdx203）](/zh/devices/pdx203) | SM8250 | 内核在 CI 编译并预链接；未启动 | chardidathing |
| [Moto Z2 Force（nash）](/zh/devices/nash) | MSM8998 | 板级配置和早期 ARM 补丁已提供，目标设备实机证据待发布 | fcxuhaq3 |
| [Redmi K40 Pro（haydn）](/zh/devices/haydn) | SM8350 | 固件、负载和启动镜像已构建，haydn4 从 guacamole 导入 | xiaomi-haydn-dev |
| [小米平板 5（nabu）](/zh/devices/nabu) | SM8150 | launchd exec 返回 ENOENT，Linux 内核构建可用 | Lux12138 |
| [一加 6T（fajita）](/zh/devices/fajita) | SDM845 | XNU 已到根挂载，无存储驱动 | johnpanos |
| [小米 8（dipper）](/zh/devices/dipper) | SDM845 | UEFI、菜单和负载；XNU 到 BSD init，无根卷 | hanyaa380 |
| [Microsoft Surface Duo 2（zeta）](/zh/devices/zeta) | SM8350 | APFS 根卷和重写后的 PID 1 已运行，共享缓存指针异常待解决 | none24smu |
| [一加 Ace 5 Pro（hummer）](/zh/devices/hummer) | SM8750 | Hello、六核和物理根卷已运行，触控和 GPU 待完成 | 2426120557 |
| [小米 10 Ultra（cas）](/zh/devices/cas) | SM8250 | UEFI 和 UniXNU 菜单已验证，DarwinBoot 和 XNU 未测试 | ht94911 |
| [小米 15（dada）](/zh/devices/dada) | SM8750 | UEFI 工作；UFS UIC 和 MCQ 探针；UniXNU 和 XNU 未运行 | 7Night-kqx |
| [Redmi Note 14 Pro+ 5G（amethyst）](/zh/devices/amethyst) | SM7635 | 内核和负载准备已提供，目标 UEFI 集成待完成 | andr0d1v |
| [Redmi K90 Pro Max / Poco F8 Ultra（myron）](/zh/devices/myron) | SM8850 | 核心和驱动分支，设备仓库与真机结果待完成 | zg7681 |
| [Redmi K70（vermeer）](/zh/devices/vermeer) | SM8550 | 平台内核 CI 通过，实机 UEFI 菜单已验证 | mansar1337、yyx2025、wuan0039、xyyyds0106 |
| [努比亚红魔 8 Pro / 8 Pro+（nx729j）](/zh/devices/nx729j) | SM8550 | 实机 UEFI 和屏幕日志已验证，XNU/根卷结果待确认 | 2713385115 |
| [小米平板 6（pipa）](/zh/devices/pipa) | SM8250 | 实机 XNU 已启动，根卷挂载失败，存储集成待完成 | xVanTuring |
| [Galaxy Tab A7 10.4（gta4l）](/zh/devices/gta4l) | SM6115 | 板级、ADT 和固件可构建，第二个仓库在 CI 构建内核 | NoNameBuilder、ilovemykedi |
| [Redmi Note 10 Pro（sweet）](/zh/devices/sweet) | SM7150 | 独立 iOS 16 移植记录了 UFS、用户态和显示结果，GPU 加速待完成 | CrackerCat, zeroninevibedslop |
| [小米 MIX 2S（polaris）](/zh/devices/polaris) | SDM845 | 平台阶段真机已验证：固件、UniXNU、DarwinBoot 与源码内核直达 BSD/IOKit；尚无根文件系统 | luuu20309 |
| [一加 5（cheeseburger）](/zh/devices/cheeseburger) | MSM8998 | 根卷、PID 1 和内存 Data 已运行，正在调查 watchdogd SIGTRAP | DinnerABC, lss717 |
| [Redmi K20 Pro / Mi 9T Pro（raphael）](/zh/devices/raphael) | SM8150 | 公开源码访问待恢复，当前构建与设备状态待确认 | penYo22 |
| [Galaxy Z Fold3（q2q）](/zh/devices/q2q) | SM8350 | 仅源码内核构建工具 | agcarbajo |
| [Redmi K30 5G（picasso）](/zh/devices/picasso) | SM7250 | XNU BSD 初始化和 APFS 注册完成，等待根设备 | YinCQL |
| [Redmi Note 9（merlinx）](/zh/devices/merlinx) | MT6768 | UEFI 可启动，自定义菜单工作；存储初始化阻塞 UniXNU 和 XNU | Dracen-W |
| [小米平板 4 LTE（clover）](/zh/devices/clover) | SDM660 | eMMC mockfs 根卷和 EL0 测试 init 已运行，APFS 探针开发中 | qine233 |
| [Benesse TAB-A04-BR3（a04br3）](/zh/devices/a04br3) | MT8167 | 主屏幕、四核和 eMMC DMA 已运行，Vulkan 传输与读回可用 | mouseos |
| [Redmi 9A（dandelion）](/zh/devices/dandelion) | MT6765 | 早期 bring-up，UEFI 移植进行中 | licg89 |
| [小米 6（sagit）](/zh/devices/sagit) | MSM8998 | 公开源码访问待恢复，当前构建与设备状态待确认 | dmnakzkahziamnk-a11y |
| [Redmi Note 12 Turbo / POCO F5（marble）](/zh/devices/marble) | SM7475 | 维护者报告 Hello，触控和公开可复现源码待完成 | sing0626 |
| [小米 10S（thyme）](/zh/devices/thyme) | SM8250-AC | 实测板级输入和早期跟踪代码已提供，实机启动证据待发布 | tobyfox1640, Coryyi |
| [Redmi K80 Ultra（dali）](/zh/devices/dali) | MT6991 | 单核 XNU 早期启动；根卷和用户态不在当前阶段 | localhosts-A |
| [中兴努比亚 Z60 Ultra（nx721j）](/zh/devices/nx721j) | Pineapple | Pineapple 内核和被动 UFS 探针，设备启动待验证 | SangLuoCN |
| [Unisoc UMS512 / T610YP](/zh/devices/t610yp) | UMS512 | 板级、内核配置和 ADT；无真机结果 | hxzbaka |
| [Google Pixel 9 Pro XL（komodo）](/zh/devices/komodo) | Tensor G4 | 实机菜单和参考内核入口探针已验证，原生平台待完成 | Trijal08 |
| [小米 9（cepheus）](/zh/devices/cepheus) | SDM855 | 设备仓库和启动链已准备；无真机结果 | sxl47 |
| [小米 MIX Flip（ruyi）](/zh/devices/ruyi) | SM8650 | 板级、内核配置和固件仓库已提供，实机结果待发布 | ArnoDorian123 |
| [小米 Civi 5 Pro（luming）](/zh/devices/luming) | SM8735 | 实测输入和宿主机 ADT 检查已完成，内核及固件构建待完成 | infinityEX-RSXQ |
| [小米平板 6 Pro（liuqin）](/zh/devices/liuqin) | SM8475 | 板级、defconfig 和内核 USB 调试口；下一步 UEFI | 1696108518, boomoodxf |
| [小米平板 5 Pro 5G（enuma）](/zh/devices/enuma) | SM8250-AC | 宿主机镜像检查和 EL1 读取诊断已完成，可见菜单待验证 | wh1stl3, Tlrenhb |
| [Redmi Turbo 3 / Poco F6（peridot）](/zh/devices/peridot) | SM8635 | WIP 设备仓库；无真机结果 | kvfsrl, hoshikv, wzy114514sb |
| [一加 8 Pro（instantnoodlep）](/zh/devices/instantnoodlep) | SM8250 | UEFI 平台和内核基线；状态未记录 | zhangp996 |
| [一加 8T（kebab）](/zh/devices/kebab) | SM8250 | HFS 根卷和静态 EL0 测试 init 已运行，完整 iOS 用户态待完成 | GFander |
| [一加 6（enchilada）](/zh/devices/enchilada) | SDM845 | 设备仓库；状态未记录 | keyfan |
| [一加 15T（fairlady）](/zh/devices/fairlady) | SM8850 | 早期移植，带 S1 到 S6 诊断；无真机结果 | Osilvfe |
| [一加平板 Pro（caihong）](/zh/devices/caihong) | SM8650 | APFS 恢复内存根卷和 launchd 已运行，显示和完整系统根卷待完成 | Axiang-dev |
| [Nothing Phone (3a)（asteroids）](/zh/devices/asteroids) | SM7635 | 八核、UFS 根卷和用户态已运行，显示呈现待完成 | rootstockos |
| [Galaxy Tab S9 Ultra Wi-Fi（gts9uwifi）](/zh/devices/gts9uwifi) | SM-X910 | 设备仓库；状态未记录 | zc47796741-pixel |
| [Moto G9 Play（guamp）](/zh/devices/guamp) | SM6115 | UEFI 菜单可启动；内核未构建 | itsChris122 |
| [Moto G 5G（gauguin）](/zh/devices/gauguin) | SM7125 | 设备仓库；状态未记录 | lvyufeng |
| [Microsoft Lumia 950](/zh/devices/lumia950) | MSM8992 | 设备仓库；使用手机自带 UEFI；未启动 | ManGuy-Legend |
| [OPPO R11（r11）](/zh/devices/r11) | SDM660 | 板级、defconfig 和硬件笔记；状态未记录 | huhaitao1136-cpu |
| [OPPO Find X9（x9）](/zh/devices/x9) | MT6993 | 未到 UEFI；约 25 到 30% | tosasitill |
| [Unisoc 设备](/zh/devices/unisoc) | Unisoc | 核心分支；尚无具体设备移植 | hxzbaka |
| [unixnu-build](/zh/devices/unixnu-build) | 构建树 | 仅构建树；设备未记录 | iskssksjjsjjzjs |
| [sheng 上的 macOS](/zh/devices/sheng-macos) | SM8550 | sheng 实机运行 macOS 26.5 launchd，图形 Recovery 待完成 | Jelly10086 |
| [Redmi K40（alioth）](/zh/devices/alioth) | SM8250-AC | 格式 2 板级、DTS 和 SM8250 共享支持，内核及镜像集成待完成 | FFT-infra, fjcx555 |
| [联想小新 Pad Pro 2021（j716f）](/zh/devices/j716f) | SM8250 | XNU 入口和 MMU 后探针已运行，重启诊断进行中 | Denis0x00 |
| [联想拯救者 Y700 四代（elden）](/zh/devices/elden) | SM8750P | 固件实机检查和 XNU 预链接构建已完成，XNU 启动待验证 | jerry-2009 |
| [小米平板 5 Pro Wi-Fi（elish）](/zh/devices/elish) | SM8250-AC | 板级骨架通过静态检查，实测输入和固件待完成 | hpadmx |
| [Redmi K80（zorn）](/zh/devices/zorn) | SM8650-AB | 只读 UFS APFS 根卷已挂载，用户映射停在 MEND | kerrinz |
| [一加 9R（lemonades）](/zh/devices/lemonades) | SM8250-AC | 固件可在 Linux 构建，板级和负载准备中，实机检查待完成 | soooink |
| [魅族 20 Classic（m2381）](/zh/devices/m2381) | SM8550 | 板级配置和固件覆盖层已提供，内核及预链接适配中 | RiverKawa271828 |
| [小米 13 Ultra（ishtar）](/zh/devices/ishtar) | SM8550 | 镜像宿主机构建通过，独立 iOS 18 移植已验证实机 UEFI 菜单 | peter8889, markakash |
| [三星 Galaxy S7 Edge（hero2lte）](/zh/devices/hero2lte) | Exynos 8890 | 集成固件可构建，GICv2 和实机启动待完成 | DokuroMitsukai |
| [一加 Ace 2 / 11R（udon）](/zh/devices/udon) | SM8475 | UFS 根卷和 117 进程用户态已运行，界面诊断进行中 | takasugl |
| [Redmi Note 10 5G（camellia）](/zh/devices/camellia) | MT6833 | 启动板级配置和内核配方已提供，硬件验证待完成 | stanveyjiang |
| [小米 14（houji）](/zh/devices/houji) | SM8650 | 桌面、八核、UFS/HFSX 和触控可用，GPU 提交待完成 | lonzzi |
| [Redmi K30 Pro 变焦版（lmipro）](/zh/devices/lmipro) | SM8250 | 格式 2 板级和实测 DTS 已提供，当前流程以内核为主 | yang232138 |
| [Rongyue E5（e5）](/zh/devices/e5) | UMS9621 | 格式 2 UMS9621 配置和早期入口/MMU 探针已提供 | Enceka |

## 设备页面记录什么

| 项目 | 示例 |
| --- | --- |
| 板级身份 | 产品名、SoC、代号 |
| IPSW | 产品、版本、build、device class、chip 和 board ID |
| 分区几何 | `first_lba`、`last_lba`、块大小 |
| 内核预链接 | slide、roots、早期安全初始化器、kernelcache 固定 |
| 固件 | Mu-Silicium 配置、DSC、固件卷路径、defines |
| 负载 | 卷标、大小、DRAM 大小、内核参数 |
| ADT | 生成脚本、身份、CPU 寄存器、PSCI 方法 |
| 设备树追加 | 给原有 bootloader 的 reserved-memory 节点 |
| 构建命令 | 实际驱动命令 |
| 启动命令 | 实际 fastboot 命令 |
| 观察状态 | 已在设备上运行过的阶段 |

## 新增设备

1. 按[移植](/zh/porting/steps)操作。
2. 创建设备仓库和 UEFI 仓库。
3. 分阶段构建和 bring-up。
4. 在 `docs/zh/devices/` 下新增页面，记录数值和命令。
5. 把设备加入上表。

设备页面是板级数值的位置。通用指南使用占位符并链接到这里。

## sheng

[sheng 页面](/zh/devices/sheng)记录小米平板 6S Pro 移植。它是一个设备条目。[Novatek 触控驱动](/zh/drivers/sheng-novatek-touch)把 sheng 的触控驱动作为内置 XNU 驱动的完整示例。

官方设备页由设备仓库的 `porting.toml` 生成，更新流程见[适配记录](/zh/porting/records)。
