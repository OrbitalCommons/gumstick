# Module v1 programming and lighting test fixture

This is the **ordered programming-carrier v1**, a USB programmer and slow GPIO
indicator fixture for the ESP32-S2 + iCE40 module. Use the [daughterboard ICD](../esp32-fpga-module/docs/ICD-v1.md)
for the interface, [design notes](docs/DESIGN.md) for the circuit, and
[ordered snapshot](releases/v1/README.md) for manufacturing files.

The procedure below specifies a test program to implement. There is **no complete
fixture firmware included here**. Affogato supplies build/loading/SPI building
blocks; [these reviewed setup notes](../gps-time-calibrator/docs/integration/affogato.md)
explain its current capabilities and limitations. The calibrator's GPIO assignments
and bitstream must **not** be used as the fixture test mapping.

## What the LEDs show

There are60 monitored interface signals:27ESP signals (including EN and input-only
GPIO46),30regular FPGA I/O and3FPGA RGB sink outputs. D1/D2 are independent5V and
3V3 TEST indicators. The monitor buffers have both /OE pins tied to ground:
**there is no software bank-enable signal**. “One bank at a time” means drive
only that bank's eligible GPIOs active while driving other eligible outputs inactive.

Green signal LEDs indicate HIGH. Red RGB monitor LEDs indicate LOW. Each monitor
has its own resistor and buffer; the GPIO drives a high-impedance input with100k
bias, not the LED current. An LED being lit proves an observed logic level,
not rated drive strength or a complete input-path/analog/high-speed test.

Use [led-map.json](docs/led-map.json) as the machine-readable test list. Group by
`buffer`, preserve `input` order, and carry `active_low`; do not assume consecutive
LED reference numbers cover every footprint or that a GPIO suffix is a FPGA pad.
The [ICD CSV](../esp32-fpga-module/docs/icd-v1-pinout.csv) maps each FPGA net to
its physical package pin for the fixture PCF.

## Setup and recovery

1. Unplug USB before fitting/removing the module. Seat both complementary DF40
   connectors evenly and use the2mm spacer/M3 retention without forcing engagement.
2. Connect a data-capable USB cable to an adequately powered, current-limited
   source/hub. This fixture uses USB CC resistors and a500mA-hold fuse; it has
   **no PD negotiation**. Fuse rating is not an authorization to draw arbitrary
   USB current. Start Wi-Fi off and a sparse LED pattern; measure total current.
3. For first flash: SW1=BOOT, press/release SW2 RESET, use native ESP32-S2 USB
   ROM programming, then SW1=RUN and RESET. Release SW3(GPIO46) during reset.
4. Use USB CDC for logs and commands. Disable UART logging/peripherals on43/44
   when testing those pins. Check FPGA loader CDONE and runtime identification.
5. Program distinct firmware identity `programming-carrier-v1-test` and require
   explicit operator arming after boot. This board has no electronic carrier-ID
   interlock: the operator must confirm the fixture. Running this sweep on the
   calibrator would toggle regulator enables, I²C and GPS pins as arbitrary LEDs.

## Pin classes: do not blindly sweep everything

| Signal | Treatment |
|---|---|
| ESP_EN / D10 | Observe high during normal run; SW2 reset tests it. Never use as a normal firmware output |
| GPIO0 / D11 | Keep high/input normally; SW1 controls BOOT/RUN. Exclude from automated bank/walk tests |
| GPIO46 / D36 | **Input only**; use SW3 after boot, read low released/high pressed. Never set output mode |
| GPIO45 / D35 | Flash-voltage strap. Keep low/high-Z through reset; optional separate post-boot test only, then return low before reset |
| ESP GPIO1–8,15–18,21,33–35,38–44 | Ordinary fixture outputs after disabling other peripheral owners |
| ESP GPIO9–14,36,37 | Internal FPGA link/reset/CDONE; not part of indicator sweep |
| ESP GPIO19/20 | USB; never repurpose during USB testing |
| FPGA ordinary30GPIOs | Output test via dedicated FPGA test design, physical pins from ICD |
| FPGA RGB0/1/2 | Current-sink outputs shared with module RGB LED; separate RGB-driver test |

Normal EN and GPIO0 indicators may remain lit while the eligible outputs are
blank. The power indicators also stay on. Log this exception so a technician
does not misdiagnose “all off.” GPIO45's special test should be opt-in; an MCU
reset while a strap is driven high deserves explicit hardware validation.
Do not change eFuses or flash-voltage settings to make a lighting test pass.

## Suggested program structure

- ESP task owns a bank/pin table generated from `led-map.json`, a USB command
  parser, a nonblocking pattern scheduler and a result log.
- A small FPGA fixture image exposes a30-bit regular-output mask, three RGB
  controls, readback/identity and a heartbeat/watchdog. It can use HFOSC; no
  external OCXO is fitted on this carrier.
- Use a tested, versioned SPI transport to apply FPGA masks atomically; do not
  assume Affogato's example register map already implements these controls.
- On boot/fault/timeout: regular test outputs low, RGB current sinks disabled,
  GPIO0 left safe, GPIO45low, GPIO46input. Require explicit `start` to illuminate.
- For RGB, use `SB_RGBA_DRV` with a conservative supported current and individual
  PWM controls. “Off” releases the sink, allowing the fixture100k pull-up to turn
  off its red LED. “On” sinks the line low; both module and monitor response should
  be inspected. Do not drive the shared sink pins as push-pull HIGH outputs.

Pseudocode (conceptual API, not an implemented library):

```text
safe_start()
verify_fpga_abi()
wait_for_operator_fixture_confirmation()

for bank in regular_banks_in_physical_order:
    eligible_outputs_off()                # EN/BOOT indicators are exceptions
    set_bank_mask(bank, eligible_mask)    # only post-boot safe push-pull pins
    wait_nonblocking(1000 ms)
    record_operator_result(bank)
    eligible_outputs_off()
    wait_nonblocking(300 ms)

for bank in regular_banks_in_physical_order:
    for channel in bank.eligible_channels:
        eligible_outputs_off()
        channel_set(channel, ON)
        log_expected_led_and_signal(channel)
        wait_nonblocking(300 ms)
        channel_set(channel, OFF)
        wait_nonblocking(150 ms)

run_checkerboards_one_bank_at_a_time()
run_walking_zero_one_bank_at_a_time()
run_short_all_regular_on_test_if_power_budget_allows()
run_rgb_sink_test_separately()
run_manual_boot_reset_and_gpio46_checks()
eligible_outputs_off()
```

For the human-visible sequence use300–1000ms dwell, not high-frequency PWM.
Offer pause/step/hold/repeat/reverse so a suspect solder joint can be probed.
A camera/photodiode can automate observation later; GPIO register readback alone
cannot confirm that the LED, buffer or connector contact actually works.

## Test phases and expected observations

1. **Baseline:** D1/D2 power, EN and RUN/BOOT indicators as described; all other
   driven regular outputs low and RGB released. Note any stuck-on lamps.
2. **One bank at a time:** light all eligible pins in U3, then U4…U10, with other
   eligible banks off. Verify location, uniformity and no unintended neighboring
   bank. U3/U6 have restricted pins; their whole physical bank will not light.
3. **Walking one:** one eligible green lamp at a time in table order, then reverse.
   Every transition is logged with signal, LED reference, connector and package
   pin. Look for missing, mirrored, duplicated and neighboring lights.
4. **Alternating:** even then odd eligible channels (`0x55` /`0xAA` masked to actual
   channels). Alternate at~2Hz. This can expose shorts masked by an all-on pattern.
5. **Walking zero:** selected bank on except one eligible channel off; other banks
   remain off. This catches stuck-high and pairwise bridge behavior.
6. **Cross-bank/all-on:** brief simultaneous regular-output test after current and
   regulator-temperature checks. The3.3V LDO and USB budget must tolerate it; the
   presence of buffers does not remove the electrical load. Limit dwell initially.
7. **RGB:** individually enable RGB0,RGB1,RGB2 sinks, then combinations. Red monitor
   polarity is inverted; inspect the module RGB LED too. Return all sinks off.
8. **Inputs/control:** press/releaseGPIO46 button after boot and log reads; verify
   EN/reset and BOOT/RUN via the physical controls in a separate controlled step.
9. **Optional input coverage:** place one ordinary pin in input mode, then apply a
   known0/3.3V through a series resistor to its accessible signal-side bias-resistor
   pad; read it back. Never drive against an output or use5V. This is separate from
   the output lamp test and requires deliberate external stimulus.

Proposed USB commands to implement: `fixture status`, `fixture banks`,
`fixture bank U7`, `fixture walk`, `fixture step`, `fixture hold FPGA_IOB_3B_G6`,
`fixture checkerboard`, `fixture rgb 1`, `fixture input46`, `fixture stop`.
`stop` must work during every dwell; use task timers/state transitions, not a
blocking multi-minute loop. Reset should return to idle, never auto-repeat all-on.

## Test report and coverage limits

Save module serial/operator ID, module/interface revision, app/FPGA hashes,
measured USB voltage/current, selected dwell, expected/observed result for each
channel, optional photos and faults. Distinguish **command applied**, **pin readback**,
and **optically observed**; only the last establishes a visible lamp result.

This fixture does not validate RF performance, high-speed signal integrity,
FPGA global clock routing, ADC precision, full current capability or every input
path. It loads signals with long traces/buffer inputs and is intended for slow
functional tests. Finish with outputs safe, SW1 RUN, and OTA/recovery firmware
validated before installing the module on an application carrier.

## Physical bank/channel order

The table below is generated from `docs/led-map.json` for the ordered fixture.
D37–D41 and D72–D73 are not populated channels in this map; do not fill numeric gaps.

| Buffer | Kind | Channels in input-pin order |
|---|---|---|
| U3 | ESP | D10=EN; D11=GPIO0_BOOT; D12=GPIO1; D13=GPIO2; D14=GPIO3; D15=GPIO4; D16=GPIO5; D17=GPIO6 |
| U4 | ESP | D18=GPIO7; D19=GPIO8; D20=GPIO15; D21=GPIO16; D22=GPIO17; D23=GPIO18; D24=GPIO21; D25=GPIO33 |
| U5 | ESP | D26=GPIO34; D27=GPIO35; D28=GPIO38; D29=GPIO39; D30=GPIO40; D31=GPIO41; D32=GPIO42; D33=GPIO43_TXD |
| U6 | ESP | D34=GPIO44_RXD; D35=GPIO45; D36=GPIO46 |
| U7 | FPGA | D42=IOB_0A; D43=IOB_2A; D44=IOB_3B_G6; D45=IOB_4A; D46=IOB_5B; D47=IOB_6A; D48=IOB_8A; D49=IOB_9B |
| U8 | FPGA | D50=IOB_13B; D51=IOB_16A; D52=IOB_18A; D53=IOB_20A; D54=IOB_22A; D55=IOB_23B; D56=IOB_25B_G3; D57=IOB_29B |
| U9 | FPGA | D58=IOT_36B; D59=IOT_37A; D60=IOT_38B; D61=IOT_39A; D62=IOT_41A; D63=IOT_42B; D64=IOT_43A; D65=IOT_44B |
| U10 | FPGA | D66=IOT_45A_G1; D67=IOT_46B_G0; D68=IOT_48B; D69=IOT_49A; D70=IOT_50B; D71=IOT_51A |
| U11 | RGB | D74=RGB0; D75=RGB1; D76=RGB2 |
