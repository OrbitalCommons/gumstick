# Gumstick: ESP32 + iCE40 FPGA module

A small "gumstick" daughterboard that pairs an Espressif ESP32 (Wi-Fi, USB,
application CPU) with a Lattice iCE40UP5K FPGA (timing-critical I/O), plus the
carrier used to program and test it. KiCad 10 sources, fabrication outputs,
interface control documents and the scripts that generated them.

| Folder | Design | Status |
|---|---|---|
| [`current-df40-connectors/`](current-df40-connectors/README.md) | **v1, current.** 20 × 45 mm, 4 layers, ESP32-S2FH4 + iCE40UP5K-SG48, U.FL antenna jack, RGB LED, two underside Hirose DF40 40-pin board-to-board connectors (one receptacle, one plug, so it cannot mate reversed). | First 10 ordered; the exact ordered files are frozen in [`releases/v1/`](current-df40-connectors/releases/v1/README.md) and Git tag `v1`. |
| [`future-m2-goldfingers/`](future-m2-goldfingers/README.md) | **v2, future.** 22 × 42 mm M.2 2242 key-M card (0.8 mm, 4 layers) with gold-finger contacts and a custom pinout; bare ESP32-C6 + 16 MB QSPI flash + the same iCE40UP5K. Not PCIe/NVMe compatible. | Development draft, not for fabrication. |
| [`programming-carrier/`](programming-carrier/README.md) | USB programmer and slow-GPIO indicator fixture for the v1 module (mating DF40 pair, buttons, LEDs). | v1 ordered. |

Start with the **[v1 interface control document](current-df40-connectors/docs/ICD-v1.md)**
when designing a carrier for the module: it is the electrical and mechanical
contract (pinout, mated height, keep-outs, reusable footprints).

## Known carriers

- [GPS time calibrator](https://github.com/OrbitalCommons/gps-time-calibrator)
  (OrbitalCommons, currently private): GNSS-disciplined optical timing
  reference built around the v1 module.

## Working on the designs (kicadmium)

These boards are set up for the
[kicadmium](https://github.com/meawoppl/agent-portal-plugins/tree/main/kicadmium)
Agent Portal plugin. [`.kicad-pcb.json`](.kicad-pcb.json) declares the three
projects (`esp32-fpga-module`, `esp32-fpga-module-v2`, `programming-carrier`)
and the quality profile in [`docs/pcb-playbook/`](docs/pcb-playbook/README.md);
[`AGENTS.md`](AGENTS.md) has the one-time setup. Then:

```sh
agent-portal plugin open kicadmium        # open the workbench, add ?project=esp32-fpga-module
kicadmium drc --json --cwd . --project esp32-fpga-module
kicadmium kct -- lint run current-df40-connectors/module.kicad_pcb --format json > /tmp/lint.json
```

Each board folder is self-contained: its symbol and footprint libraries
(`Module.pretty`, `Module.kicad_sym`, ...) and 3D models live beside the board
and are referenced through `${KIPRJMOD}`. Datasheets cited by the designs are
in [`libraries/datasheets/`](libraries/datasheets/README.md).

## Scripts

`tools/hardware/` holds the Python (KiCad `pcbnew`) and C++ helpers used to
place, route, audit and export the boards. They are kept for reproducibility
and are not required to open or fabricate the designs. A few of the earliest
v1 scripts (`extract_module.py`, `build_placement.py`, `add_rgb.py`) read the
original MainBoard import the module was extracted from; that reference board
remains in [meawoppl/bp-test](https://github.com/meawoppl/bp-test/tree/master/boards/mainboard-reference).

## History

This repository was split out of [meawoppl/bp-test](https://github.com/meawoppl/bp-test)
with history preserved for these paths. Folder moves:
`boards/esp32-fpga-module` → `current-df40-connectors`,
`boards/esp32-fpga-module-v2` → `future-m2-goldfingers`,
`boards/programming-carrier` → `programming-carrier`.

## License

[MIT](LICENSE). Third-party datasheets and vendor 3D models included for
reference keep their own terms; see `NOTICE`.
