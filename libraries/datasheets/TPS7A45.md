# TPS7A45

Original PDF: [TPS7A45.pdf](TPS7A45.pdf)

SHA-256: `c8c2fe4b7b5bd34b8ec750809817736cb66bcc29bbdf3a0238738c2d8a1ae80f`

Source: https://www.ti.com/lit/ds/symlink/tps7a45.pdf

Parts: TPS7A4533DCQR

GPS calibrator references: U15

Machine-extracted text; consult the original PDF for drawings, symbols and table alignment.

## Page 1

```text
                              Product         Sample &         Technical                                 Tools &            Support &            Reference
                              Folder          Buy              Documents                                 Software           Community            Design



                                                         TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
                                                                                                                 SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015

    TPS7A45xx Low-Noise Fast-Transient-Response 1.5-A Low-Dropout Voltage Regulators
1 Features                                                             3 Description
•
1    Optimized for Fast Transient Response                             The TPS7A45xx devices are low-dropout (LDO)
                                                                       regulators optimized for fast transient response. The
•    Output Current: 1.5 A                                             device can supply 1.5 A of output current with a
•    High Output Voltage Accuracy: 1% at 25°C                          dropout voltage of 300 mV. Operating quiescent
•    Dropout Voltage: 300 mV                                           current is 1 mA, dropping to less than 1 μA in
•    Low Noise: 35 μVRMS (10 Hz to 100 kHz)                            shutdown. Quiescent current is well controlled; it does
                                                                       not rise in dropout as with many other regulators. In
•    High Ripple Rejection: 68 dB at 1 kHz                             addition to fast transient response, the TPS7A45xx
•    1-mA Quiescent Current                                            regulators have very-low output noise, which makes
•    No Protection Diodes Needed                                       them ideal for sensitive RF supply applications.
•    Controlled Quiescent Current in Dropout                           Output voltage range is from 1.21 to 20 V. The
•    Fixed Output Voltages: 1.5 V, 1.8 V, 2.5 V, 3.3 V                 TPS7A45xx regulators are stable with output
                                                                       capacitance as low as 10 μF. Small ceramic
•    Adjustable Output from 1.21 V to 20 V                             capacitors can be used without the necessary
     (TPS7A4501 Only)                                                  addition of ESR as is common with other regulators.
•    Less Than 1-μA Quiescent Current in Shutdown                      Internal protection circuitry includes reverse-battery
•    Stable With 10-μF Ceramic Output Capacitor                        protection, current limiting, thermal limiting, and
                                                                       reverse-current protection. The devices are available
•    Reverse-Battery Protection                                        in fixed output voltages of 1.5 V, 1.8 V, 2.5 V, 3.3 V,
•    Reverse Current Protection                                        and as an adjustable device with a 1.21-V reference
                                                                       voltage.
2 Applications
                                                                                                                    Device Information(1)
•    Industrial
                                                                                        PART NUMBER                       PACKAGE             BODY SIZE (NOM)
•    Wireless Infrastructure
                                                                                                                    SOT-223 (6)          6.50 mm × 7.06 mm
•    Radio-Frequency Systems                                                TPS7A45xx
                                                                                                                    TO-263 (5)           10.16 mm × 15.24 mm
                                                                            (1) For all available packages, see the orderable addendum at
                                                                                the end of the data sheet.

                  Simplified Schematic                                                                  Dropout Voltage vs Output Current
                                                                                              500

                                                                                              450

                                                                                              400

                                                                                              350
                                                                       Dropout Voltage – mV




                                                                                                                    TA = 125°C

                                                                                              300

                                                                                              250

                                                                                              200

                                                                                              150                                 TA = 25°C

                                                                                              100

                                                                                              50

                                                                                               0
                                                                                                    0      0.2      0.4    0.6    0.8     1      1.2    1.4   1.6
                                                                                                                          Output Current – A


1




       An IMPORTANT NOTICE at the end of this data sheet addresses availability, warranty, changes, use in safety-critical applications,
       intellectual property matters and other important disclaimers. PRODUCTION DATA.
```

## Page 2

```text
TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015                                                                                                                           www.ti.com


                                                                           Table of Contents
    1   Features .................................................................. 1                8.4 Device Functional Modes........................................ 16
    2   Applications ........................................................... 1            9     Application and Implementation ........................ 17
    3   Description ............................................................. 1                  9.1 Application Information............................................ 17
    4   Revision History..................................................... 2                      9.2 Typical Applications ................................................ 18
    5   Device Comparison Table..................................... 3                        10 Power Supply Recommendations ..................... 22
    6   Pin Configuration and Functions ......................... 3                           11 Layout................................................................... 22
                                                                                                     11.1 Layout Guidelines ................................................. 22
    7   Specifications......................................................... 4
                                                                                                     11.2 Layout Example .................................................... 23
         7.1    Absolute Maximum Ratings ..................................... 4
                                                                                                     11.3 Thermal Considerations ........................................ 24
         7.2    ESD Ratings.............................................................. 4
         7.3    Recommended Operating Conditions....................... 4                     12 Device and Documentation Support ................. 26
         7.4    Thermal Information .................................................. 5             12.1    Related Links ........................................................ 26
         7.5    Electrical Characteristics........................................... 5              12.2    Community Resources.......................................... 26
         7.6    Typical Characteristics .............................................. 8             12.3    Trademarks ........................................................... 26
                                                                                                     12.4    Electrostatic Discharge Caution ............................ 26
    8   Detailed Description ............................................ 13
                                                                                                     12.5    Glossary ................................................................ 26
         8.1 Overview ................................................................. 13
         8.2 Functional Block Diagram ....................................... 13              13 Mechanical, Packaging, and Orderable
         8.3 Feature Description................................................. 13
                                                                                                 Information ........................................................... 26



4 Revision History
NOTE: Page numbers for previous revisions may differ from page numbers in the current version.

Changes from Revision E (August 2014) to Revision F                                                                                                                             Page

•   Corrected the body sizes listed for the packages ................................................................................................................. 1
•   Moved Tstg to Absolute Maximum Ratings table and changed Handling Ratings to ESD Ratings table ............................... 4
•   Relocated Thermal Considerations and Calculating Junction Temperature to Layout ........................................................ 24
•   Added Community Resources ............................................................................................................................................. 26


Changes from Revision D (August 2011) to Revision E                                                                                                                             Page

•   Added Handling Rating table, Feature Description section, Device Functional Modes, Application and
    Implementation section, Power Supply Recommendations section, Layout section, Device and Documentation
    Support section, and Mechanical, Packaging, and Orderable Information section ............................................................... 1


Changes from Revision C (December 2010) to Revision D                                                                                                                           Page

•   Replaced the Dissipation Ratings table with the Thermal Information table .......................................................................... 5




2        Submit Documentation Feedback                                                                          Copyright © 2008–2015, Texas Instruments Incorporated

                                  Product Folder Links: TPS7A4501 TPS7A4515 TPS7A4518 TPS7A4525 TPS7A4533
```

## Page 3

```text
                                                               TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
www.ti.com                                                                                        SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015


5 Device Comparison Table

                             DEVICE                                       OUTPUT VOLTAGE                                    PIN 5
                            TPS7A4501                                          Adjustable                                    ADJ
                            TPS7A4515                                             1.5 V                                    SENSE
                            TPS7A4518                                             1.8 V                                    SENSE
                            TPS7A4525                                             2.5 V                                    SENSE
                            TPS7A4533                                             3.3 V                                    SENSE



6 Pin Configuration and Functions

                             DCQ Package
                             6-Pin SOT-223                                                                KTT Package
                               Top View                                                                   6-Pin TO-263
                                                                                                            Top View
                                5       SENSE/ADJ
                                4       OUT                                                                 5          SENSE/ADJ
                  GND




                        6       3       GND                                                                 4          OUT
                                2       IN                                                                  3          GND
                                1       SHDN                                                                2          IN
                                                                                                            1          SHDN


                                                                 Pin Functions
            PIN
                                                                                 DESCRIPTION
  NO.          NAME
                              Shutdown. SHDN is used to put the TPS7A45xx regulators into a low-power shutdown state. The output is off
                              when SHDN is pulled low. SHDN can be driven by 5-V logic, 3-V logic or open-collector logic with a pullup
   1           SHDN           resistor. The pullup resistor is required to supply the pullup current of the open-collector gate, normally several
                              microamperes, and SHDN current, typically 3 μA. If unused, SHDN must be connected to VIN. The device is in
                              the low-power shutdown state if SHDN is not connected.
                              Input. Power is supplied to the device through IN. A bypass capacitor is required on this pin if the device is more
                              than six inches away from the main input filter capacitor. In general, the output impedance of a battery rises with
                              frequency, so it is advisable to include a bypass capacitor in battery-powered circuits. A bypass capacitor
                              (ceramic) in the range of 1 μF to 10 μF is sufficient. The TPS7A45xx regulators are designed to withstand
   2              IN
                              reverse voltages on IN with respect to ground and on OUT. In the case of a reverse input, which can happen if a
                              battery is plugged in backwards, the device acts as if there is a diode in series with its input. There is no reverse
                              current flow into the regulator, and no reverse voltage appears at the load. The device protects both itself and
                              the load.
                              Ground.
   3            GND           For the KTT package, the exposed thermal pad is connected to GND and must be soldered to the PCB for rated
                              thermal performance.
                              Output. The output supplies power to the load. A minimum output capacitor (ceramic) of 10 μF is required to
   4            OUT           prevent oscillations. Larger output capacitors are required for applications with large transient loads to limit peak
                              voltage transients.
                              Adjust. For the adjustable version only (TPS7A4501), this is the input to the error amplifier. ADJ is internally
   5              ADJ         clamped to ±7 V. It has a bias current of 3 μA that flows into the pin. ADJ voltage is 1.21 V referenced to ground,
                              and the output voltage range is 1.21 V to 20 V.
                              Sense. For fixed-voltage versions (TPS7A4515, TPS7A4518, TPS7A4525, and TPS7A4533), SENSE is the
                              input to the error amplifier. Optimum regulation is obtained at the point where SENSE is connected to the OUT
                              pin of the regulator. In critical applications, small voltage drops are caused by the resistance (RP) of PCB traces
                              between the regulator and the load. These may be eliminated by connecting SENSE to the output at the load as
   5          SENSE
                              shown in Figure 32. Note that the voltage drop across the external PCB traces adds to the dropout voltage of the
                              regulator. SENSE bias current is 600 μA at the rated output voltage. SENSE can be pulled below ground (as in a
                              dual supply system in which the regulator load is returned to a negative supply) and still allow the device to start
                              and operate.
   6            GND           Ground. DCQ package only.




Copyright © 2008–2015, Texas Instruments Incorporated                                                    Submit Documentation Feedback                3
                              Product Folder Links: TPS7A4501 TPS7A4515 TPS7A4518 TPS7A4525 TPS7A4533
```

## Page 4

```text
TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015                                                                                            www.ti.com


7 Specifications
7.1 Absolute Maximum Ratings
over operating virtual-junction temperature range (unless otherwise noted) (1)
                                                                                                             MIN           MAX            UNIT
                                         IN                                                                  –20            20
                                         OUT                                                                 –20            20
                                         Input-to-output differential (2)                                    –20            20
Input voltage, VIN                                                                                                                          V
                                         SENSE                                                               –20            20
                                         ADJ                                                                  –7             7
                                         SHDN                                                                –20            20
Output short-circuit duration, tshort                                                                                    Indefinite
Maximum lead temperature (10-s soldering time), Tlead                                                                      300             °C
Maximum junction temperature, TJMAX                                                                                        150             °C
Storage temperature, Tstg                                                                                    –65           150             °C

(1)   Stresses beyond those listed under Absolute Maximum Ratings may cause permanent damage to the device. These are stress ratings
      only, and functional operation of the device at these or any other conditions beyond those indicated under Recommended Operating
      Conditions is not implied. Exposure to conditions beyond the recommended operating maximum for extended periods may affect device
      reliability.
(2)   Absolute maximum input-to-output differential voltage cannot be achieved with all combinations of rated IN pin and OUT pin voltages.
      With the IN pin at 20 V, the OUT pin may not be pulled below 0 V. The total measured voltage from IN to OUT can not exceed ±20 V.

7.2 ESD Ratings
                                                                                                                           VALUE           UNIT
           Electrostatic                Human body model (HBM), per ANSI/ESDA/JEDEC JS-001, all pins (1)                   ±2000
V(ESD)                                                                                                                                      V
           discharge                    Charged device model (CDM), per JEDEC specification JESD22-C101, all pins (2)      ±1000

(1)   JEDEC document JEP155 states that 500-V HBM allows safe manufacturing with a standard ESD control process. Pins listed as 2000 V
      may actually have higher performance.
(2)   JEDEC document JEP157 states that 250-V CDM allows safe manufacturing with a standard ESD control process. Pins listed as 1000 V
      may actually have higher performance.

7.3 Recommended Operating Conditions
over operating free-air temperature range (unless otherwise noted)
                                                                                                              MIN             MAX         UNIT
VIN        Input voltage range (1)                                                                    VOUT + VDO                  20        V
VIH        SHDN high-level input voltage                                                                           2              20        V
VIL        SHDN low-level input voltage                                                                                          0.25       V
TJ         Recommended operating junction temperature range                                                    –40               125       °C

(1)   TPS7A4501, TPS7A4515, and TPS7A4518 may require a higher minimum input voltage under some output voltage/load conditions as
      indicated under Electrical Characteristics.




4        Submit Documentation Feedback                                                       Copyright © 2008–2015, Texas Instruments Incorporated

                            Product Folder Links: TPS7A4501 TPS7A4515 TPS7A4518 TPS7A4525 TPS7A4533
```

## Page 5

```text
                                                                TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
www.ti.com                                                                                         SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015


7.4 Thermal Information
                                                                                                       TPS7A45xx
                              THERMAL METRIC (1) (2)                                    KTT (TO-263)              DCQ (SOT-223)                UNIT
                                                                                            5 PINS                       6 PINS
RθJA             Junction-to-ambient thermal resistance                                      28.0                         50.5                 °C/W
RθJC(top)        Junction-to-case (top) thermal resistance                                   43.0                         31.1                 °C/W
RθJB             Junction-to-board thermal resistance                                        17.4                         5.1                  °C/W
ψJT              Junction-to-top characterization parameter                                  3.9                          1.0                  °C/W
ψJB              Junction-to-board characterization parameter                                9.4                          5.0                  °C/W
RθJC(bot)        Junction-to-case (bottom) thermal resistance                                0.3                           —                   °C/W

(1)   For more information about traditional and new thermal metrics, see the Semiconductor and IC Package Thermal Metrics application
      report, SPRA953.
(2)   For thermal estimates of this device based on PCB copper area, see the TI PCB Thermal Calculator.

7.5 Electrical Characteristics
Over recommended operating temperature range TJ = –40 to 125°C (unless otherwise noted) (1)
                 PARAMETER                                   TEST CONDITIONS                          TJ          MIN     TYP (2)      MAX      UNIT
                                              ILOAD = 0.5 A                                          25°C                        1.9
VIN         Minimum input voltage (3) (4)                                                                                                        V
                                              ILOAD = 1.5 A                                     Full range                       2.1     2.5
                                                                VIN = 2.21 V, ILOAD = 1 mA           25°C        1.485           1.5   1.515
                                              TPS7A4515         VIN = 2.5 V to 20 V,
                                                                                                Full range       1.447           1.5   1.545
                                                                ILOAD = 1 mA to 1.5 A
                                                                VIN = 2.3 V, ILOAD = 1 mA            25°C        1.782           1.8   1.818
                                              TPS7A4518         VIN = 2.8 V to 20 V,
                                                                                                Full range       1.737           1.8   1.854
                                                                ILOAD = 1 mA to 1.5 A
VOUT        Regulated output voltage (5)                                                                                                         V
                                                                VIN = 3 V, ILOAD = 1 mA              25°C        2.475           2.5   2.525
                                              TPS7A4525         VIN = 3.5 V to 20 V,
                                                                                                Full range       2.412           2.5   2.575
                                                                ILOAD = 1 mA to 1.5 A
                                                                VIN = 3.8 V, ILOAD = 1 mA            25°C        3.266           3.3   3.333
                                              TPS7A4533         VIN = 4.3 V to 20 V,
                                                                                                Full range         3.2           3.3     3.4
                                                                ILOAD = 1 mA to 1.5 A
                                                                VIN = 2.21 V, ILOAD = 1 mA           25°C        1.197          1.21   1.222
VADJ        ADJ pin voltage (3) (5)           TPS7A4501         VIN = 2.5 V to 20 V,                                                             V
                                                                                                Full range       1.174          1.21   1.246
                                                                ILOAD = 1 mA to 1.5 A
                                                                ΔVIN = 2.21 V to 20 V,
                                              TPS7A4515                                         Full range                        2       6
                                                                ILOAD = 1 mA
                                                                ΔVIN = 2.3 V to 20 V,
                                              TPS7A4518                                         Full range                       2.5      7
                                                                ILOAD = 1 mA
                                                                ΔVIN = 3 V to 20 V,
            Line regulation                   TPS7A4525                                         Full range                        3      10     mV
                                                                ILOAD = 1 mA
                                                                ΔVIN = 3.8 V to 20 V,
                                              TPS7A4533                                         Full range                       3.5     10
                                                                ILOAD = 1 mA
                                                                ΔVIN = 2.21 V to 20 V,
                                              TPS7A4501 (3)                                     Full range                       1.5      3
                                                                ILOAD = 1 mA




(1)   The TPS7A45xx regulators are tested and specified under pulse load conditions such that TJ ≉ TA. They are fully tested at TA = 25°C.
      Performance at –40 and 125°C is specified by design, characterization, and correlation with statistical process controls.
(2)   Typical values represent the likely parametric nominal values determined at the time of characterization. Typical values depend on the
      application and configuration and may vary over time. Typical values are not ensured on production material.
(3)   The TPS7A4501 is tested and specified for these conditions with the ADJ pin connected to the OUT pin.
(4)   For the TPS7A4501, TPS7A4515 and TPS7A4518, dropout voltages are limited by the minimum input voltage specification under some
      output voltage/load conditions.
(5)   Operating conditions are limited by maximum junction temperature. The regulated output voltage specification does not apply for all
      possible combinations of input voltage and output current. When operating at maximum input voltage, the output current range must be
      limited. When operating at maximum output current, the input voltage range must be limited.
Copyright © 2008–2015, Texas Instruments Incorporated                                                      Submit Documentation Feedback               5
                              Product Folder Links: TPS7A4501 TPS7A4515 TPS7A4518 TPS7A4525 TPS7A4533
```

## Page 6

```text
TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015                                                                                          www.ti.com


Electrical Characteristics (continued)
Over recommended operating temperature range TJ = –40 to 125°C (unless otherwise noted) (1)
                PARAMETER                                    TEST CONDITIONS                       TJ          MIN    TYP (2)     MAX     UNIT
                                                                   VIN = 2.5 V,                  25°C                        2        9
                                              TPS7A4515
                                                                   ΔILOAD = 1 mA to 1.5 A      Full range                           18
                                                                   VIN = 2.8 V,                  25°C                        2      10
                                              TPS7A4518
                                                                   ΔILOAD = 1 mA to 1.5 A      Full range                           20
                                                                   VIN = 3.5 V,                  25°C                      2.5      15
                                              TPS7A4525
                                                                   ΔILOAD = 1 mA to 1.5 A      Full range                           30
           Load regulation                                                                       25°C                        3      20     mV
                                                                   VIN = 4.3 V,               -40 to +85
                                              TPS7A4533                                                                             30
                                                                   ΔILOAD = 1 mA to 1.5 A         °C
                                                                                               Full range                           70
                                                                                                 25°C                        2        8
                                                             (3)   VIN = 2.5 V,               -40 to +85
                                              TPS7A4501                                                                               8
                                                                   ΔILOAD = 1 mA to 1.5 A         °C
                                                                                               Full range                           18
                                                                                                 25°C                    0.02     0.05
                                              ILOAD = 1 mA
                                                                                               Full range                         0.06
                                                                                                 25°C                   0.085     0.10
                                              ILOAD = 100 mA
           Dropout voltage    (4) (6) (7)                                                      Full range                         0.13
VDO                                                                                                                                         V
           VIN = VOUT(NOMINAL)                                                                   25°C                    0.17    0.180
                                              ILOAD = 500 mA
                                                                                               Full range                        0.250
                                                                                                 25°C                   0.300    0.350
                                              ILOAD = 1.5 A
                                                                                               Full range                        0.450
                                              ILOAD = 0 mA                                     Full range                    1      1.5
                                              ILOAD = 1 mA                                     Full range                  1.1      1.6
           GND pin current (7) (8)
IGND                                          ILOAD = 100 mA                                   Full range                  3.3      3.5    mA
           VIN = VOUT(NOMINAL) + 1
                                              ILOAD = 500 mA                                   Full range                  15       17
                                              ILOAD = 1.5 A                                    Full range                  80       90
                                              COUT = 10 μF, ILOAD = 1.5 A,
eN         Output voltage noise                                                                  25°C                      35             μVRMS
                                              BW = 10 Hz to 100 kHz
                                    (3) (9)
IADJ       ADJ pin bias current                                                                  25°C                        3        7     μA
                                              VOUT = OFF to ON                                 Full range                  0.9        2
           Shutdown threshold                                                                                                               V
                                              VOUT = ON to OFF                                 Full range      0.25      0.75
                                              V SHDN = 0 V                                       25°C                    0.01         1
I SHDN     SHDN pin current                                                                                                                 μA
                                              V SHDN = 20 V                                      25°C                        3      20
           Quiescent current in shutdown      VIN = 6 V, V SHDN = 0 V                            25°C                    0.01         1     μA
                                              VIN – VOUT = 1.5 V (avg), VRIPPLE = 0.5 VP-P,
           Ripple rejection                                                                      25°C                      68               dB
                                              fRIPPLE = 120 Hz, ILOAD = 0.75 A
                                              VIN = 7 V, VOUT = 0 V                              25°C                        2
ILIMIT     Current limit                                                                                                                    A
                                              VIN = VOUT(NOMINAL) + 1                          Full range       1.6
IIL        Input reverse leakage current      VIN = –20 V, VOUT = 0 V                          Full range                          300      μA




(6)    Dropout voltage is the minimum input to output voltage differential needed to maintain regulation at a specified output current. In
       dropout, the output voltage is equal to: VIN – VDROPOUT.
(7)    To satisfy requirements for minimum input voltage, the TPS7A4501 is tested and specified for these conditions with an external resistor
       divider (two 4.12-kΩ resistors) for an output voltage of 2.4 V. The external resistor divider adds a 300-µA DC load on the output.
(8)    GND pin current is tested with VIN = (VOUT(NOMINAL) + 1 V) and a current source load. The GND pin current decreases at higher input
       voltages.
(9)    ADJ pin bias current flows into the ADJ pin.
6         Submit Documentation Feedback                                                       Copyright © 2008–2015, Texas Instruments Incorporated

                              Product Folder Links: TPS7A4501 TPS7A4515 TPS7A4518 TPS7A4525 TPS7A4533
```

## Page 7

```text
                                                            TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
www.ti.com                                                                                    SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015


Electrical Characteristics (continued)
Over recommended operating temperature range TJ = –40 to 125°C (unless otherwise noted) (1)
              PARAMETER                                   TEST CONDITIONS                        TJ          MIN    TYP (2)    MAX     UNIT
                                              TPS7A4515       VOUT = 1.5 V, VIN < 1.5 V         25°C                   600     1000
                                              TPS7A4518       VOUT = 1.8 V, VIN < 1.8 V         25°C                   600     1000
IRO      Reverse output current (10)          TPS7A4525       VOUT = 2.5 V, VIN < 2.5 V         25°C                   600     1000     μA
                                              TPS7A4533       VOUT = 3.3 V, VIN < 3.3 V         25°C                   600     1000
                                              TPS7A4501       VOUT = 1.21 V, VIN < 1.21 V       25°C                   300      500

(10) Reverse output current is tested with the IN pin grounded and the OUT pin forced to the rated output voltage. This current flows into the
     OUT pin and out the GND pin.




Copyright © 2008–2015, Texas Instruments Incorporated                                                 Submit Documentation Feedback           7
                            Product Folder Links: TPS7A4501 TPS7A4515 TPS7A4518 TPS7A4525 TPS7A4533
```

## Page 8

```text
TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015                                                                                                                                                          www.ti.com


7.6 Typical Characteristics
Typical characteristics apply to all TPS7A45xx devices unless otherwise noted.

                                    500                                                                                                   480

                                    450                                                                                                                             IOUT = 1.5 A

                                    400
                                                                                                                                          360
                                    350
             Dropout Voltage – mV




                                                                                                                   Dropout Voltage – mV
                                                     TA = 125°C

                                    300

                                    250                                                                                                   240
                                                                                                                                                                    IOUT = 0.5 A
                                    200

                                    150                           TA = 25°C
                                                                                                                                          120                       IOUT = 100 mA
                                    100

                                    50
                                                                                                                                                                    IOUT = 1 mA
                                     0                                                                                                     0
                                          0   0.2   0.4    0.6     0.8    1    1.2   1.4   1.6                                              -50    -25      0      25      50       75    100   125
                                                          Output Current – A                                                                             TA – Free-Air Temperature – °C




             Figure 1. Dropout Voltage vs Output Current                                                                           Figure 2. Dropout Voltage vs Temperature




            VIN = 6 V                                             IOUT = 0 A                     VSHDN = VIN   IOUT = 1 mA                                        TPS7A4518

               Figure 3. Quiescent Current vs Temperature                                                      Figure 4. TPS7A4518 Output Voltage vs Temperature




         IOUT = 1 mA                                         TPS7A4525                                         IOUT = 1 mA                                        TPS7A4533

         Figure 5. TPS7A4525 Output Voltage vs Temperature                                                     Figure 6. TPS7A4533 Output Voltage vs Temperature




8      Submit Documentation Feedback                                                                                                            Copyright © 2008–2015, Texas Instruments Incorporated

                                                    Product Folder Links: TPS7A4501 TPS7A4515 TPS7A4518 TPS7A4525 TPS7A4533
```

## Page 9

```text
                                                                                                                     TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
www.ti.com                                                                                                                                                                 SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015


Typical Characteristics (continued)
Typical characteristics apply to all TPS7A45xx devices unless otherwise noted.
                                                    1.23                                                                                                     1.2

                                                 1.225
                                                                                                                                                              1




                                                                                                                                    Quiescent Current (mA)
                                                    1.22
                           Output Voltage (V)




                                                                                                                                                             0.8
                                                 1.215
                                                                                                                                                             0.6
                                                    1.21

                                                 1.205                                                                                                       0.4

                                                     1.2                                                                                                     0.2

                                                 1.195
                                                                                                                                                              0
                                                    1.19                                                                                                           0   2     4   6     8    10    12     14   16   18   20
                                                                                                                                                                                     Input Voltage (V)
                                                       -50     -25       0       25      50       75     100       125                                                                                                  D021
                                                                          Free-Air Temperature (qC)                 D020                         TJ = 25°C                           ROUT = 4.3 kΩ
                                                IOUT = 1 mA                         VIN = 6 V                                                                                          VSHDN = VIN

                                        Figure 7. TPS7A4501 Output Voltage vs Temperature                                                                    Figure 8. Quiescent Current vs Input Voltage
                           10
                                                                                                       IOUT = 10 mA
                                  9                                                                    IOUT = 100 mA
                                  8                                                                    IOUT = 300 mA
     Ground Current (mA)




                                  7
                                  6
                                  5
                                  4
                                  3
                                  2
                                  1
                                  0
                                                0          1   2     3       4     5     6        7      8     9         10
                                                                           Input Voltage (V)                               D022
                                                    TJ = 25°C                VOUT = 1.21 V                                                       TJ = 25°C                           VOUT = 1.21 V
                                                                              VSHDN = VIN                                                                                             VSHDN = VIN
                               Figure 9. TPS7A4501 Ground Current vs Input Voltage                                                Figure 10. TPS7A4501 Ground Current vs Input Voltage




                                                    TJ = 25°C                   VSHDN = VIN                                                      TJ = 25°C                              VSHDN = VIN

                           Figure 11. TPS7A4533 Ground Current vs Input Voltage                                                   Figure 12. TPS7A4533 Ground Current vs Input Voltage




Copyright © 2008–2015, Texas Instruments Incorporated                                                                                                                            Submit Documentation Feedback                 9
                                                                     Product Folder Links: TPS7A4501 TPS7A4515 TPS7A4518 TPS7A4525 TPS7A4533
```

## Page 10

```text
TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015                                                                                                            www.ti.com


Typical Characteristics (continued)
Typical characteristics apply to all TPS7A45xx devices unless otherwise noted.




                       VIN = VOUT(nom) + 1                                                                                VSHDN = 0 V

            Figure 13. Ground Current vs Output Current             Figure 14. Quiescent Current in Shutdown vs Input Voltage
                                                                                                   2.5

                                                                                                  2.25

                                                                        SHDN Input Current – µA     2

                                                                                                  1.75

                                                                                                   1.5

                                                                                                  1.25

                                                                                                    1

                                                                                                  0.75

                                                                                                   0.5

                                                                                                  0.25

                                                                                                    0
                                                                                                         0   2   4    6   8    10   12   14   16   18   20
                                                                                                                     SHDN Input Voltage – V
         VSHON = 0 V

         Figure 15. SHDN Pin Current (ISHDN) vs Temperature        Figure 16. SHDN Pin Current (ISHDN) vs SHDN Input Voltage




                                                                       IOUT = 1 mA
         IOUT = 1 mA
                                                                     Figure 18. SHDN Threshold (ON to OFF) vs Temperature
       Figure 17. SHDN Threshold (OFF to ON) vs Temperature

10     Submit Documentation Feedback                                                                         Copyright © 2008–2015, Texas Instruments Incorporated

                        Product Folder Links: TPS7A4501 TPS7A4515 TPS7A4518 TPS7A4525 TPS7A4533
```

## Page 11

```text
                                                                                                    TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
www.ti.com                                                                                                                    SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015


Typical Characteristics (continued)
Typical characteristics apply to all TPS7A45xx devices unless otherwise noted.
                                          5

                                         4.5

                                          4

                                         3.5
                 ADJ Bias Current – µA




                                          3

                                         2.5

                                          2

                                         1.5

                                          1

                                         0.5

                                          0
                                           -50   -25      0      25     50      75      100   125
                                                       TA – Free-Air Temperature – °C

                                                                                                              ΔVOUT = 100 mV

               Figure 19. ADJ Bias Current vs Temperature                                                         Figure 20. Current Limit vs Input-to-Output Differential
                                                                                                                                         Voltage




                                                                                                                     TJ = 25°C               VIN = 0 V
              VIN = 7 V                                           VOUT = 0 V                                               Current flows into OUT pin

                              Figure 21. Current Limit vs Temperature                                             Figure 22. Reverse Output Current vs Output Voltage




                                                                                                             VRIPPLE = 0.05 VPP               CIN = 0            TA = 25°C
              VIN = 0 V                                                                                             VIN = 2.7 V                      COUT = 10 µF (ceramic)

           Figure 23. Reverse Output Current vs Temperature                                                             Figure 24. Ripple Rejection vs Frequency



Copyright © 2008–2015, Texas Instruments Incorporated                                                                                Submit Documentation Feedback           11
                                                       Product Folder Links: TPS7A4501 TPS7A4515 TPS7A4518 TPS7A4525 TPS7A4533
```

## Page 12

```text
TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015                                                                                   www.ti.com


Typical Characteristics (continued)
Typical characteristics apply to all TPS7A45xx devices unless otherwise noted.




         IOUT = 1.5 A
                                                                            COUT = 10 µF            IOUT = 1.5 A
                                                                               (ceramic)
             Figure 25. Load Regulation vs Temperature                          Figure 26. Output Noise Voltage vs Frequency




          VIN = 4.3 V           CIN = 10 µF                                   VIN = 4.3 V           CIN = 10 µF
                     COUT = 10 µF (ceramic)                                              COUT = 10 µF (ceramic)

                 Figure 27. Load Transient Response                                  Figure 28. Load Transient Response




                                       IOUT = 1.5 A                           CIN = 10 µF
                                                                   COUT = 10 µF (ceramic)

                                                      Figure 29. Line Transient Response




12     Submit Documentation Feedback                                                   Copyright © 2008–2015, Texas Instruments Incorporated

                        Product Folder Links: TPS7A4501 TPS7A4515 TPS7A4518 TPS7A4525 TPS7A4533
```

## Page 13

```text
                                                        TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
www.ti.com                                                                          SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015


8 Detailed Description

8.1 Overview
The TPS7A45xx series are 1.5-A low-dropout regulators optimized for fast transient response. The devices are
capable of supplying 1.5 A at a dropout voltage of 300 mV. The low operating quiescent current (1 mA) drops to
less than 1 μA in shutdown. In addition to the low quiescent current, the TPS7A45xx regulators incorporate
several protection features that make them ideal for use in battery-powered systems. The devices are protected
against both reverse input and reverse output voltages. In battery-backup applications where the output can be
held up by a backup battery when the input is pulled to ground, the TPS7A45xx acts as if it has a diode in series
with its output and prevents reverse current flow. Additionally, in dual-supply applications where the regulator
load is returned to a negative supply, the output can be pulled below ground by as much as (20 V – VIN) and still
allow the device to start and operate.

8.2 Functional Block Diagram



                               Reverse
                                                             Pass                        Current
         IN                    Current                                                                         OUT
                                                            Element                       Limit
                              Protection




    SHDN
                                                                       Error Amplifier
                                                                   +


                           Thermal
                                                                                                               SENSE/ADJ
                           Overload

                                                               +
                                                                   Voltage Reference
                           Reverse
                           Voltage
                          Protection




                                                           GND

8.3 Feature Description
8.3.1 Adjustable Operation
The TPS7A4501 has an adjustable output voltage range of 1.21 V to 20 V. The output voltage is set by the ratio
of two external resistors as shown in Figure 30. The device maintains the voltage at the ADJ pin at 1.21 V
referenced to ground. The current in R1 is then equal to (1.21 V/R1), and the current in R2 is the current in R1
plus the ADJ pin bias current. The ADJ pin bias current, 3 μA at 25°C, flows through R2 into the ADJ pin. The
output voltage can be calculated using the formula shown in Equation 1. The value of R1 should be less than
4.17 kΩ to minimize errors in the output voltage caused by the ADJ pin bias current. Note that in shutdown the
output is turned off, and the divider current is zero.




Copyright © 2008–2015, Texas Instruments Incorporated                                       Submit Documentation Feedback    13
                            Product Folder Links: TPS7A4501 TPS7A4515 TPS7A4518 TPS7A4525 TPS7A4533
```

## Page 14

```text
TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015                                                                                www.ti.com




                                               Figure 30. Adjustable Operation

The output voltage can be set using the following equations:
                      R2
     VOUT = 1.21V(1 +    ) + IADJ ´ R2
                      R1                                                                                                             (1)
      VADJ = 1.21 V                                                                                                                  (2)
      IADJ = 3 µA at 25°C                                                                                                            (3)
      Output Range = 1.21 to 20 V                                                                                                    (4)

8.3.2 Fixed Operation
The TPS7A45xx can be used in a fixed voltage configuration. The SENSE/ADJ pin should be connected to OUT
for proper operation. An example of this is shown in Figure 31. The TPS7A4501 can also be used in this
configuration for a fixed output voltage of 1.21 V.

                                                            IN           OUT                          2.5 V at 1.5 A
                                       10 µF                                          10 µF
                                       (ceramic)              TPS7A4525               (ceramic)
                VIN > 3 V
                                                            SHDN       SENSE

                                                                   GND




                                               Figure 31. 3.3 to 2.5 V Regulator

During fixed voltage operation, the SENSE/ADJ pin can be used for a Kelvin connection if routed separately to
the load. This allows the regulator to compensate for voltage drop across parasitic resistances (RP) between the
output and the load. This becomes more crucial with higher load currents.
                                                                               RP
                                                       IN              OUT

                                                            TPS7A4501

                                VIN                    SHDN        SENSE                  Load
                                                                 GND




                                                                               RP

                                          Figure 32. Kelvin Sense Connection




14     Submit Documentation Feedback                                                Copyright © 2008–2015, Texas Instruments Incorporated

                        Product Folder Links: TPS7A4501 TPS7A4515 TPS7A4518 TPS7A4525 TPS7A4533
```

## Page 15

```text
                                                        TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
www.ti.com                                                                       SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015


8.3.3 Overload Recovery
Like many IC power regulators, the TPS7A45xx has safe operating area protection. The safe area protection
decreases the current limit as input-to-output voltage increases and keeps the power transistor inside a safe
operating region for all values of input-to-output voltage. The protection is designed to provide some output
current at all values of input-to-output voltage up to the device breakdown.
When power is first turned on, as the input voltage rises, the output follows the input, allowing the regulator to
start up into very heavy loads. During start up, as the input voltage is rising, the input-to-output voltage
differential is small, allowing the regulator to supply large output currents. With a high input voltage, a problem
can occur wherein removal of an output short does not allow the output voltage to recover. Other regulators also
exhibit this phenomenon, so it is not unique to the TPS7A45xx.
The problem occurs with a heavy output load when the input voltage is high and the output voltage is low.
Common situations occur immediately after the removal of a short circuit or when the shutdown pin is pulled high
after the input voltage has already been turned on. The load line for such a load may intersect the output current
curve at two points. If this happens, there are two stable output operating points for the regulator. With this
double intersection, the input power supply may need to be cycled down to zero and brought up again to make
the output recover.

8.3.4 Output Voltage Noise
The TPS7A45xx regulators have been designed to provide low output voltage noise over the 10-Hz to 100-kHz
bandwidth while operating at full load. Output voltage noise is typically 35 nV/√Hz over this frequency bandwidth
for the TPS7A4501 (adjustable version). For higher output voltages (generated by using a resistor divider), the
output voltage noise is gained up accordingly. This results in RMS noise over the 10-Hz to 100-kHz bandwidth of
14 μVRMS for the TPS7A4501, increasing to 38 μVRMS for the TPS7A4533.
Higher values of output voltage noise may be measured when care is not exercised with regard to circuit layout
and testing. Crosstalk from nearby traces can induce unwanted noise onto the output of the TPS7A45xx. Power-
supply ripple rejection must also be considered; the TPS7A45xx regulators do not have unlimited power-supply
rejection and pass a small portion of the input noise through to the output.

8.3.5 Protection Features
The TPS7A45xx regulators incorporate several protection features which make them ideal for use in battery-
powered circuits. In addition to the normal protection features associated with monolithic regulators, such as
current limiting and thermal limiting, the devices are protected against reverse input voltages, reverse output
voltages and reverse voltages from output to input.
Current limit protection and thermal overload protection are intended to protect the device against current
overload conditions at the output of the device. For normal operation, the junction temperature should not exceed
125°C.
The input of the device withstands reverse voltages of 20 V. Current flow into the device is limited to less than
1 mA (typically less than 100 μA), and no negative voltage appears at the output. The device protects both itself
and the load. This provides protection against batteries that can be plugged in backward.
The output of the TPS7A45xx can be pulled below ground without damaging the device. If the input is left open
circuit or grounded, the output can be pulled below ground by 20 V. For fixed voltage versions, the output acts
like a large resistor, typically 5 kΩ or higher, limiting current flow to typically less than 600 μA. For adjustable
versions, the output acts like an open circuit; no current flows out of the pin. If the input is powered by a voltage
source, the output sources the short-circuit current of the device and protects itself by thermal limiting. In this
case, grounding the SHDN pin turns off the device and stops the output from sourcing the short-circuit current.
The ADJ pin of the adjustable device can be pulled above or below ground by as much as 7 V without damaging
the device. If the input is left open circuit or grounded, the ADJ pin acts like an open circuit when pulled below
ground and like a large resistor (typically 5 kΩ) in series with a diode when pulled above ground.
In situations where the ADJ pin is connected to a resistor divider that would pull the ADJ pin above its 7-V clamp
voltage if the output is pulled high, the ADJ pin input current must be limited to less than 5 mA. For example, a
resistor divider is used to provide a regulated 1.5-V output from the 1.21-V reference when the output is forced to
20 V. The top resistor of the resistor divider must be chosen to limit the current into the ADJ pin to less than
5 mA when the ADJ pin is at 7 V. The 13-V difference between OUT and ADJ divided by the 5-mA maximum
current into the ADJ pin yields a minimum top resistor value of 2.6 kΩ.
Copyright © 2008–2015, Texas Instruments Incorporated                                  Submit Documentation Feedback      15
                            Product Folder Links: TPS7A4501 TPS7A4515 TPS7A4518 TPS7A4525 TPS7A4533
```

## Page 16

```text
TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015                                                                          www.ti.com


In circuits where a backup battery is required, several different input/output conditions can occur. The output
voltage may be held up while the input is either pulled to ground, pulled to some intermediate voltage, or is left
open circuit.
When the IN pin of the TPS7A45xx is forced below the OUT pin or the OUT pin is pulled above the IN pin, input
current typically drops to less than 2 μA. This can happen if the input of the device is connected to a discharged
(low voltage) battery and the output is held up by either a backup battery or a second regulator circuit. The state
of the SHDN pin has no effect on the reverse output current when the output is pulled above the input.

8.4 Device Functional Modes

Table 1 shows the functional modes for the TPS7A45xx.

                                                   Table 1. Device Modes
                                          SHDN                     DEVICE STATE
                                               H                  Regulated voltage
                                               L                     Shutdown




16     Submit Documentation Feedback                                          Copyright © 2008–2015, Texas Instruments Incorporated

                        Product Folder Links: TPS7A4501 TPS7A4515 TPS7A4518 TPS7A4525 TPS7A4533
```

## Page 17

```text
                                                        TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
www.ti.com                                                                       SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015


9 Application and Implementation

                                                           NOTE
               Information in the following applications sections is not part of the TI component
               specification, and TI does not warrant its accuracy or completeness. TI’s customers are
               responsible for determining suitability of components for their purposes. Customers should
               validate and test their design implementation to confirm system functionality.


9.1 Application Information
This section highlights some design considerations for implementing this device in various applications.

9.1.1 Output Capacitance and Transient Response
The TPS7A45xx regulators are designed to be stable with a wide range of output capacitors. The ESR of the
output capacitor affects stability, most notably with small capacitors. A minimum output capacitor of 10 μF with
an ESR of 3 Ω or less is recommended to prevent oscillations. Larger values of output capacitance can decrease
the peak deviations and provide improved transient response for larger load current changes. Bypass capacitors,
used to decouple individual components powered by the TPS7A45xx, increase the effective output capacitor
value.
Extra consideration must be given to the use of ceramic capacitors. Ceramic capacitors are manufactured with a
variety of dielectrics, each with different behavior over temperature and applied voltage. The most common
dielectrics used are Z5U, Y5V, X5R and X7R. The Z5U and Y5V dielectrics are good for providing high
capacitances in a small package, but exhibit strong voltage and temperature coefficients. When used with a 5-V
regulator, a 10-μF Y5V capacitor can exhibit an effective value as low as 1 μF to 2 μF over the operating
temperature range. The X5R and X7R dielectrics result in more stable characteristics and are more suitable for
use as the output capacitor. The X7R type has better stability across temperature, while the X5R is less
expensive and is available in higher values.
Voltage and temperature coefficients are not the only sources of problems. Some ceramic capacitors have a
piezoelectric response. A piezoelectric device generates voltage across its terminals due to mechanical stress,
similar to the way a piezoelectric accelerometer or microphone works. For a ceramic capacitor, the stress can be
induced by vibrations in the system or thermal transients.




Copyright © 2008–2015, Texas Instruments Incorporated                                  Submit Documentation Feedback      17
                            Product Folder Links: TPS7A4501 TPS7A4515 TPS7A4518 TPS7A4525 TPS7A4533
```

## Page 18

```text
TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015                                                                                        www.ti.com


9.2 Typical Applications
9.2.1 Adjustable Output Operation


                                                         IN                    OUT                                   2.5 V at 1 A
                                                                                               R2
                           +               C1                                                 4.22 k            C2
              VIN = 5 V
                                          10 PF                    TPS7A4501                                   10 PF

                                                         SHDN                   ADJ
                                                                     GND                       R1
                                                                                              4k



     NOTE: All capacitors are ceramic.

                                         Figure 33. Adjustable Output Voltage Operation

9.2.1.1 Design Requirements
Table 2 shows the design requirements.

                                                     Table 2. Design Parameters
                                          DESIGN PARAMETER                     EXAMPLE VALUE
                                            Input voltage (VIN)                       5.0 V
                                          Output voltage (VOUT)                       2.5 V
                                           Output current (IOUT)                  0 to 1 A
                                             Load regulation                          1%

9.2.1.2 Detailed Design Procedure
The TPS7A4501 has an adjustable output voltage range of 1.21 to 20 V. The output voltage is set by the ratio of
two external resistors R1 and R2 as shown in Figure 33. The device maintains the voltage at the ADJ pin at 1.21
V referenced to ground. The current in R1 is then equal to (1.21 V/R1), and the current in R2 is the current in R1
plus the ADJ pin bias current. The ADJ pin bias current, 3 µA at 25°C, flows through R2 into the ADJ pin. The
output voltage can be calculated using Equation 5.
                       R2
      VOUT = 1.21V(1 +    ) + IADJ ´ R2
                       R1                                                                                       (5)
The value of R1 should be less than 4.17 kΩ to minimize errors in the output voltage caused by the ADJ pin bias
current. Note that in shutdown the output is turned off, and the divider current is zero. For an output voltage of
2.50 V, R1 will be set to 4.0 kΩ. R2 is then found to be 4.22 kΩ using the equation above.
                       4.22kW
     VOUT = 1.21V(1 +          ) + 3µA ´ 4.22kW
                        4.0kW                                                                                   (6)
        VOUT = 2.50 V                                                                                                                       (7)
The adjustable device is tested and specified with the ADJ pin tied to the OUT pin for an output voltage of 1.21
V. Specifications for output voltages greater than 1.21 V are proportional to the ratio of the desired output voltage
to 1.21 V: VOUT/1.21 V. For example, load regulation for an output current change of 1 mA to 1.5 A is –2 mV (typ)
at VOUT = 1.21 V. At VOUT = 2.50 V, the typical load regulation is:
        (2.50 V/1.21 V)(–2 mV) = –4.13 mV                                                                                                   (8)
Figure 34 shows the actual change in output is about 3 mV for a 1-A load step. The maximum load regulation at
25°C is –8 mV. At VOUT = 2.50 V, the maximum load regulation is:
        (2.50 V/1.21 V)(–8 mV) = –16.53 mV                                                                                                  (9)
Because 16.53 mV is only 0.7% of the 2.5 V output voltage, the load regulation will meet the design
requirements.


18       Submit Documentation Feedback                                                     Copyright © 2008–2015, Texas Instruments Incorporated

                           Product Folder Links: TPS7A4501 TPS7A4515 TPS7A4518 TPS7A4525 TPS7A4533
```

## Page 19

```text
                                                         TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
www.ti.com                                                                       SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015


9.2.1.3 Application Curve




                                              Figure 34. 1-A Load Transient Response




Copyright © 2008–2015, Texas Instruments Incorporated                                  Submit Documentation Feedback      19
                            Product Folder Links: TPS7A4501 TPS7A4515 TPS7A4518 TPS7A4525 TPS7A4533
```

## Page 20

```text
TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015                                                                            www.ti.com


9.2.2 Paralleling Regulators for Higher Output Current




     NOTE: All capacitors are ceramic.

                              Figure 35. Paralleling Regulators for Higher Output Current

9.2.2.1 Design Requirements
Table 3 shows the design requirements.

                                                 Table 3. Design Requirements
                                         DESIGN PARAMETER            EXAMPLE VALUE
                                          Input voltage (VIN)              6.0 V
                                         Output voltage (VOUT)             3.3 V
                                         Output current (IOUT)             3.0 A

9.2.2.2 Detailed Design Procedure
In an application requiring higher output current, an adjustable output regular can be placed in parallel with a
fixed output regulator to increase the current capacity. Two sense resistors and a comparator can be used to
control the feedback loop of the adjustable regulator in order to balance the current between the two regulators.
In Figure 35 resistors R1 and R2 are used to sense the current flowing into each regulator and should have a
very low resistance to avoid unnecessary power loss. R1 and R2 should have the same value and a tolerance of
1% or better so the current is shared equally between the regulators. For this example, a value of 0.01 Ω will be
used.



20       Submit Documentation Feedback                                          Copyright © 2008–2015, Texas Instruments Incorporated

                           Product Folder Links: TPS7A4501 TPS7A4515 TPS7A4518 TPS7A4525 TPS7A4533
```

## Page 21

```text
                                                        TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
www.ti.com                                                                       SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015


The TLV3691 rail-to-rail nanopower comparator output will alternate between VIN and GND depending on the
currents flowing into each of the two regulators. To design this control circuit, begin by looking at the case where
the two output currents are approximately equal and the comparator output is low. In this case, the output of the
TPS7A4501 should be set the same as the fixed voltage regulator. The TPS7A4533 has a 3.3 V fixed output, so
this will be the set point for the adjustable regulator. Begin by selecting a R7 value less than 4.17 kΩ. In this
example, 3.3 kΩ will be used. R5 will need to have a high resistance to satisfy Equation 14, for this example 100
kΩ was chosen. Then find the parallel resistance of R5 and R7 since they are both connected from the ADJ pin
to GND using Equation 10.
                   R5 ´ R7
      (R5 | |R7) =          = 3.19kΩ
                   R5 + R7                                                                                       (10)
Once the R5 and R7 parallel resistance in calculated, the value for R6 can be found using Equation 11.
          V
    R6 = OUT (R5 | |R7) - (R5 || R7)
          1.22V                                                                                                         (11)
           3.3V
    R6 =        (3.19kW ) - (3.19kW )
          1.22V                                                                                                         (12)
       R6 = 5.45 kΩ                                                                                                     (13)
In the case where the TPS7A4533 is sourcing more current than TPS7A4501, the comparator output will go high.
This will lower the voltage at the ADJ pin causing the TPS7A4501 to try and raise the output voltage by sourcing
more current. The TPS7A4533 will then react by sourcing less current to try and keep the output from rising.
When the current through the TPS7A4533 becomes less than the TPS7A4501, the comparator output will return
to GND. In order for this to happen, Equation 14 must be satisfied:
          æ R7 ö                     æ R6 ö
      VIN ç
               +    ÷ + (VIN - VOUT )ç R5 + R6 ÷ < Vref
          è R5   R7 ø                è         ø                                                             (14)
          æ     3.3kW     ö          æ     5.45kW     ö
       6V ç               ÷ + (2.7V) ç 100kW + 5.45kW ÷ < 1.21V
          è 100kW + 3.3kW ø          è                ø                                                                 (15)
       0.19 V + 0.14 V < 1.21 V                                                                                         (16)
       0.33 V < 1.21 V                                                                                                  (17)

9.2.2.3 Application Curve




                                     Figure 36. Parallel Regulators Sharing Load Current




Copyright © 2008–2015, Texas Instruments Incorporated                                  Submit Documentation Feedback      21
                            Product Folder Links: TPS7A4501 TPS7A4515 TPS7A4518 TPS7A4525 TPS7A4533
```

## Page 22

```text
TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015                                                                        www.ti.com


10 Power Supply Recommendations
The device is designed to operate with an input voltage supply up to 20 V. The minimum input voltage should
provide adequate headroom greater than the dropout voltage in order for the device to have a regulated output. If
the input supply is noisy, additional input capacitors with low ESR can help improve the output noise
performance.

11 Layout

11.1 Layout Guidelines
1. For best performance, all traces should be as short as possible.
2. Use wide traces for IN, OUT, and GND to minimize the parasitic electrical effects.
3. A minimum output capacitor of 10 μF with an ESR of 3 Ω or less is recommended to prevent oscillations.
   X5R and X7R dielectrics are preferred.
4. Place the Output Capacitor as close as possible to the OUT pin of the device.
5. The tab of the DCQ package should be connected to ground.
6. The exposed thermal pad of the KTT package should be connected to a wide ground plane for effective heat
   dissipation.




22     Submit Documentation Feedback                                        Copyright © 2008–2015, Texas Instruments Incorporated

                        Product Folder Links: TPS7A4501 TPS7A4515 TPS7A4518 TPS7A4525 TPS7A4533
```

## Page 23

```text
                                                        TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
www.ti.com                                                                       SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015


11.2 Layout Example




                                             Figure 37. TO-263 Layout Example (KTT)




Copyright © 2008–2015, Texas Instruments Incorporated                                  Submit Documentation Feedback      23
                            Product Folder Links: TPS7A4501 TPS7A4515 TPS7A4518 TPS7A4525 TPS7A4533
```

## Page 24

```text
TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015                                                                        www.ti.com


Layout Example (continued)




                                       Figure 38. SOT-223 Layout Example (DCQ)


11.3 Thermal Considerations
The power handling capability of the device is limited by the recommended maximum operating junction
temperature (125°C). The power dissipated by the device is made up of two components:
 1. Output current multiplied by the input/output voltage differential: IOUT (VIN – VOUT)
 2. GND pin current multiplied by the input voltage: IGNDVIN
The GND pin current can be found using the GND pin current graphs in Typical Characteristics. Power
dissipation is equal to the sum of the two components listed above.
The TPS7A45xx series regulators have internal thermal limiting designed to protect the device during overload
conditions. For continuous normal conditions, the recommended maximum operating junction temperature is
125°C. It is important to give careful consideration to all sources of thermal resistance from junction to ambient.
Additional heat sources mounted nearby must also be considered.
For surface-mount devices, heat sinking is accomplished by using the heat-spreading capabilities of the PCB and
its copper traces. Copper board stiffeners and plated through-holes can also be used to spread the heat
generated by power devices.

24     Submit Documentation Feedback                                        Copyright © 2008–2015, Texas Instruments Incorporated

                        Product Folder Links: TPS7A4501 TPS7A4515 TPS7A4518 TPS7A4525 TPS7A4533
```

## Page 25

```text
                                                             TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
www.ti.com                                                                        SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015


Thermal Considerations (continued)
Table 4 lists thermal resistance for several different board sizes and copper areas. All measurements were taken
in still air on 1/16-inch FR-4 board with 1-oz copper.

                                       Table 4. Thermal Data (KTT Package, 5-Pin TO-263)
                                  COPPER AREA                                      THERMAL RESISTANCE
                                                                  BOARD AREA
                       TOPSIDE (1)               BACKSIDE                         (JUNCTION TO AMBIENT)
                         2500 mm2                 2500 mm2          2500 mm2              23°C/W
                                   2                     2
                         1000 mm                  2500 mm           2500 mm2              25°C/W
                         125 mm2                  2500 mm2          2500 mm2              33°C/W

                 (1)   Device is mounted on topside.

11.3.1 Calculating Junction Temperature
Example: Given an output voltage of 3.3 V, an input voltage range of 4 to 6 V, an output current range of 0 to
500 mA, and a maximum ambient temperature of 50°C, what is the operating junction temperature?
The power dissipated by the device is equal to:
       IOUT(MAX)(VIN(MAX) – VOUT) + IGND(VIN(MAX))
       where
             •   IOUT(MAX) = 500 mA
             •   VIN(MAX) = 6 V
             •   IGND at (IOUT = 500 mA, VIN = 6 V) = 10 mA                                                              (18)
So,
       P = 500 mA × (6 V – 3.3 V) + 10 mA × 6 V = 1.41 W                                                                 (19)
Using a KTT package, the thermal resistance is in the range of 23°C/W to 33°C/W, depending on the copper
area. So the junction temperature rise above ambient is approximately equal to:
       1.41 W × 28°C/W = 39.5 °C                                                                                         (20)
The junction temperature rise can then be added to the maximum ambient temperature to find the operating
junction temperature (TJ):
       TJ = 50°C + 39.5°C = 89.5°C                                                                                       (21)




Copyright © 2008–2015, Texas Instruments Incorporated                                   Submit Documentation Feedback      25
                            Product Folder Links: TPS7A4501 TPS7A4515 TPS7A4518 TPS7A4525 TPS7A4533
```

## Page 26

```text
TPS7A4501, TPS7A4515, TPS7A4518, TPS7A4525, TPS7A4533
SLVS720F – JUNE 2008 – REVISED NOVEMBER 2015                                                                                    www.ti.com


12 Device and Documentation Support

12.1 Related Links
The table below lists quick access links. Categories include technical documents, support and community
resources, tools and software, and quick access to sample or buy.

                                                       Table 5. Related Links
                                                                        TECHNICAL                TOOLS &                 SUPPORT &
       PARTS           PRODUCT FOLDER           SAMPLE & BUY
                                                                        DOCUMENTS               SOFTWARE                 COMMUNITY
     TPS7A4501              Click here              Click here             Click here             Click here               Click here
     TPS7A4515              Click here              Click here             Click here             Click here               Click here
     TPS7A4518              Click here              Click here             Click here             Click here               Click here
     TPS7A4525              Click here              Click here             Click here             Click here               Click here
     TPS7A4533              Click here              Click here             Click here             Click here               Click here


12.2 Community Resources
The following links connect to TI community resources. Linked contents are provided "AS IS" by the respective
contributors. They do not constitute TI specifications and do not necessarily reflect TI's views; see TI's Terms of
Use.
TI E2E™ Online Community TI's Engineer-to-Engineer (E2E) Community. Created to foster collaboration
           among engineers. At e2e.ti.com, you can ask questions, share knowledge, explore ideas and help
           solve problems with fellow engineers.
Design Support TI's Design Support Quickly find helpful E2E forums along with design support tools and
           contact information for technical support.

12.3 Trademarks
E2E is a trademark of Texas Instruments.
All other trademarks are the property of their respective owners.
12.4 Electrostatic Discharge Caution
         These devices have limited built-in ESD protection. The leads should be shorted together or the device placed in conductive foam
         during storage or handling to prevent electrostatic damage to the MOS gates.


12.5 Glossary
SLYZ022 — TI Glossary.
   This glossary lists and explains terms, acronyms, and definitions.

13 Mechanical, Packaging, and Orderable Information
The following pages include mechanical, packaging, and orderable information. This information is the most
current data available for the designated devices. This data is subject to change without notice and revision of
this document. For browser-based versions of this data sheet, refer to the left-hand navigation.




26     Submit Documentation Feedback                                                    Copyright © 2008–2015, Texas Instruments Incorporated

                         Product Folder Links: TPS7A4501 TPS7A4515 TPS7A4518 TPS7A4525 TPS7A4533
```

## Page 27

```text
                                                                                                                                 PACKAGE OPTION ADDENDUM

  www.ti.com                                                                                                                                                    10-Nov-2025




PACKAGING INFORMATION

 Orderable part number   Status   Material type    Package | Pins     Package qty | Carrier   RoHS      Lead finish/       MSL rating/        Op temp (°C)   Part marking
                           (1)         (2)                                                     (3)      Ball material      Peak reflow                            (6)
                                                                                                             (4)                (5)

    TPS7A4501DCQR        Active    Production     SOT-223 (DCQ) | 6    2500 | LARGE T&R        Yes        NIPDAU        Level-2-260C-1 YEAR    -40 to 125     PS7A4501
   TPS7A4501DCQR.A       Active    Production     SOT-223 (DCQ) | 6    2500 | LARGE T&R        Yes        NIPDAU        Level-2-260C-1 YEAR    -40 to 125     PS7A4501
   TPS7A4501DCQRG4       Active    Production     SOT-223 (DCQ) | 6    2500 | LARGE T&R        Yes        NIPDAU        Level-2-260C-1 YEAR    -40 to 125     PS7A4501
  TPS7A4501DCQRG4.A      Active    Production     SOT-223 (DCQ) | 6    2500 | LARGE T&R        Yes        NIPDAU        Level-2-260C-1 YEAR    -40 to 125     PS7A4501
    TPS7A4501DCQT        Active    Production     SOT-223 (DCQ) | 6     250 | SMALL T&R        Yes        NIPDAU        Level-2-260C-1 YEAR    -40 to 125     PS7A4501
   TPS7A4501DCQT.A       Active    Production     SOT-223 (DCQ) | 6     250 | SMALL T&R        Yes        NIPDAU        Level-2-260C-1 YEAR    -40 to 125     PS7A4501
   TPS7A4501DCQTG4       Active    Production     SOT-223 (DCQ) | 6     250 | SMALL T&R        Yes        NIPDAU        Level-2-260C-1 YEAR    -40 to 125     PS7A4501
  TPS7A4501DCQTG4.A      Active    Production     SOT-223 (DCQ) | 6     250 | SMALL T&R        Yes        NIPDAU        Level-2-260C-1 YEAR    -40 to 125     PS7A4501
    TPS7A4501KTTR        Active    Production        DDPAK/            500 | LARGE T&R         Yes          SN          Level-3-245C-168 HR    -40 to 125    TPS7A4501
                                                  TO-263 (KTT) | 5
   TPS7A4501KTTR.A       Active    Production        DDPAK/            500 | LARGE T&R         Yes          SN          Level-3-245C-168 HR    -40 to 125    TPS7A4501
                                                  TO-263 (KTT) | 5
    TPS7A4515DCQR        Active    Production     SOT-223 (DCQ) | 6    2500 | LARGE T&R        Yes        NIPDAU        Level-2-260C-1 YEAR    -40 to 125     PS7A4515
   TPS7A4515DCQR.A       Active    Production     SOT-223 (DCQ) | 6    2500 | LARGE T&R        Yes        NIPDAU        Level-2-260C-1 YEAR    -40 to 125     PS7A4515
    TPS7A4515DCQT        Active    Production     SOT-223 (DCQ) | 6     250 | SMALL T&R        Yes        NIPDAU        Level-2-260C-1 YEAR        -          PS7A4515
   TPS7A4515DCQT.A       Active    Production     SOT-223 (DCQ) | 6     250 | SMALL T&R        Yes        NIPDAU        Level-2-260C-1 YEAR    -40 to 125     PS7A4515
    TPS7A4515KTTR        Active    Production        DDPAK/            500 | LARGE T&R         Yes          SN          Level-3-245C-168 HR    -40 to 125    TPS7A4515
                                                  TO-263 (KTT) | 5
   TPS7A4515KTTR.A       Active    Production        DDPAK/            500 | LARGE T&R         Yes          SN          Level-3-245C-168 HR    -40 to 125    TPS7A4515
                                                  TO-263 (KTT) | 5
    TPS7A4518DCQR        Active    Production     SOT-223 (DCQ) | 6    2500 | LARGE T&R        Yes        NIPDAU        Level-2-260C-1 YEAR    -40 to 125     PS7A4518
   TPS7A4518DCQR.A       Active    Production     SOT-223 (DCQ) | 6    2500 | LARGE T&R        Yes        NIPDAU        Level-2-260C-1 YEAR    -40 to 125     PS7A4518
    TPS7A4518DCQT        Active    Production     SOT-223 (DCQ) | 6     250 | SMALL T&R        Yes        NIPDAU        Level-2-260C-1 YEAR        -          PS7A4518
   TPS7A4518DCQT.A       Active    Production     SOT-223 (DCQ) | 6     250 | SMALL T&R        Yes        NIPDAU        Level-2-260C-1 YEAR    -40 to 125     PS7A4518
    TPS7A4518KTTR        Active    Production        DDPAK/            500 | LARGE T&R         Yes          SN          Level-3-245C-168 HR    -40 to 125    TPS7A4518
                                                  TO-263 (KTT) | 5
   TPS7A4518KTTR.A       Active    Production        DDPAK/            500 | LARGE T&R         Yes          SN          Level-3-245C-168 HR    -40 to 125    TPS7A4518
                                                  TO-263 (KTT) | 5
   TPS7A4518KTTRG3       Active    Production        DDPAK/            500 | LARGE T&R         Yes          SN          Level-3-245C-168 HR    -40 to 125    TPS7A4518
                                                  TO-263 (KTT) | 5
    TPS7A4525DCQR        Active    Production     SOT-223 (DCQ) | 6    2500 | LARGE T&R        Yes        NIPDAU        Level-2-260C-1 YEAR    -40 to 125     PS7A4525


                                                                                      Addendum-Page 1
```

## Page 28

```text
                                                                                                                                                                     PACKAGE OPTION ADDENDUM

       www.ti.com                                                                                                                                                                                                   10-Nov-2025




       Orderable part number          Status     Material type      Package | Pins      Package qty | Carrier       RoHS             Lead finish/               MSL rating/          Op temp (°C)               Part marking
                                        (1)            (2)                                                            (3)            Ball material              Peak reflow                                           (6)
                                                                                                                                          (4)                       (5)

        TPS7A4525DCQR.A               Active      Production      SOT-223 (DCQ) | 6      2500 | LARGE T&R            Yes               NIPDAU           Level-2-260C-1 YEAR            -40 to 125                 PS7A4525
          TPS7A4525DCQT               Active      Production      SOT-223 (DCQ) | 6       250 | SMALL T&R            Yes               NIPDAU           Level-2-260C-1 YEAR                 -                     PS7A4525
         TPS7A4525DCQT.A              Active      Production      SOT-223 (DCQ) | 6       250 | SMALL T&R            Yes               NIPDAU           Level-2-260C-1 YEAR            -40 to 125                 PS7A4525
          TPS7A4525KTTR               Active      Production          DDPAK/              500 | LARGE T&R            Yes                  SN             Level-3-245C-168 HR           -40 to 125                TPS7A4525
                                                                   TO-263 (KTT) | 5
         TPS7A4525KTTR.A              Active      Production          DDPAK/              500 | LARGE T&R            Yes                  SN             Level-3-245C-168 HR           -40 to 125                TPS7A4525
                                                                   TO-263 (KTT) | 5
         TPS7A4533DCQR                Active      Production      SOT-223 (DCQ) | 6      2500 | LARGE T&R            Yes               NIPDAU           Level-2-260C-1 YEAR            -40 to 125                 PS7A4533
        TPS7A4533DCQR.A               Active      Production      SOT-223 (DCQ) | 6      2500 | LARGE T&R            Yes               NIPDAU           Level-2-260C-1 YEAR            -40 to 125                 PS7A4533
          TPS7A4533DCQT               Active      Production      SOT-223 (DCQ) | 6       250 | SMALL T&R            Yes               NIPDAU           Level-2-260C-1 YEAR            -40 to 125                 PS7A4533
         TPS7A4533DCQT.A              Active      Production      SOT-223 (DCQ) | 6       250 | SMALL T&R            Yes               NIPDAU           Level-2-260C-1 YEAR            -40 to 125                 PS7A4533
        TPS7A4533DCQTG4               Active      Production      SOT-223 (DCQ) | 6       250 | SMALL T&R            Yes               NIPDAU           Level-2-260C-1 YEAR            -40 to 125                 PS7A4533
       TPS7A4533DCQTG4.A              Active      Production      SOT-223 (DCQ) | 6       250 | SMALL T&R            Yes               NIPDAU           Level-2-260C-1 YEAR            -40 to 125                 PS7A4533
          TPS7A4533KTTR               Active      Production          DDPAK/              500 | LARGE T&R            Yes                  SN             Level-3-245C-168 HR           -40 to 125                TPS7A4533
                                                                   TO-263 (KTT) | 5
         TPS7A4533KTTR.A              Active      Production          DDPAK/              500 | LARGE T&R            Yes                  SN             Level-3-245C-168 HR           -40 to 125                TPS7A4533
                                                                   TO-263 (KTT) | 5

(1)
      Status: For more details on status, see our product life cycle.

(2)
   Material type: When designated, preproduction parts are prototypes/experimental devices, and are not yet approved or released for full production. Testing and final process, including without limitation quality assurance,
reliability performance testing, and/or process qualification, may not yet be complete, and this item is subject to further changes or possible discontinuation. If available for ordering, purchases will be subject to an additional
waiver at checkout, and are intended for early internal evaluation purposes only. These items are sold without warranties of any kind.

(3)
      RoHS values: Yes, No, RoHS Exempt. See the TI RoHS Statement for additional information and value definition.

(4)
   Lead finish/Ball material: Parts may have multiple material finish options. Finish options are separated by a vertical ruled line. Lead finish/Ball material values may wrap to two lines if the finish value exceeds the maximum
column width.

(5)
  MSL rating/Peak reflow: The moisture sensitivity level ratings and peak solder (reflow) temperatures. In the event that a part has multiple moisture sensitivity ratings, only the lowest level per JEDEC standards is shown.
Refer to the shipping label for the actual reflow temperature that will be used to mount the part to the printed circuit board.

(6)
      Part marking: There may be an additional marking, which relates to the logo, the lot trace code information, or the environmental category of the part.



                                                                                                          Addendum-Page 2
```

## Page 29

```text
                                                                                                                                                                      PACKAGE OPTION ADDENDUM

    www.ti.com                                                                                                                                                                                                   10-Nov-2025




Multiple part markings will be inside parentheses. Only one part marking contained in parentheses and separated by a "~" will appear on a part. If a line is indented then it is a continuation of the previous line and the two
combined represent the entire part marking for that device.

Important Information and Disclaimer:The information provided on this page represents TI's knowledge and belief as of the date that it is provided. TI bases its knowledge and belief on information provided by third parties, and
makes no representation or warranty as to the accuracy of such information. Efforts are underway to better integrate information from third parties. TI has taken and continues to take reasonable steps to provide representative
and accurate information but may not have conducted destructive testing or chemical analysis on incoming materials and chemicals. TI and TI suppliers consider certain information to be proprietary, and thus CAS numbers
and other limited information may not be available for release.

In no event shall TI's liability arising out of such information exceed the total purchase price of the TI part(s) at issue in this document sold by TI to Customer on an annual basis.




                                                                                                          Addendum-Page 3
```

## Page 30

```text
                                                                                PACKAGE MATERIALS INFORMATION

www.ti.com                                                                                                                                         27-Oct-2024



TAPE AND REEL INFORMATION

       REEL DIMENSIONS                                                                       TAPE DIMENSIONS
                                                                                        K0       P1



                                                                                                                        B0 W
                                          Reel
                                        Diameter
                                                                                     Cavity           A0
                                                                 A0   Dimension designed to accommodate the component width
                                                                 B0   Dimension designed to accommodate the component length
                                                                 K0   Dimension designed to accommodate the component thickness
                                                                 W    Overall width of the carrier tape
                                                                 P1   Pitch between successive cavity centers


                                         Reel Width (W1)
                              QUADRANT ASSIGNMENTS FOR PIN 1 ORIENTATION IN TAPE

                                                                                                       Sprocket Holes


                                                   Q1       Q2          Q1    Q2

                                                   Q3       Q4          Q3    Q4                  User Direction of Feed



                                                             Pocket Quadrants


*All dimensions are nominal
             Device           Package Package Pins               SPQ        Reel   Reel   A0                  B0         K0     P1     W     Pin1
                               Type Drawing                               Diameter Width (mm)                (mm)       (mm)   (mm)   (mm) Quadrant
                                                                            (mm) W1 (mm)
    TPS7A4501DCQR             SOT-223     DCQ           6        2500        330.0        12.4        7.1    7.45       1.88   8.0    12.0    Q3
  TPS7A4501DCQRG4             SOT-223     DCQ           6        2500        330.0        12.4        7.1    7.45       1.88   8.0    12.0    Q3
    TPS7A4501DCQT             SOT-223     DCQ           6         250        177.8        12.4        7.1    7.45       1.88   8.0    12.0    Q3
   TPS7A4501DCQTG4            SOT-223     DCQ           6         250        177.8        12.4        7.1    7.45       1.88   8.0    12.0    Q3
    TPS7A4501KTTR             DDPAK/       KTT          5         500        330.0        24.4        10.8   16.3       5.11   16.0   24.0    Q2
                              TO-263
    TPS7A4515DCQR             SOT-223     DCQ           6        2500        330.0        12.4        7.1    7.45       1.88   8.0    12.0    Q3
    TPS7A4515DCQT             SOT-223     DCQ           6         250        177.8        12.4        7.1    7.45       1.88   8.0    12.0    Q3
    TPS7A4515KTTR             DDPAK/       KTT          5         500        330.0        24.4        10.8   16.3       5.11   16.0   24.0    Q2
                              TO-263
    TPS7A4518DCQR             SOT-223     DCQ           6        2500        330.0        12.4        7.1    7.45       1.88   8.0    12.0    Q3
    TPS7A4518DCQT             SOT-223     DCQ           6         250        177.8        12.4        7.1    7.45       1.88   8.0    12.0    Q3
    TPS7A4518KTTR             DDPAK/       KTT          5         500        330.0        24.4        10.8   16.3       5.11   16.0   24.0    Q2
                              TO-263
    TPS7A4525DCQR             SOT-223     DCQ           6        2500        330.0        12.4        7.1    7.45       1.88   8.0    12.0    Q3
    TPS7A4525DCQT             SOT-223     DCQ           6         250        177.8        12.4        7.1    7.45       1.88   8.0    12.0    Q3




                                                                        Pack Materials-Page 1
```

## Page 31

```text
                                                           PACKAGE MATERIALS INFORMATION

www.ti.com                                                                                                          27-Oct-2024



             Device   Package Package Pins   SPQ       Reel   Reel   A0            B0     K0     P1     W     Pin1
                       Type Drawing                  Diameter Width (mm)          (mm)   (mm)   (mm)   (mm) Quadrant
                                                       (mm) W1 (mm)
    TPS7A4525KTTR     DDPAK/    KTT    5     500       330.0     24.4      10.8   16.3   5.11   16.0   24.0    Q2
                      TO-263
    TPS7A4533DCQR     SOT-223   DCQ    6     2500      330.0     12.4      7.1    7.45   1.88   8.0    12.0    Q3
    TPS7A4533DCQT     SOT-223   DCQ    6     250       177.8     12.4      7.1    7.45   1.88   8.0    12.0    Q3
  TPS7A4533DCQTG4     SOT-223   DCQ    6     250       177.8     12.4      7.1    7.45   1.88   8.0    12.0    Q3
    TPS7A4533KTTR     DDPAK/    KTT    5     500       330.0     24.4      10.8   16.3   5.11   16.0   24.0    Q2
                      TO-263




                                                   Pack Materials-Page 2
```

## Page 32

```text
                                                                PACKAGE MATERIALS INFORMATION

www.ti.com                                                                                                              27-Oct-2024



 TAPE AND REEL BOX DIMENSIONS




                                                               Width (mm)
                                                                              H
                      W




                                                          L




*All dimensions are nominal
             Device           Package Type   Package Drawing   Pins         SPQ    Length (mm)   Width (mm)   Height (mm)
    TPS7A4501DCQR               SOT-223           DCQ           6           2500      346.0        346.0         29.0
   TPS7A4501DCQRG4              SOT-223           DCQ           6           2500      346.0        346.0         29.0
     TPS7A4501DCQT              SOT-223           DCQ           6           250       223.0        270.0         35.0
   TPS7A4501DCQTG4              SOT-223           DCQ           6           250       223.0        270.0         35.0
     TPS7A4501KTTR            DDPAK/TO-263        KTT           5           500       340.0        340.0         38.0
    TPS7A4515DCQR               SOT-223           DCQ           6           2500      346.0        346.0         29.0
     TPS7A4515DCQT              SOT-223           DCQ           6           250       180.0        180.0         85.0
     TPS7A4515KTTR            DDPAK/TO-263        KTT           5           500       340.0        340.0         38.0
    TPS7A4518DCQR               SOT-223           DCQ           6           2500      346.0        346.0         41.0
     TPS7A4518DCQT              SOT-223           DCQ           6           250       223.0        270.0         35.0
     TPS7A4518KTTR            DDPAK/TO-263        KTT           5           500       340.0        340.0         38.0
    TPS7A4525DCQR               SOT-223           DCQ           6           2500      346.0        346.0         41.0
     TPS7A4525DCQT              SOT-223           DCQ           6           250       180.0        180.0         85.0
     TPS7A4525KTTR            DDPAK/TO-263        KTT           5           500       340.0        340.0         38.0
    TPS7A4533DCQR               SOT-223           DCQ           6           2500      346.0        346.0         29.0
     TPS7A4533DCQT              SOT-223           DCQ           6           250       180.0        180.0         85.0
   TPS7A4533DCQTG4              SOT-223           DCQ           6           250       180.0        180.0         85.0
     TPS7A4533KTTR            DDPAK/TO-263        KTT           5           500       340.0        340.0         38.0




                                                        Pack Materials-Page 3
```

## Page 33

```text
                                                                                                             PACKAGE OUTLINE
 DCQ0006A                                                               SCALE 2.000
                                                                                                            SOT - 1.8 mm max height
                                                                                                                      PLASTIC SMALL OUTLINE




                                                                                                    7.26
                                                                                                    6.86

                           0.08                                                                     3.6
                                                                                                                      B
                                                                                                    3.4                                     A
                                                     PIN 1                                         NOTE 3
                                               INDEX AREA

                                                                    1

                                                             1.27
                                                             TYP

                                                                                                                                           6.6
                                                                                                                                           6.4
                                                                                                                                          NOTE 3
                                                    5.08                                                                          6




                                                                                                                                3.05
                                                                                                                                2.95
                                                                                                                          0.1     C A B
                                                                    5
                                                      0.51
                                                 5X
   0.10                                               0.41
                   (1.6)
   0.02                                  0.1        C A B
                 1.8 MAX




                                                                                                                                           0.32
                                         0.25                                                                                              0.24
                                  GAGE PLANE


                                                                                            1.14            SEATING PLANE
                                                C          0 -8                             0.91
                                                           TYP




                                                                                                                                4214845/C 11/2021
NOTES:

1. All linear dimensions are in millimeters. Any dimensions in parenthesis are for reference only. Dimensioning and tolerancing
   per ASME Y14.5M.
2. This drawing is subject to change without notice.
3. This dimension does not include mold flash, protrusions, or gate burrs. Mold flash, protrusions, or gate burrs shall not
   exceed 0.15 mm per side.




                                                                                      www.ti.com
```

## Page 34

```text
                                                                                   EXAMPLE BOARD LAYOUT
 DCQ0006A                                                                                        SOT - 1.8 mm max height
                                                                                                               PLASTIC SMALL OUTLINE




                                                                      (6)



                                       1
                                                                                                            0.2 TYP
                            4X (1.27)



                                                                              (1.35)
                              SYMM
                                                                                                              (3.2)
                                                                                                        6
                  (R0.05) TYP




                           5X (0.65)                                                                        (0.775) TYP

                                       5
                                                                                            (2.05)
                                           5X (2.05)                 PKG



                                                       LAND PATTERN EXAMPLE
                                                          EXPOSED METAL SHOWN
                                                               SCALE: 10X




                      SOLDER MASK                         METAL         METAL UNDER                            SOLDER MASK
                          OPENING                                       SOLDER MASK                            OPENING


            EXPOSED METAL
                                                                                                                      EXPOSED METAL
                                            0.07 MAX                                            0.07 MIN
                                            ALL AROUND                                          ALL AROUND


                                                         SOLDER MASK DETAILS



                                                                                                                       4214845/C 11/2021

NOTES: (continued)

4. Publication IPC-7351 may have alternate designs.
5. Solder mask tolerances between and around signal pads can vary based on board fabrication site.
6. Vias are optional depending on application, refer to device data sheet. If any vias are implemented, refer to their locations shown
   on this view. It is recommended that vias under paste be filled, plugged or tented.




                                                                    www.ti.com
```

## Page 35

```text
                                                                                   EXAMPLE STENCIL DESIGN
 DCQ0006A                                                                                    SOT - 1.8 mm max height
                                                                                                           PLASTIC SMALL OUTLINE




                                                                 (6)


                                   1
                                                                                                  (0.56) TYP
                        (1.27) TYP

                                                                                                         (0.755)

                           SYMM

                                                                                                  6

                 (R0.05) TYP                                           4X (1.31)




                                                                                            4X (0.92)
                       5X (0.65)
                                   5
                                       5X (2.05)               SYMM




                                                    SOLDER PASTE EXAMPLE
                                                   BASED ON 0.125 mm THICK STENCIL
                                                             SCALE: 10X




                                                                                                                   4214845/C 11/2021

NOTES: (continued)

7. Laser cutting apertures with trapezoidal walls and rounded corners may offer better paste release. IPC-7525 may have alternate
   design recommendations.
8. Board assembly site may have different recommendations for stencil design.




                                                                  www.ti.com
```

## Page 36

```text

```

## Page 37

```text

```

## Page 38

```text
                                         IMPORTANT NOTICE AND DISCLAIMER
TI PROVIDES TECHNICAL AND RELIABILITY DATA (INCLUDING DATASHEETS), DESIGN RESOURCES (INCLUDING REFERENCE
DESIGNS), APPLICATION OR OTHER DESIGN ADVICE, WEB TOOLS, SAFETY INFORMATION, AND OTHER RESOURCES “AS IS”
AND WITH ALL FAULTS, AND DISCLAIMS ALL WARRANTIES, EXPRESS AND IMPLIED, INCLUDING WITHOUT LIMITATION ANY
IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE OR NON-INFRINGEMENT OF THIRD
PARTY INTELLECTUAL PROPERTY RIGHTS.
These resources are intended for skilled developers designing with TI products. You are solely responsible for (1) selecting the appropriate
TI products for your application, (2) designing, validating and testing your application, and (3) ensuring your application meets applicable
standards, and any other safety, security, regulatory or other requirements.
These resources are subject to change without notice. TI grants you permission to use these resources only for development of an
application that uses the TI products described in the resource. Other reproduction and display of these resources is prohibited. No license
is granted to any other TI intellectual property right or to any third party intellectual property right. TI disclaims responsibility for, and you fully
indemnify TI and its representatives against any claims, damages, costs, losses, and liabilities arising out of your use of these resources.
TI’s products are provided subject to TI’s Terms of Sale, TI’s General Quality Guidelines, or other applicable terms available either on
ti.com or provided in conjunction with such TI products. TI’s provision of these resources does not expand or otherwise alter TI’s applicable
warranties or warranty disclaimers for TI products. Unless TI explicitly designates a product as custom or customer-specified, TI products
are standard, catalog, general purpose devices.
TI objects to and rejects any additional or different terms you may propose.
IMPORTANT NOTICE

                                                Copyright © 2025, Texas Instruments Incorporated
                                                                Last updated 10/2025
```
