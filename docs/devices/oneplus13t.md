# OnePlus 13T (oneplus13t)

A community-maintained port for SM8750. Current results are based on the maintainer records at the revisions linked below.

| Repository | Maintainer |
| --- | --- |
| [UniXNU-Pagani_SM8750](https://github.com/IssacL04/UniXNU-Pagani_SM8750) | [IssacL04](https://github.com/IssacL04) |
| [UniXNU-sm8750-common](https://github.com/IssacL04/UniXNU-sm8750-common) | [IssacL04](https://github.com/IssacL04) |
| [UniXNU-Pagani-Drivers](https://github.com/IssacL04/UniXNU-Pagani-Drivers) | [IssacL04](https://github.com/IssacL04) |

## State

The verified hardware configuration reaches the iPadOS UI with UFS root reads and CPU framebuffer presentation. Data uses a volatile RAM seed.

The format 2 kernel, firmware, payload and image pass host builds. The current source includes S3910 touch, physical keys and DSI brightness/blanking; the kernel link, prelink and HID/backlight ABI checks pass. The migrated image and these peripheral additions await device validation. GPU, network, audio and full power management remain pending.

## Sources

- [README: IssacL04/UniXNU-Pagani_SM8750](https://github.com/IssacL04/UniXNU-Pagani_SM8750/blob/fcab49e2ea2f9ddfaa08ee6e8109ba7ed67029ac/README.md)

## Dual-system storage

The layout below is recorded from the 256 GB model.

| Item | Captured value |
| --- | --- |
| Recovery kernel | `6.6.118-android15-8-o-g4d611c32bedc-enc3l-4k` |
| Disk / logical sector | `/dev/block/sda` / 4096 bytes |
| Remaining userdata | Partition 15, LBA 4020972 to 44928767 |
| UniXNU partition | Partition 16, LBA 44928768 to 61705983 |
| F2FS shrink request / expected result | 40907264 / 40907535 blocks of 4096 bytes |

Calculate and inspect the target layout with the [dual-system partition guide](/porting/dual-system-partition). Measure the connected device before selecting partition boundaries.

## Use this port

1. Read the repository build instructions and pinned records. Prepare its firmware, system images and board inputs.
2. Build with that repository's commands. Use [Build and boot](/building) for common configuration.
3. Follow the [bring-up order](/porting/bring-up) and save results through [log capture](/porting/log-capture).
4. Update the [porting record](/porting/records) with the source revisions and last confirmed stage.
