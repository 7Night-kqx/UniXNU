# 三星 Galaxy S7 Edge（hero2lte）

[DokuroMitsukai/UniXNU-hero2lte](https://github.com/DokuroMitsukai/UniXNU-hero2lte)

<div v-pre>

Samsung Galaxy S7 Edge \(SM-G935F\) on Exynos 8890. Phase 1 is a Mu-Silicium UEFI firmware with display and keypad input. XNU requires GICv2 support in ArmCpu, native storage, display, input and power drivers, and verified EFS/CPEFS backups before any wipe.

源记录: [porting.toml](https://github.com/DokuroMitsukai/UniXNU-hero2lte/blob/53ccc853aefa388215504ddc75ca8f602917e6e3/porting.toml), `53ccc853aefa388215504ddc75ca8f602917e6e3`.

本页按设备记录自动生成。

| 部分 | 状态 |
| --- | --- |
| [配置](#configuration) | `host-verified` |
| [固件与启动](#firmware) | `host-verified` |
| [CPU 与中断](#cpu) | `planned` |
| [内存与 DMA](#memory) | `planned` |
| [存储与根卷](#storage) | `planned` |
| [显示](#display) | `planned` |
| [输入](#input) | `planned` |
| [GPU](#gpu) | `planned` |
| [网络](#network) | `planned` |
| [音频](#audio) | `planned` |
| [电源](#power) | `planned` |
| [镜像组装](#packaging) | `planned` |
| [诊断](#diagnostics) | `planned` |

## 配置 {#configuration}

`host-verified`

### 硬件与依赖

- SM-G935F \(hero2lte\), Exynos 8890, bootloader G935FXXS6ESI4, framebuffer at 0xE2A00000.
- iPadOS 17.7.11 build 21H461 is the only OS profile in this UniXNU revision.

### 配置

- board.soc = Exynos 8890; board.soc\_source = exynos8890; board.os\_profile = ipados-17.7.11-21H461; schema\_version = 2.
- Firmware paths select the DokuroMitsukai/Mu-Silicium hero2lte package and the five Mu\_Basecore patches that package requires.

### 操作步骤

- Run ./unixnu defconfig hero2lte\_defconfig -D ../UniXNU-hero2lte from UniXNU.
- Run ./unixnu fetch -D ../UniXNU-hero2lte to resolve base sources and write unixnu.lock.
- Run ./unixnu status --json -D ../UniXNU-hero2lte and review profiles, components, source pins and patch order.

### 开发经验

- The ARM64, SoC, OS and device tables merge in that order. Ordinary arrays replace inherited arrays, so board.toml repeats the complete component, fragment and patch-series lists.
- The SM-G935F keeps TWRP on RECOVERY. No configuration step touches that partition.

### 完成条件

- All source pins resolve; every selected component has an area; status shows the intended profiles and patch order.

### 当前范围

- The published SoC feed is pinned in feeds.toml and unixnu.lock; fetch succeeds without a local source override.
- No hardware checkpoint exists for this board.

### 下一步

- Keep the published SoC revision synchronized between feeds.toml and unixnu.lock.

### 证据

- `source`: [Board identity, component selection, firmware paths and boot image parameters](https://github.com/DokuroMitsukai/UniXNU-hero2lte/blob/53ccc853aefa388215504ddc75ca8f602917e6e3/board.toml)
- `host`: [schema\_version 2 resolved the arch, exynos8890, iPadOS and device profiles with the selected components and patch series](https://github.com/DokuroMitsukai/UniXNU-hero2lte/blob/53ccc853aefa388215504ddc75ca8f602917e6e3/unixnu.lock)
  Command: <code>./unixnu status --json -D ../UniXNU-hero2lte</code>. Revision: `e9fb02f99c4cc2e6c882b1c2b6443fd342bc85e0`.

## 固件与启动 {#firmware}

`host-verified`

组件: `DarwinBoot`.

### 硬件与依赖

- Mu-Silicium hero2lte firmware, S-Boot framebuffer at 0xE2A00000 with size 0xE10000, UEFI FD base 0xC9000000 and size 0x200000.
- Firmware version G935FXXS6ESI4 and the five Mu\_Basecore patches used by the package.

### 配置

- firmware.config = hero2lte; DSC = Platforms/Samsung/hero2ltePkg/hero2lte.dsc; FD = Build/hero2ltePkg/&\#123;target&\#125;\_CLANGPDB/FV/SILICIUM\_UEFI.fd.
- The package list mirrors the working Mu-Silicium build and adds &\#123;tree&\#125;/package and &\#123;tree&\#125;/drivers/DarwinBoot for UniXNU.

### 操作步骤

- The standalone build runs ./build-hero2lte.sh -c at the workspace root; test\_bootshim.py and test\_hero2lte\_keypad.py pass.
- The DSC and DXE.inc add UniXNU.inf, UniXNUDxe.inf, UniXNURamDiskDxe.inf, DarwinBoot.inf, DiskIoDxe, PartitionDxe, EnglishDxe and Fat behind UNIXNU\_PAYLOAD=1.
- ./unixnu build firmware --uefi ../Mu-Silicium --target RELEASE -D ../UniXNU-hero2lte applies the five base patches and builds the 2 MiB FD.

### 开发经验

- The standalone image is an Android v0 header at 0x10000000 with kernel at 0x10008000 and tags at 0x10000100; the kernel field is exactly BootShim plus the 2 MiB FD.
- The standalone image omits the stock DTBH table and SEANDROIDENFORCE footer. S-Boot acceptance is untested.
- The standalone build is bit-for-bit reproducible and the DECON trigger is preserved instead of writing the Exynos 8895 value 0x1281.
- With UNIXNU\_PAYLOAD=1 the UniXNU firmware build links UniXNU, UniXNUDxe, UniXNURamDiskDxe and DarwinBoot. FVMAIN grows from 0x20a000 to 0x235000 inside the 2 MiB FD.

### 完成条件

- Firmware builds, enters UniXNU, publishes the framebuffer, keeps the payload FAT readable and preserves the reserved-memory ranges.

### 当前范围

- No hardware boot attempt yet.
- The integrated firmware has no payload or boot image yet.

### 下一步

- Boot the integrated firmware and verify the UniXNU menu and payload FAT.

### 证据

- `source`: [hero2lte firmware package, keypad library, host tests and optional UniXNU payload integration](https://github.com/DokuroMitsukai/Mu-Silicium/commit/5790015a98714044d72d5037cea300b40f66a2e0)
- `host`: [2 MiB SILICIUM\_UEFI.fd contains UniXNU, UniXNUDxe, UniXNURamDiskDxe and DarwinBoot; FVMAIN used 0x235000 and FVMAIN\_COMPACT kept 0x194998 free](https://github.com/DokuroMitsukai/UniXNU-hero2lte/blob/53ccc853aefa388215504ddc75ca8f602917e6e3/board.toml)
  Command: <code>./unixnu build firmware --uefi ../Mu-Silicium --target RELEASE -D ../UniXNU-hero2lte</code>. Revision: `5790015a98714044d72d5037cea300b40f66a2e0`.

## CPU 与中断 {#cpu}

`planned`

组件: `ArmCpu`, `ArmDTPlatform`, `SoftwareAES`.

### 硬件与依赖

- Four Mongoose cores at MPIDR 0x0-0x3 and four Cortex-A53 cores at MPIDR 0x100-0x103 with a 26 MHz generic timer.
- GIC-400 at 0x11001000: distributor 0x11001000, CPU interface 0x11002000, GICH 0x11004000 and GICV 0x11006000; PPIs 13, 14, 11 and 10.

### 配置

- exynos8890.dtsi declares all eight CPUs, PSCI 0.2 over SMC, GICv2 and the generic timer. hero2lte.dts enables only cpu0 for the first bring-up.
- ArmCpu and ArmDTPlatform come from the UniXNU catalog. SoftwareAES keeps the shared ARM64 component set complete.

### 操作步骤

- Compile the board DTS and inspect /cpus, /psci, /arm-io/intc and timebase-frequency in the generated ADT.
- Record per-CPU entry, timer interrupts and IPI delivery on hardware.

### 开发经验

- ArmCpu registers only the compatible string arm,gic-v3 and requires a 32-byte reg property with a distributor and redistributors. GIC-400 exposes four ranges, so mapGic rejects this tree.
- The stock timer node sets use-clocksource-only and Android uses MCT ticks for events. The architectural timer PPI is unvalidated.
- Cluster 0 is Mongoose and cluster 1 is Cortex-A53 on this SoC, the opposite of the usual big-little numbering.

### 完成条件

- Every enabled CPU reaches its entry checkpoint and timer and IPI handling works on each enabled CPU.

### 当前范围

- GICv2 MMIO support and the timer interrupt path are not implemented.
- Only one CPU is enabled.

### 下一步

- Add GICv2 distributor, CPU-interface and timer handling to ArmCpu before enabling secondary CPUs.

### 证据

- `source`: [Board CPU selection on top of the shared exynos8890.dtsi](https://github.com/DokuroMitsukai/UniXNU-hero2lte/blob/53ccc853aefa388215504ddc75ca8f602917e6e3/dts/hero2lte.dts)

## 内存与 DMA {#memory}

`planned`

### 硬件与依赖

- RAM ranges from the stock DTB: 0x80000000 with size 0x7e400000 and 0x880000000 with size 0x80000000.
- S-Boot framebuffer at 0xE2A00000 with size 0xE10000; the DT video\_frame and video\_scaler regions also reserve display buffers.

### 配置

- hero2lte.dts declares the low 0x7e400000 range as the XNU memory node and the framebuffer as reserved-memory.
- The upper 2 GiB range is not described yet because the common ADT generator currently expects one contiguous memory node.

### 操作步骤

- Compile the DTS and compare the generated ADT memory range with the stock DTB.
- Verify that DarwinBoot's owned window excludes the framebuffer and the DT video pools.

### 开发经验

- The provisional Mu-Silicium MemoryMapLib overlaps the DT video\_frame and video\_scaler pools; safety is unproven.
- The framebuffer lies inside the low RAM range, so the PMAP must reserve it before XNU maps RAM.

### 完成条件

- Every handoff and reserved range is accounted for and DMA masters use only their allocated windows.

### 当前范围

- Upper 2 GiB RAM is unused.
- Reserved-memory conversion and framebuffer exclusion are unverified.

### 下一步

- Decide how the ADT generator represents the second RAM range and the display reservations.

### 证据

- `source`: [Memory range and framebuffer reservation](https://github.com/DokuroMitsukai/UniXNU-hero2lte/blob/53ccc853aefa388215504ddc75ca8f602917e6e3/dts/hero2lte.dts)

## 存储与根卷 {#storage}

`planned`

### 硬件与依赖

- UFS controller at 0x155A0000. The GPT uses 4096-byte logical sectors.
- USERDATA is partition 18, first LBA 2085544, last LBA 7806207.

### 配置

- The SoC DTSI describes the UFS controller and leaves it disabled.
- userdata geometry is deliberately absent from board.toml until the EFS and CPEFS backups are verified.

### 操作步骤

- Capture EFS and CPEFS from TWRP with device-dump/capture-critical.py and verify both SHA-256 digests.
- Select or implement an Exynos UFS host driver before enabling the node.

### 开发经验

- ShengUfs targets Qualcomm UFS and cannot be reused directly.
- KernelSU is installed but adb shell has no root, so the critical backup needs TWRP or a root grant.

### 完成条件

- Host facts match the board; reads return the expected GPT; the configured root volume mounts and launchd starts.

### 当前范围

- No storage driver and no verified EFS/CPEFS backup.
- No wipe or repartition is allowed in this state.

### 下一步

- Obtain the EFS/CPEFS backup, then select or implement the UFS host driver.

### 证据

按下一步操作收集证据。

## 显示 {#display}

`planned`

### 硬件与依赖

- s6e3hf4 SVC\_OCTA panel at 1440x2560, 32 bpp, handed over at 0xE2A00000 by S-Boot.
- The stock DT reserves video\_frame and video\_scaler pools for the display pipeline.

### 配置

- Mu-Silicium SimpleFbDxe publishes a GOP from the S-Boot framebuffer address. No native display driver is selected yet.

### 操作步骤

- Build the Phase 1 firmware and capture the menu on the panel.
- Record geometry, colors and backlight behavior before adding a native driver.

### 开发经验

- The standalone firmware builds, but the display path has no hardware checkpoint.
- DECON's trigger register is logged and left untouched because the Exynos 8895 value is not evidence for 8890.

### 完成条件

- A known frame appears with correct geometry and colors, then userland presentation and backlight controls work.

### 当前范围

- No display hardware checkpoint.
- No brightness or native scanout driver.

### 下一步

- Boot the Phase 1 firmware and record the display result.

### 证据

按下一步操作收集证据。

## 输入 {#input}

`planned`

### 硬件与依赖

- gpio\_keys from the stock DTB: volume up GPA0-3, volume down GPA0-4, home GPA0-5, power GPA2-4, all active low.
- The keypad banks are at 0x10580000 with DAT at offset 0x04.

### 配置

- Mu-Silicium KeypadDeviceLib polls the GPA0 and GPA2 data registers, applies a 20 ms debounce and maps press-only events to the menu.
- The SoC DTSI does not export a pinctrl node because XNU has no Samsung pinctrl driver.

### 操作步骤

- Run Resources/Scripts/test\_hero2lte\_keypad.py in the firmware checkout.
- Hold Volume Up at reset and record the menu response on hardware.

### 开发经验

- The keypad host test passes. Device input is untested.
- Touch needs a separate component and has no driver yet.

### 完成条件

- Touches map to the display, simultaneous contacts keep stable IDs, release events arrive, and buttons produce expected HID reports.

### 当前范围

- Only keypad logic exists; touch and XNU gpio-keys integration are pending.

### 下一步

- Validate keypad input in the Phase 1 firmware menu.

### 证据

按下一步操作收集证据。

## GPU {#gpu}

`planned`

### 硬件与依赖

- The stock DT exposes G3D power and DVS nodes but no Mali node.
- The GPU model, power sequence and SMMU inputs still need to be recorded from the vendor kernel.

### 配置

- No GPU component is selected. The Adreno components target Qualcomm hardware and do not apply.

### 操作步骤

- Inventory the GPU from the vendor kernel and board files before selecting a component.
- Record power-domain and SMMU requirements in this area.

### 开发经验

- No UniXNU component currently supports the Exynos 8890 GPU.

### 完成条件

- GPU submissions complete, mapping and fence handling are correct, a known image renders, and the selected Metal client presents it.

### 当前范围

- No GPU inventory, driver or hardware result.

### 下一步

- Identify the GPU and its power and SMMU inputs from the vendor kernel.

### 证据

按下一步操作收集证据。

## 网络 {#network}

`planned`

### 硬件与依赖

- The stock boot DT has no wireless controller node; the chip must be identified from the vendor kernel and board files.

### 配置

- No network component is selected.

### 操作步骤

- Inventory the wireless chip, firmware files and bus before selecting a driver.
- Add firmware paths and hashes to proprietary-files.txt.

### 开发经验

- Wi-Fi firmware and driver inputs are not collected yet.

### 完成条件

- Scanning, association, address configuration and sustained receive and transmit traffic pass with the selected firmware.

### 当前范围

- No wireless inventory or driver.

### 下一步

- Identify the wireless chip and its firmware from the vendor kernel.

### 证据

按下一步操作收集证据。

## 音频 {#audio}

`planned`

### 硬件与依赖

- The stock boot DT describes no audio route; the codec and DSP inputs still need to be recorded.

### 配置

- No audio component is selected.

### 操作步骤

- Inventory the codec, DSP and amplifier wiring before selecting a component.

### 开发经验

- Audio hardware and firmware inputs are not collected yet.

### 完成条件

- Each declared route carries the selected audio format through playback or capture and handles start and stop correctly.

### 当前范围

- No audio inventory or driver.

### 下一步

- Identify the audio hardware from the vendor kernel and schematics.

### 证据

按下一步操作收集证据。

## 电源 {#power}

`planned`

### 硬件与依赖

- The stock DT names max77854 PMIC and MUIC, s2mpb02 sub-PMIC, max77838 and p9220 wireless charger.
- Battery and charger policy are not yet inventoried.

### 配置

- No power component is selected and no regulator or charger driver runs.

### 操作步骤

- Inventory regulators, charger and battery reporting from the vendor kernel.
- Record sleep and resume dependencies before claiming a power transition.

### 开发经验

- The firmware leaves power management to S-Boot and UEFI defaults.

### 完成条件

- Declared power controls and battery readings match observations; each claimed sleep or resume transition restores dependent peripherals.

### 当前范围

- No battery, charger or power-domain driver.

### 下一步

- Inventory the PMIC and charger topology from the vendor kernel.

### 证据

按下一步操作收集证据。

## 镜像组装 {#packaging}

`planned`

组件: `XnuPrelink`.

### 硬件与依赖

- XNU 10063.141.1 and Darwin 23.6.0 from the iPadOS profile.
- Android v0 boot image: base 0x10000000, kernel 0x10008000, tags 0x10000100, page size 2048.

### 配置

- patch\_series covers the arch, SoC, OS and device series in that order.
- kernel.defconfig = hero2lte\_defconfig.

### 操作步骤

- Run ./unixnu build kernel, ./unixnu build package and ./unixnu build payload once the kernel inputs exist.
- Pack the image with ./unixnu bootimg and inspect boot.json before flashing.

### 开发经验

- The standalone Mu-Silicium boot image already uses the v0 layout and passes the BootShim host tests.
- No XNU kernel, payload or UniXNU boot image has been built for this board.

### 完成条件

- Kernel and prelink succeed, the payload contains all declared inputs, and the boot image matches the bootloader format and size limit.

### 当前范围

- No kernelcache, trust cache or data ramdisk is available.

### 下一步

- Build the kernel after ArmCpu GICv2 support and the first hardware checkpoint.

### 证据

按下一步操作收集证据。

## 诊断 {#diagnostics}

`planned`

### 硬件与依赖

- Porting record CI, UniXNU status output and firmware or kernel logs.

### 配置

- The record workflow from the template is kept. unixnu.lock pins the resolved sources.

### 操作步骤

- Run python3 scripts/porting-record.py check --device ../UniXNU-hero2lte after each record change.
- Capture the firmware log before kernel handoff once the log exporter is integrated.

### 开发经验

- Host build logs exist locally; no firmware or kernel log has been captured from the device.

### 完成条件

- Each claimed milestone has a reproducible command, a matching revision and an accessible result.

### 当前范围

- No QR log exporter or persistent capture in the firmware yet.

### 下一步

- Add the firmware log exporter before the first hardware boot.

### 证据

按下一步操作收集证据。

</div>
