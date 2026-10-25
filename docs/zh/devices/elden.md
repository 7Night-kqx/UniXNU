# 联想拯救者 Y700 四代（elden）

SM8750P 社区设备移植，由 jerry-2009 维护。

- [jerry-2009/UNIXNU_elden](https://github.com/jerry-2009/UNIXNU_elden)

## 当前状态

TB322FC 已通过菜单、1904x3040 GOP 显示、音量键和 FAT 负载的重复内存启动验证。格式 2 配置、live FDT、内存保留区、ADT 和启动 CPU 输入通过宿主机审查。

4 KiB XNU 内核、预链接的 `kernel.macho` 和宿主机 ADT 已生成并审计。下一项设备验证为 56 MiB 内存负载传输，随后验证 DarwinBoot 和 XNU 入口。

## 使用此移植

1. 阅读下方固定版本的源码说明和验证记录，准备该设备要求的固件和系统输入。
2. 克隆设备仓库，在检出目录内按其构建指南准备依赖：

```sh
git clone --branch main https://github.com/jerry-2009/UNIXNU_elden.git
cd UNIXNU_elden
git checkout c591b1a0a471f24978aba25c56c8f6ec9bd06668
git submodule update --init --recursive
```

3. 在该版本完成对应构建后，按[启动验证顺序](/zh/porting/bring-up)验证，并按[日志抓取](/zh/porting/log-capture)保存最后确认的阶段。
4. 将结果写入[移植记录](/zh/porting/records)。板级结构和组件选择见[移植设备](/zh/porting/steps)。

## 来源

- [README: jerry-2009/UNIXNU_elden](https://github.com/jerry-2009/UNIXNU_elden/blob/57e68be133c407ef9fa7dc6b4f10f1bd4cd3aedd/README.md)
- [内核输入: jerry-2009/UNIXNU_elden](https://github.com/jerry-2009/UNIXNU_elden/blob/57e68be133c407ef9fa7dc6b4f10f1bd4cd3aedd/docs/PHASE2.2-STATUS.md)
