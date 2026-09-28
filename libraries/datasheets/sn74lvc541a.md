# sn74lvc541a

Original PDF: [sn74lvc541a.pdf](sn74lvc541a.pdf)

SHA-256: `2dd5b2769640eeb604841ccd2a6b2783e12d6d590296aca9d4c3cf9632572634`

Source: https://www.ti.com/lit/ds/symlink/sn74lvc541a.pdf

Parts: SN74LVC541APWR

GPS calibrator references: U3, U4

Machine-extracted text; consult the original PDF for drawings, symbols and table alignment.

## Page 1

```text
                                                                                                          SN54LVC541A, SN74LVC541A
                                                                                               SCAS298O – JANUARY 1993 – REVISED JUNE 2026

                     SNx4LVC541A Octal Buffers/Drivers With 3-State Outputs
1 Features                                                              3 Description
•   Operates from 1.65V to 3.6V                                         The SNx4LVC541A contains eight non-inverting
•   Inputs accept voltages to 5.5V                                      buffers with 3-state outputs. The active low output
•   Maximum tpd of 5.1ns at 3.3V                                        enable pins (OE1 and OE2) control all eight channels,
•   Typical VOLP (output ground bounce) <0.8V at VCC                    and are configured so that both must be low for the
    = 3.3V, TA = 25°C                                                   outputs to be active.
•   Typical VOHV (output VOH undershoot) >2V at VCC
                                                                                            Package Information
    = 3.3V, TA = 25°C
                                                                               PART                          PACKAGE
•   Support mixed-mode signal operation on all ports                          NUMBER
                                                                                           PACKAGE(1)
                                                                                                              SIZE(2)
                                                                                                                            BODY SIZE(3)
    (5V input/output voltage with 3.3V VCC)
                                                                                                           24.2mm ×        24.2mm ×
•   Ioff supports live insertion, partial-power-down                                      J (CDIP, 20)
                                                                                                           7.62mm          6.92mm
    mode, and back-drive protection
                                                                                                           13.09mm ×       13.09mm ×
•   Latch-up performance exceeds 100mA per JESD                          SN54LVC541A W (CFP, 20)
                                                                                                           8.13mm          6.92mm
    78
                                                                                                           8.89mm ×        8.89mm ×
•   On products compliant to MIL-PRF-38535, all                                           FK (LCCC, 20)
                                                                                                           8.89mm          8.89mm
    parameters are tested unless otherwise noted, on                                      PW (TSSOP,       6.5mm ×         6.5mm ×
    all other products, production processing does not                                    20)              6.4mm           4.4mm
    necessarily include testing of all parameters                                                          12.80mm ×       12.8mm ×
                                                                                          DW (SOIC, 20)
                                                                                                           10.3mm          7.5mm
2 Applications
                                                                                                           7.2mm ×         7.50mm ×
                                                                                          DB (SSOP, 20)
•   Drive an indicator LED                                                                                 7.8mm           5.3mm
•   Redrive a digital signal                                                                               12.6mm ×        12.6mm ×
                                                                                          NS (SOP, 20)
•   Drive a transmission line                                                                              7.8mm           5.3mm
                                                                         SN74LVC541A
•   Hold a signal during controller reset                                                 DGS (VSSOP,      5.1mm ×         5.1mm ×
                                                                                          20)              4.9mm           3.0mm
                                                                                          RKS (VQFN,       4.5mm ×         4.5mm ×
                                                                                          20)              2.5mm           2.5mm
                                                                                          DGV (TVSOP,      5.0mm ×         5.0mm ×
                                                                                          20)              6.4mm           4.4mm
                                                                                          RGY (VQFN,       4.5mm ×         4.5mm ×
                                                                                          20)              3.5mm           3.5mm

                                                                        (1)    For more information, see Mechanical, Packaging, and
                                                                               Orderable Information.
                                                                        (2)    The package size (length × width) is a nominal value and
                                                                               includes pins, where applicable.
                                                                        (3)    The body size (length × width) is a nominal value and does
                                                                               not include pins.

                                                            Shared Control Logic

                                             OE1


                                             OE2




                                               Ax                                         Yx


                                                         One of Eight 3-State Buffers


                                                    Functional Block Diagram


     An IMPORTANT NOTICE at the end of this data sheet addresses availability, warranty, changes, use in safety-critical applications,
     intellectual property matters and other important disclaimers. PRODUCTION DATA.
```

## Page 2

```text
SN54LVC541A, SN74LVC541A
SCAS298O – JANUARY 1993 – REVISED JUNE 2026                                                                                                                      www.ti.com


                                                                        Table of Contents
1 Features............................................................................1     7.1 Overview................................................................... 10
2 Applications..................................................................... 1       7.2 Functional Block Diagram......................................... 10
3 Description.......................................................................1       7.3 Feature Description...................................................10
4 Pin Configuration and Functions...................................3                       7.4 Device Functional Modes..........................................11
5 Specifications.................................................................. 5      8 Application and Implementation.................................. 12
  5.1 Absolute Maximum Ratings........................................ 5                    8.1 Application Information............................................. 12
  5.2 ESD Ratings............................................................... 5          8.2 Typical Application.................................................... 12
  5.3 Recommended Operating Conditions.........................6                            8.3 Power Supply Recommendations.............................14
  5.4 Thermal Information....................................................6              8.4 Layout....................................................................... 14
  5.5 Electrical Characteristics—DC Limit Changes............7                            9 Device and Documentation Support............................16
  5.6 Switching Characteristics - SN54LVC541A................ 7                             9.1 Documentation Support............................................ 16
  5.7 Switching Characteristics, SN74LVC541A –40°C                                          9.2 Receiving Notification of Documentation Updates....16
    to 85°C.......................................................................... 8     9.3 Support Resources................................................... 16
  5.8 Switching Characteristics, SN74LVC541A –40°C                                          9.4 Trademarks............................................................... 16
    to 125°C........................................................................ 8      9.5 Electrostatic Discharge Caution................................16
  5.9 Operating Characteristics........................................... 8                9.6 Glossary....................................................................16
  5.10 Typical Characteristics.............................................. 8            10 Revision History.......................................................... 16
6 Parameter Measurement Information............................ 9                         11 Mechanical, Packaging, and Orderable
7 Detailed Description......................................................10              Information.................................................................... 18




2       Submit Document Feedback                                                                                         Copyright © 2026 Texas Instruments Incorporated

                                                        Product Folder Links: SN54LVC541A SN74LVC541A
```

## Page 3

```text
                                                                                                                  SN54LVC541A, SN74LVC541A
www.ti.com                                                                                      SCAS298O – JANUARY 1993 – REVISED JUNE 2026


4 Pin Configuration and Functions




                                                                                                                 OE1


                                                                                                                             OE2
                                                                                                                       VCC
                                                                                                      A2
                                                                                                           A1
                 OE1          1               20          VCC
                   A1         2               19          OE2                                         3    2     1     20 19
                   A2         3               18          Y1                               A3     4                        18       Y1
                   A3         4               17          Y2                               A4     5                            17   Y2
                   A4         5               16          Y3                               A5     6                            16   Y3
                   A5         6               15          Y4                               A6     7                            15   Y4

                                                  14                                       A7     8               14                Y5
                   A6         7                           Y5
                                                                                                      9 10 11 12 13
                   A7         8               13          Y6




                                                                                                                             Y6
                                                                                                           GND


                                                                                                                       Y7
                                                                                                      A8
                   A8       9                     12      Y7




                                                                                                                 Y8
                 GND       10                     11      Y8
                                                                               Figure 4-2. SN54LVC541A FK Package (Top View)
       Figure 4-1. SN54LVC541A J , W Package (Top
                          View)

                                                                    Pin Functions
               PIN
                                      TYPE(1)          DESCRIPTION
      NAME              NO.
 A1               2                       I            Input for channel 1
 A2               3                       I            Input for channel 2
 A3               4                       I            Input for channel 3
 A4               5                       I            Input for channel 4
 A5               6                       I            Input for channel 5
 A6               7                       I            Input for channel 6
 A7               8                       I            Input for channel 7
 A8               9                       I            Input for channel 8
 GND              10                     G             Ground
 OE1              1                       I            Output enable 1, active low
 OE2              19                      I            Output enable 2, active low
 VCC              20                      P            Positive supply
 Y1               18                     O             Output for channel 1
 Y2               17                     O             Output for channel 2
 Y3               16                     O             Output for channel 3
 Y4               15                     O             Output for channel 4
 Y5               14                     O             Output for channel 5
 Y6               13                     O             Output for channel 6
 Y7               12                     O             Output for channel 7
 Y8               11                     O             Output for channel 8

(1)    Signal Types: I = Input, O = Output, G = Ground, P = Power.




Copyright © 2026 Texas Instruments Incorporated                                                                      Submit Document Feedback   3
                                                  Product Folder Links: SN54LVC541A SN74LVC541A
```

## Page 4

```text
SN54LVC541A, SN74LVC541A
SCAS298O – JANUARY 1993 – REVISED JUNE 2026                                                                                                     www.ti.com


                                    OE1 VCC
                                                                                                 OE1      1                    20       VCC
                                     1    20
                         A1    2                   19   OE2                                       A1      2                    19       OE2
                         A2    3                   18    Y1                                       A2      3                    18       Y1
                         A3    4                   17    Y2                                       A3      4                    17       Y2
                         A4    5                   16    Y3                                       A4      5                    16       Y3
                                                                                                  A5      6                    15       Y4
                         A5    6     PAD           15    Y4
                                                                                                  A6      7                    14       Y5
                         A6    7                   14    Y5
                                                                                                  A7      8                    13       Y6
                         A7    8                   13    Y6
                                                                                                  A8      9                    12       Y7
                         A8    9                   12    Y7
                                     10   11                                                    GND       10                   11       Y8
                                   GND      Y8
    Figure 4-3. SN74LVC541A RKS Package (Top View)                                       Figure 4-4. SN74LVC541A PW , DW , NS , DB ,
                                                                                                      DGS , DGV Package
                                                                                                          (Top View)

                                                                        Pin Functions
                 PIN
                                          TYPE(1)          DESCRIPTION
         NAME            NO.
    A1              2                          I           Input for channel 1
    A2              3                          I           Input for channel 2
    A3              4                          I           Input for channel 3
    A4              5                          I           Input for channel 4
    A5              6                          I           Input for channel 5
    A6              7                          I           Input for channel 6
    A7              8                          I           Input for channel 7
    A8              9                          I           Input for channel 8
    GND             10                         G           Ground
    OE1             1                          I           Output enable 1, active low
    OE2             19                         I           Output enable 2, active low
                                                           The thermal pad can be connected to GND or left floating. Do not connect to any other
            Thermal Pad(2)                     —
                                                           signal or supply.
    VCC             20                         P           Positive supply
    Y1              18                         O           Output for channel 1
    Y2              17                         O           Output for channel 2
    Y3              16                         O           Output for channel 3
    Y4              15                         O           Output for channel 4
    Y5              14                         O           Output for channel 5
    Y6              13                         O           Output for channel 6
    Y7              12                         O           Output for channel 7
    Y8              11                         O           Output for channel 8

(1)       Signal Types: I = Input, O = Output, G = Ground, P = Power.
(2)       RKS package only.




4         Submit Document Feedback                                                                             Copyright © 2026 Texas Instruments Incorporated

                                                        Product Folder Links: SN54LVC541A SN74LVC541A
```

## Page 5

```text
                                                                                                             SN54LVC541A, SN74LVC541A
www.ti.com                                                                                       SCAS298O – JANUARY 1993 – REVISED JUNE 2026


5 Specifications
5.1 Absolute Maximum Ratings
over operating free-air temperature range (unless otherwise noted)(1)
                                                                                                                    MIN         MAX      UNIT
 VCC        Supply voltage range                                                                                   –0.5            6.5     V
 VI         Input voltage range(2)                                                                                 –0.5            6.5     V
 VO         Voltage range applied to any output in the high-impedance or power-off state(2)                        –0.5            6.5     V
 VO         Voltage range applied to any output in the high or low state(2) (3)                                    –0.5    VCC + 0.5       V
 IIK        Input clamp current                                        VI < 0                                                      –50    mA
 IOK        Output clamp current                                       VO < 0                                                      –50    mA
 IO         Continuous output current                                                                                              ±50    mA
            Continuous current through VCC or GND                                                                               ±100      mA
 Tstg       Storage temperature                                                                                      -65           150    °C

(1)     Operation outside the Absolute Maximum Ratings may cause permanent device damage. Absolute maximum ratings do not imply
        functional operation of the device at these or any other conditions beyond those listed under Recommended Operating Conditions.
        If briefly operating outside the Recommended Operating Conditions but within the Absolute Maximum Ratings, the device may not
        sustain damage, but it may not be fully functional. Operating the device in this manner may affect device reliability, functionality,
        performance, and shorten the device lifetime.
(2)     The input negative-voltage and output voltage ratings can be exceeded if the input and output current ratings are observed.
(3)     The value of VCC is provided in the Recommended Operating Conditions table.

5.2 ESD Ratings
                                                                                                                           VALUE         UNIT

               Electrostatic      Human-body model (HBM), per ANSI/ESDA/JEDEC JS-001(1)                                    ±2000
 V(ESD)                                                                                                                                   V
               discharge          Charged-device model (CDM), per ANSI/ESDA/JEDEC JS-002(2)                                ±1000

(1)     JEDEC document JEP155 states that 500V HBM allows safe manufacturing with a standard ESD control process.
(2)     JEDEC document JEP157 states that 250V CDM allows safe manufacturing with a standard ESD control process.




Copyright © 2026 Texas Instruments Incorporated                                                               Submit Document Feedback          5
                                                  Product Folder Links: SN54LVC541A SN74LVC541A
```

## Page 6

```text
SN54LVC541A, SN74LVC541A
SCAS298O – JANUARY 1993 – REVISED JUNE 2026                                                                                                www.ti.com

5.3 Recommended Operating Conditions
over operating free-air temperature range (unless otherwise noted)(1)
                                                                                        SN54LVC541A                 SN74LVC541A
                                                                                                                                             UNIT
                                                                                            MIN      MAX              MIN           MAX
                                                        Operating                              2       3.6           1.65            3.6
    VCC       Supply voltage                                                                                                                   V
                                                        Data retention only                  1.5                      1.5
                                                        VCC = 1.65V to 1.95V                                   0.65 × VCC
    VIH       High-level input voltage                  VCC = 2.3V to 2.7V                                            1.7                      V
                                                        VCC = 2.7V to 3.6V                     2                        2
                                                        VCC = 1.65V to 1.95V                                                 0.35 × VCC
    VIL       Low-level input voltage                   VCC = 2.3V to 2.7V                                                           0.7       V
                                                        VCC = 2.7V to 3.6V                             0.8                           0.8
    VI        Input voltage                                                                    0       5.5              0            5.5       V
                                                        High or low state                      0      VCC               0           VCC
    VO        Output voltage                                                                                                                   V
                                                        3-state                                0       5.5              0            5.5
                                                        VCC = 1.65V                                                                  –4
                                                        VCC = 2.3V                                                                   –8
    IOH       High-level output current                                                                                                       mA
                                                        VCC = 2.7V                                    –12                           –12
                                                        VCC = 3V                                      –24                           –24
                                                        VCC = 1.65V                                                                    4
                                                        VCC = 2.3V                                                                     8
    IOL       Low-level output current                                                                                                        mA
                                                        VCC = 2.7V                                     12                            12
                                                        VCC = 3V                                       24                            24
    TA        Operating free-air temperature                                                –55       125             –40           125       °C

(1)       All unused inputs of the device must be held at VCC or GND to verify proper device operation. Refer to the TI application note,
          Implications of Slow or Floating CMOS Inputs.

5.4 Thermal Information
                                                                            THERMAL METRIC(1)
          PACKAGE              PINS                                                                                                         UNIT
                                               RθJA        RθJC(top)          RθJB          ΨJT              ΨJB        RθJC(bot)
    PW (TSSOP)                  20             120.3         62.5             82.4         16.0              81.5           N/A             °C/W
    DGS (VSSOP)                 20             129.9         72.4             86.1         18.6              85.8           N/A             °C/W
    RKS (VQFN)                  20             87.2          93.4             59.8         24.9              59.6           44.3            °C/W
    DB (SSOP)                   20             121.7         86.8             87.8         44.7              87             N/A             °C/W
    DW (SOIC)                   20             114.8         84.1             88.8         55.8              87.8           N/A             °C/W
    NS (SOP)                    20             116.3         82.4             86.2         43.9              85.5           N/A             °C/W
    DGV (TVSOP)                 20             128.7         43.8             70.4          3.2              69.7           N/A             °C/W
    RGY (VQFN)                  20             82.84         88.73            56.81        32.37          56.62             42.09           °C/W

(1)       For more information about traditional and new thermal metrics, see the Semiconductor and IC Package Thermal Metrics application
          note.




6         Submit Document Feedback                                                                     Copyright © 2026 Texas Instruments Incorporated

                                                 Product Folder Links: SN54LVC541A SN74LVC541A
```

## Page 7

```text
                                                                                                                     SN54LVC541A, SN74LVC541A
www.ti.com                                                                                            SCAS298O – JANUARY 1993 – REVISED JUNE 2026


5.5 Electrical Characteristics—DC Limit Changes
over recommended operating free-air temperature range (unless otherwise noted)
                                                               –55°C TO 125°C              –40°C TO 85°C                 –40°C TO 125°C
 PARAMETE
                       TEST CONDITIONS                VCC       SN54LVC541A                SN74LVC541A                    SN74LVC541A               UNIT
     R
                                                                MIN    TYP(1)   MAX           MIN   TYP(1)    MAX            MIN    TYP(1)   MAX
                                                    1.65V to
                                                                                       VCC – 0.2                      VCC – 0.3
                                                      3.6V
                 IOH = –100μA
                                                    2.7V to    VCC –
                                                     3.6V        0.2
                 IOH = –4mA                          1.65V                                 1.20                              1.20
      VOH                                                                                                                                             V
                 IOH = –8mA                          2.3V                                     1.7                             1.7
                                                     2.7V        2.2                          2.2                             2.2
                 IOH = –12mA
                                                      3V         2.4                          2.4                             2.4
                 IOH = –24mA                          3V         2.2                          2.2                             2.2
                                                    1.65V to
                                                                                                               0.2                            0.3
                                                      3.6V
                 IOL = 100μA
                                                    2.7V to
                                                                                 0.2
                                                     3.6V
      VOL        IOL = 4mA                           1.65V                                                    0.45                           0.45     V

                 IOL = 8mA                           2.3V                                                      0.7                            0.7
                 IOL = 12mA                          2.7V                        0.4                           0.4                            0.4
                 IOL = 24mA                           3V                        0.55                          0.55                           0.55
        II       VI = 0 to 5.5V                      3.6V                        ±5                            ±5                             ±5     μA
       Ioff      VI or VO = 5.5V                       0                                                      ±10                            ±10     μA
       IOZ       VO = 0 to 5.5V                      3.6V                       ±15                           ±10                            ±10     μA
                 VI = VCC or GND                                                 10                            10                             10
      ICC                              IO = 0        3.6V                                                                                            μA
                 3.6V ≤ VI ≤ 5.5V(2)                                             10                            10                             10
                 One input at VCC – 0.6V,
                                                    2.7V to
      ΔICC       Other inputs at VCC or                                         500                           500                            500     μA
                                                     3.6V
                 GND
       Ci        VI = VCC or GND                     3.3V                  4                            4                               4            pF
       Co        VO = VCC or GND                     3.3V                 5.5                          5.5                             5.5           pF

(1)    All typical values are at VCC = 3.3V, TA = 25°C.
(2)    This applies in the disabled state only.

5.6 Switching Characteristics - SN54LVC541A
over recommended operating free-air temperature range (unless otherwise noted) (see Section 6)
                                                                                                    SN54LVC541A
                                          FROM                    TO
             PARAMETER                                                                 VCC = 2.7V               VCC = 3.3V ± 0.3V              UNIT
                                         (INPUT)               (OUTPUT)
                                                                                        MIN           MAX             MIN            MAX
                tpd                             A                  Y                                    5.6              1             5.1      ns
                ten                         OE                     Y                                    7.5              1              7       ns
                tdis                        OE                     Y                                    7.7              1              7       ns




Copyright © 2026 Texas Instruments Incorporated                                                                      Submit Document Feedback              7
                                                    Product Folder Links: SN54LVC541A SN74LVC541A
```

## Page 8

```text
SN54LVC541A, SN74LVC541A
SCAS298O – JANUARY 1993 – REVISED JUNE 2026                                                                                                                       www.ti.com

5.7 Switching Characteristics, SN74LVC541A –40°C to 85°C
over recommended operating free-air temperature range (unless otherwise noted) (see Section 6)
                                                                                                           SN74LVC541A
                                                                                                           –40°C TO 85°C
                                  FROM        TO
     PARAMETER                                                 VCC = 1.8V              VCC = 2.5V                                                VCC = 3.3V             UNIT
                                 (INPUT)   (OUTPUT)                                                                         VCC = 2.7V
                                                                ± 0.15V                  ± 0.2V                                                    ± 0.3V
                                                                MIN         MAX         MIN                   MAX            MIN     MAX           MIN          MAX
                  tpd               A          Y                  1         15.7                   1            7.8            1         5.6        1.5          5.1     ns
                  ten              OE          Y                  1         17.5                   1           10.5            1         7.5        1.5            7     ns
                  tdis             OE          Y                  1         16.5                   1             9             1         7.7        1.5            7     ns
                 tsk(o)                                                                                                                                            1     ns


5.8 Switching Characteristics, SN74LVC541A –40°C to 125°C
over recommended operating free-air temperature range (unless otherwise noted) (see Section 6)
                                                                                                           SN74LVC541A
                                                                                                       –40°C TO 125°C
                                  FROM        TO
     PARAMETER                                                 VCC = 1.8V               VCC = 2.5V                                               VCC = 3.3V             UNIT
                                 (INPUT)   (OUTPUT)                                                                         VCC = 2.7V
                                                                ± 0.15V                   ± 0.2V                                                   ± 0.3V
                                                                MIN         MAX           MIN                  MAX           MIN     MAX           MIN          MAX
                  tpd              A          Y                    1        16.3                   1            8.3            1         6.1         1           5.6     ns
                  ten              OE         Y                    1        18.5                   1           11.1            1           8         1           7.5     ns
                  tdis             OE         Y                    1        17.3                   1            9.7            1         8.2         1           7.5     ns
                 tsk(o)                                                                                                                                          1.5     ns


5.9 Operating Characteristics
TA = 25°C
                                                                                 TEST                       VCC = 1.8V          VCC = 2.5V         VCC = 3.3V
                                    PARAMETER                                                                                                                          UNIT
                                                                              CONDITIONS                       TYP                  TYP               TYP

                   Power dissipation capacitance         Outputs enabled                                        65                   58                  33
    Cpd                                                                           f = 10MHz                                                                             pF
                   per buffer/driver                     Outputs disabled                                        2                   2                    2


5.10 Typical Characteristics

                   6                                                                                   4
                 5.5       TPD
                                                                                                   3.5
                   5
                 4.5                                                                                   3
                   4
                                                                                                   2.5
                 3.5
                                                                                        TPD - ns
      TPD - ns




                   3                                                                                   2
                 2.5
                                                                                                   1.5
                   2
                 1.5                                                                                   1
                   1
                                                                                                   0.5
                 0.5                                                                                                                                              TPD
                   0                                                                                   0
                       0            1                2                 3    3.5                        -100           -50        0          50            100          150
                                           VCC - V                                                                              Temperature (qC)                        D002
                                                                             D001

    Figure 5-1. SN74LVC541A TPD Across VCC at 25°C                                                         Figure 5-2. SN74LVC541A TPD Across
                                                                                                                    Temperature at 3.3V


8                Submit Document Feedback                                                                                      Copyright © 2026 Texas Instruments Incorporated

                                                         Product Folder Links: SN54LVC541A SN74LVC541A
```

## Page 9

```text
                                                                                                                         SN54LVC541A, SN74LVC541A
www.ti.com                                                                                                 SCAS298O – JANUARY 1993 – REVISED JUNE 2026


6 Parameter Measurement Information
                                                         VLOAD
                                       RL      S1            Open
    From Output                                                                                               TEST                  S1
      Under Test                                            GND
                                                                                                             tPLH/tPHL           Open
               CL
                                 RL                                                                          tPLZ/tPZL           VLOAD
      (see Note A)
                                                                                                             tPHZ/tPZH           GND


                          LOAD CIRCUIT


                                                       INPUTS
                                 VCC                                         VM        VLOAD          CL          RL           V∆
                                                  VI           tr/tf
                            1.8 V ± 0.15 V     VCC           ≤2 ns          VCC/2      2 × VCC       30 pF      1 kΩ          0.15 V
                            2.5 V ± 0.2 V      VCC           ≤2 ns          VCC/2      2 × VCC       30 pF      500 Ω         0.15 V
                                2.7 V          2.7 V        ≤2.5 ns         1.5 V        6V          50 pF      500 Ω         0.3 V
                            3.3 V ± 0.3 V      2.7 V        ≤2.5 ns         1.5 V        6V          50 pF      500 Ω         0.3 V


                                                                                                                                                    VI
                                                                                     Timing Input                              VM
                                                                                                                                                    0V
                                 tw

                                                                       VI                                            tsu            th
                                                                                                                                                    VI
  Input                VM                          VM
                                                                                       Data Input                 VM                         VM
                                                                       0V                                                                           0V
                      VOLTAGE WAVEFORMS                                                                       VOLTAGE WAVEFORMS
                        PULSE DURATION                                                                       SETUP AND HOLD TIMES

                                                               VI                                                                                   VI
                            VM               VM                                         Output
       Input                                                                                                    VM                   VM
                                                                                        Control
                                                               0V                                                                                   0V
               tPLH                                     tPHL                                        tPZL                                    tPLZ
                                                                                          Output
                                                               VOH                                                                                  VLOAD/2
                                                                                     Waveform 1
     Output                       VM                   VM                                                            VM
                                                                                     S1 at VLOAD                                         VOL + V∆
                                                               VOL                  (see Note B)                                                    VOL
               tPHL                                     tPLH                                        tPZH                                    tPHZ
                                                               VOH                       Output
                                                                                                                                                    VOH
                                  VM                   VM                            Waveform 2                                          VOH − V∆
     Output                                                                                                          VM
                                                                                      S1 at GND
                                                               VOL                                                                                  ≈0 V
                                                                                    (see Note B)
                  VOLTAGE WAVEFORMS                                                                      VOLTAGE WAVEFORMS
               PROPAGATION DELAY TIMES                                                                 ENABLE AND DISABLE TIMES
          INVERTING AND NONINVERTING OUTPUTS                                                         LOW- AND HIGH-LEVEL ENABLING

 NOTES: A. CL includes probe and jig capacitance.
        B. Waveform 1 is for an output with internal conditions such that the output is low, except when disabled by the output control.
           Waveform 2 is for an output with internal conditions such that the output is high, except when disabled by the output control.
        C. All input pulses are supplied by generators having the following characteristics: PRR ≤ 10 MHz, ZO = 50 Ω.
        D. The outputs are measured one at a time, with one transition per measurement.
        E. tPLZ and tPHZ are the same as tdis.
        F. tPZL and tPZH are the same as ten.
        G. tPLH and tPHL are the same as tpd.
        H. All parameters and waveforms are not applicable to all devices.

                                            Figure 6-1. Load Circuit and Voltage Waveforms




Copyright © 2026 Texas Instruments Incorporated                                                                            Submit Document Feedback           9
                                                  Product Folder Links: SN54LVC541A SN74LVC541A
```

## Page 10

```text
SN54LVC541A, SN74LVC541A
SCAS298O – JANUARY 1993 – REVISED JUNE 2026                                                                                        www.ti.com

7 Detailed Description
7.1 Overview
The SNx4LVC541A contains eight buffers with 3-state outputs. The active low output enable pins (OE1 and
OE2) control all eight channels, and are configured so that both must be low for the outputs to be active.
When the outputs are enabled, the outputs are actively driven low or high.
When the outputs are disabled, the outputs are set into the high-impedance state.
7.2 Functional Block Diagram
                                                   1
                                          OE1
                                                   19
                                          OE2


                                                   2                                 18
                                              A1                                            Y1




                                                             To Seven Other Channels
                                               Copyright © 2016, Texas Instruments Incorporated

                                      Figure 7-1. Logic Diagram (Positive Logic)

7.3 Feature Description
7.3.1 Balanced CMOS 3-State Outputs
This device includes balanced CMOS 3-state outputs: driving high, driving low, and high impedance. The term
balanced indicates that the device can sink and source similar currents. The drive capability of this device can
create fast edges into light loads, so consider routing and load conditions to prevent ringing. Additionally, the
outputs of this device can drive larger currents than the device can sustain without damage. Limit the output
power of the device to avoid damage from overcurrent. The electrical and thermal limits defined in the Absolute
Maximum Ratings must be followed at all times.
When placed into the high-impedance state, the output does not source or sink current except minor leakage
current as defined in the Electrical Characteristics table. In the high-impedance state, the device does not control
the output voltage. The output current is dependent on external factors. A floating node is a node that has no
other drivers connected, and the voltage is unknown. A pull-up or pull-down resistor can be connected to the
output to provide a known voltage at the output while the device is in the high-impedance state. The value
of the resistor depends on multiple factors, including parasitic capacitance and power consumption limitations.
Typically, a 10kΩ resistor meets these requirements.
Leave unused 3-state CMOS outputs disconnected.
7.3.2 Partial Power Down (Ioff)
This device includes circuitry to disable all outputs when the supply pin is held at 0V. When disabled, the outputs
neither source nor sink current, regardless of the input voltages. The amount of leakage current at each output is
defined by the Ioff specification in the Electrical Characteristics table.
7.3.3 Standard CMOS Inputs
This device includes standard CMOS inputs. Standard CMOS inputs are high impedance and are typically
modeled as a resistor in parallel with the input capacitance given in the Electrical Characteristics. The worst
case resistance is calculated with the maximum input voltage, given in the Absolute Maximum Ratings, and the
maximum input leakage current, given in the Electrical Characteristics, using Ohm's law (R = V ÷ I).
Standard CMOS inputs require that input signals transition between valid logic states quickly, as defined by the
input transition time or rate in the Recommended Operating Conditions table. Failing to meet this specification


10    Submit Document Feedback                                                                    Copyright © 2026 Texas Instruments Incorporated

                                       Product Folder Links: SN54LVC541A SN74LVC541A
```

## Page 11

```text
                                                                                                             SN54LVC541A, SN74LVC541A
www.ti.com                                                                                         SCAS298O – JANUARY 1993 – REVISED JUNE 2026


results in excessive power consumption and can cause oscillations. See more details in Implications of Slow or
Floating CMOS Inputs.
Do not leave standard CMOS inputs floating at any time during operation. Terminate unused inputs at VCC or
GND. If a system does not always drive an input, consider adding a pull-up or pull-down resistor to provide a
valid input voltage. The resistor value depends on multiple factors; a 10kΩ resistor, however, is recommended
and typically meets all requirements.
7.3.4 Clamp Diode Structure
Figure 7-2 shows the inputs and outputs to this device have negative clamping diodes only.

                                                     CAUTION
        Voltages beyond the values specified in the Absolute Maximum Ratings table can cause damage
        to the device. The input and output voltage ratings may be exceeded if the input and output clamp-
        current ratings are observed.




                   Figure 7-2. Electrical Placement of Clamping Diodes for Each Input and Output

7.4 Device Functional Modes
                                                          Table 7-1. Function Table
                                                          INPUTS(1)                        OUTPUT(2)
                                            OE1             OE2             A                      Y
                                              L               L             L                      L
                                              L               L             H                      H
                                              H              X              X                      Z
                                              X              H              X                      Z

                                      (1)    L = input low, H = input high, X = don't care
                                      (2)    L = output low, H = output high, Z = high impedance




Copyright © 2026 Texas Instruments Incorporated                                                               Submit Document Feedback     11
                                                  Product Folder Links: SN54LVC541A SN74LVC541A
```

## Page 12

```text
SN54LVC541A, SN74LVC541A
SCAS298O – JANUARY 1993 – REVISED JUNE 2026                                                                                 www.ti.com

8 Application and Implementation
                                                              Note
      Information in the following applications sections is not part of the TI component specification,
      and TI does not warrant its accuracy or completeness. TI’s customers are responsible for
      determining suitability of components for their purposes, as well as validating and testing their design
      implementation to confirm system functionality.

8.1 Application Information
SNx4LVC541A is a high drive CMOS device that can be used for a multitude of bus interface type applications
where output drive or PCB trace length is a concern.
8.2 Typical Application

               System      1A1        1Y1     Rd                                           1A1          1Y1
                                                                 Z0                                            Peripheral
              Controller
                                                              L > 12 cm
                             Transmitter                                                         Receiver

                                              Figure 8-1. Application Schematic

8.2.1 Design Requirements
8.2.1.1 Power Considerations
Verify that the desired supply voltage is within the range specified in the Electrical Characteristics. The supply
voltage sets the device electrical characteristics, as described in the Electrical Characteristics section.
The positive voltage supply must be capable of sourcing current equal to the total current to be sourced by all
outputs of the SNx4LVC541A plus the maximum static supply current, ICC, listed in the Electrical Characteristics,
and any transient current required for switching. The logic device can only source as much current that is
provided by the positive supply source. Verify that the maximum total current through VCC listed in the Absolute
Maximum Ratings is not exceeded.
The ground must be capable of sinking current equal to the total current to be sunk by all outputs of the
SNx4LVC541A plus the maximum supply current, ICC, listed in the Electrical Characteristics, and any transient
current required for switching. The logic device can only sink as much current that can be sunk into the ground
connection. Verify that the maximum total current through GND listed in the Absolute Maximum Ratings is not
exceeded.
The SNx4LVC541A can drive a load with a total capacitance less than or equal to 50pF while still meeting all of
the datasheet specifications. Larger capacitive loads can be applied; however, do not exceed 50pF.
The SNx4LVC541A can drive a load with total resistance described by RL ≥ VO / IO, with the output voltage and
current defined in the Electrical Characteristics table with VOH and VOL. When outputting in the HIGH state, the
output voltage in the equation is defined as the difference between the measured output voltage and the supply
voltage at the VCC pin.
Total power consumption can be calculated using the information provided in the CMOS Power Consumption
and Cpd Calculation application note.
Thermal increase can be calculated using the information provided in the Thermal Characteristics of Standard
Linear and Logic (SLL) Packages and Devices application note.

                                                     CAUTION
       The maximum junction temperature, TJ(max) listed in the Absolute Maximum Ratings, is an additional
       limitation to prevent damage to the device. Do not violate any values listed in the Absolute Maximum
       Ratings. These limits are provided to prevent damage to the device.


12    Submit Document Feedback                                                             Copyright © 2026 Texas Instruments Incorporated

                                           Product Folder Links: SN54LVC541A SN74LVC541A
```

## Page 13

```text
                                                                                                      SN54LVC541A, SN74LVC541A
www.ti.com                                                                                  SCAS298O – JANUARY 1993 – REVISED JUNE 2026


8.2.1.2 Input Considerations
Input signals must cross VIL(max) to be considered a logic LOW, and VIH(min) to be considered a logic HIGH. Do
not exceed the maximum input voltage range found in the Absolute Maximum Ratings.
Unused inputs must be terminated to either VCC or ground. The unused inputs can be directly terminated if the
input is completely unused, or the inputs can be connected with a pullup or pulldown resistor if the input is
used sometimes, but not always. A pullup resistor is used for a default state of HIGH, and a pulldown resistor is
used for a default state of LOW. The drive current of the controller, leakage current into the SNx4LVC541A (as
specified in the Electrical Characteristics), and the desired input transition rate limits the resistor size. A 10kΩ
resistor value is often used due to these factors.
The SNx4LVC541A has CMOS inputs and thus requires fast input transitions to operate correctly, as defined in
the Electrical Characteristics table. Slow input transitions can cause oscillations, additional power consumption,
and reduction in device reliability.
Refer to the Feature Description for additional information regarding the inputs for this device.
8.2.1.3 Output Considerations
The positive supply voltage is used to produce the output HIGH voltage. Drawing current from the output
decreases the output voltage as specified by the VOH specification in the Electrical Characteristics. The ground
voltage is used to produce the output LOW voltage. Sinking current into the output increases the output voltage
as specified by the VOL specification in the Electrical Characteristics.
Push-pull outputs that can be in opposite states, even for a very short time period, must never be connected
directly together. This can cause excessive current and damage to the device.
Two channels within the same device with the same input signals can be connected in parallel for additional
output drive strength.
Unused outputs can be left floating. Do not connect outputs directly to VCC or ground.
Refer to the Feature Description section for additional information regarding the outputs for this device.
8.2.2 Detailed Design Procedure
1. Add a decoupling capacitor from VCC to GND. The capacitor needs to be placed physically close to the
   device and electrically close to both the VCC and GND pins. An example layout is shown in the Layout
   section.
2. Verify that the capacitive load at the output is ≤ 50pF. Low load capacitance can be accomplished by
   providing short, appropriately sized traces from the SNx4LVC541A to the receiving device.
3. Verify that the resistive load at the output is larger than (VCC / IO(max))Ω. Never violate the maximum output
   current from the Absolute Maximum Ratings. Most CMOS inputs have a resistive load measured in MΩ;
   much larger than the minimum calculated previously.
4. Thermal issues are rarely a concern for logic gates; however, the power consumption and thermal increase
   can be calculated using the steps provided in the CMOS Power Consumption and Cpd Calculation
   application note.




Copyright © 2026 Texas Instruments Incorporated                                                        Submit Document Feedback     13
                                                  Product Folder Links: SN54LVC541A SN74LVC541A
```

## Page 14

```text
SN54LVC541A, SN74LVC541A
SCAS298O – JANUARY 1993 – REVISED JUNE 2026                                                                                       www.ti.com

8.2.3 Application Curves
                                               5
                                                                                      0
                                               4                                      22
                                                                                      50
                                              3.3


                                               2

                                               1

                                               0

                                              -1

                                              -2
                                                    0   15   30   45        60   75   90   100
                                                                  Time (ns)


     Figure 8-2. Simulated Signal Integrity at the Receiver With Different Damping Resistor (Rd) Values

8.3 Power Supply Recommendations
The power supply can be any voltage between the minimum and maximum supply voltage rating located in the
Recommended Operating Conditions. Each VCC terminal must have a good bypass capacitor to prevent power
disturbance.
A 0.1μF capacitor is recommended for this device. It is acceptable to parallel multiple bypass capacitors to
reject different frequencies of noise. The 0.1μF and 1μF capacitors are commonly used in parallel. The bypass
capacitor must be installed as close to the power terminal as possible for best results.
8.4 Layout
8.4.1 Layout Guidelines
•    Bypass capacitor placement
     – Place near the positive supply terminal of the device
     – Provide an electrically short ground return path
     – Use wide traces to minimize impedance
     – Keep the device, capacitors, and traces on the same side of the board whenever possible
•    Signal trace geometry
     – 8mil to 12mil trace width
     – Lengths less than 12cm to minimize transmission line effects
     – Avoid 90° corners for signal traces
     – Use an unbroken ground plane below signal traces
     – Flood fill areas around signal traces with ground
     – Parallel traces must be separated by at least 3x dielectric thickness
     – For traces longer than 12cm
        • Use impedance controlled traces
        • Source-terminate using a series damping resistor near the output
        • Avoid branches; buffer each signal that must branch separately




14    Submit Document Feedback                                                                   Copyright © 2026 Texas Instruments Incorporated

                                       Product Folder Links: SN54LVC541A SN74LVC541A
```

## Page 15

```text
                                                                                                                      SN54LVC541A, SN74LVC541A
www.ti.com                                                                                               SCAS298O – JANUARY 1993 – REVISED JUNE 2026


8.4.2 Layout Example
                          WORST                                        BETTER                                             BEST




                                                                 2W




                                                                               W
                                                                               ≥
                                                                                                                          ≥ 5W



                                                                                                            W
                                                                  W

                                Figure 8-3. Example Trace Corners for Improved Signal Integrity

                                  GND   VCC                                                                  VCC                  GND

                                    0.1 F
                                                                                                                       0.1 F
                                                                                                                     VCC
                            1                     14      VCC
                                                                                                                1         20
                            2                     13                                                        2              19
                            3                     12                                                        3              18
                            4                     11                                                        4              17
                            5                     10
                                                                                                            5              16
                            6                      9
                                                                                                            6       GND    15
                GND         7                      8
                                                                                                            7              14
   Figure 8-4. Example Bypass Capacitor Placement                                                           8              13
           for TSSOP and Similar Packages
                                                                                                            9              12
                                                                                                             10           11
                                                                                                                GND

                                                                                   Figure 8-5. Example Bypass Capacitor Placement
                                                                                            for WQFN and Similar Packages

                                                                 GND                   VCC
                                                                           0.1 F
                                                                           1       6    VCC
                                                                           2       5
                                                                GND        3       4

              Figure 8-6. Example Bypass Capacitor Placement for SOT, SC70 and Similar Packages

                                                       Transmitting Port               Receiving Port

                                                                22    Long controlled-impedance trace



                   Figure 8-7. Example Damping Resistor Placement for Improved Signal Integrity




Copyright © 2026 Texas Instruments Incorporated                                                                           Submit Document Feedback   15
                                                  Product Folder Links: SN54LVC541A SN74LVC541A
```

## Page 16

```text
SN54LVC541A, SN74LVC541A
SCAS298O – JANUARY 1993 – REVISED JUNE 2026                                                                                                        www.ti.com

9 Device and Documentation Support
TI offers an extensive line of development tools. Tools and software to evaluate the performance of the device,
generate code, and develop solutions are listed below.
9.1 Documentation Support
9.1.1 Related Documentation
For related documentation, see the following:
•    Texas Instruments, CMOS Power Consumption and Cpd Calculation application note
•    Texas Instruments, Designing With Logic application note
•    Texas Instruments, Thermal Characteristics of Standard Linear and Logic (SLL) Packages and Devices
     application note
9.2 Receiving Notification of Documentation Updates
To receive notification of documentation updates, navigate to the device product folder on ti.com. Click on
Notifications to register and receive a weekly digest of any product information that has changed. For change
details, review the revision history included in any revised document.
9.3 Support Resources
TI E2E™ support forums are an engineer's go-to source for fast, verified answers and design help — straight
from the experts. Search existing answers or ask your own question to get the quick design help you need.
Linked content is provided "AS IS" by the respective contributors. They do not constitute TI specifications and do
not necessarily reflect TI's views; see TI's Terms of Use.
9.4 Trademarks
TI E2E™ is a trademark of Texas Instruments.
All trademarks are the property of their respective owners.
9.5 Electrostatic Discharge Caution
                    This integrated circuit can be damaged by ESD. Texas Instruments recommends that all integrated circuits be handled
                    with appropriate precautions. Failure to observe proper handling and installation procedures can cause damage.
                    ESD damage can range from subtle performance degradation to complete device failure. Precision integrated circuits may
                    be more susceptible to damage because very small parametric changes could cause the device not to meet its published
                    specifications.


9.6 Glossary
 TI Glossary              This glossary lists and explains terms, acronyms, and definitions.

10 Revision History
NOTE: Page numbers for previous revisions may differ from page numbers in the current version.
Changes from June 1, 2014 to June 17, 2026 (from Revision N (June 2014) to Revision O (June
2026))                                                                                                                                                   Page
• Updated the numbering format for tables, figures, and cross-references throughout the document................. 1
• Moved ESD ratings to ESD Ratings table.......................................................................................................... 1
• Updated latch-up ratings to latest standards...................................................................................................... 1
• Updated Device Information format and included package size........................................................................ 1
• Updated Simplified Schematic ...........................................................................................................................1
• Updated Applications .........................................................................................................................................1
• Added DGS and RKS package information........................................................................................................1
• Changed RθJA for DB package from: 112.1°C/W to: 121.7°C/W.......................................................................6
• Changed RθJC(top) for DB package from: 73.6°C/W to: 86.8°C/W...................................................................6



16     Submit Document Feedback                                                                                Copyright © 2026 Texas Instruments Incorporated

                                                  Product Folder Links: SN54LVC541A SN74LVC541A
```

## Page 17

```text
                                                                                                                                SN54LVC541A, SN74LVC541A
www.ti.com                                                                                                       SCAS298O – JANUARY 1993 – REVISED JUNE 2026

•    Changed ΨJT for DB package from: 67.3°C/W to: 87.8°C/W............................................................................ 6
•    Changed ΨJB for DB package from: 33.3°C/W to: 44.7°C/W............................................................................6
•    Changed RθJC(bot) for DB package from: 66.9°C/W to: 87°C/W......................................................................6
•    Changed RθJA for DW package from: 99.4°C/W to: 114.8°C/W........................................................................6
•    Changed RθJC(top) for DW package from: 66.9°C/W to: 84.1°C/W..................................................................6
•    Changed ΨJT for DW package from: 66.9°C/W to: 88.8°C/W........................................................................... 6
•    Changed ΨJB for DW package from: 33.8°C/W to: 55.8°C/W...........................................................................6
•    Changed RθJC(bot) for DW package from: 66.5°C/W to: 87.8°C/W..................................................................6
•    Changed RθJA for NS package from: 90.3°C/W to: 116.3°C/W.........................................................................6
•    Changed RθJC(top) for NS package from: 56.6°C/W to: 82.4°C/W...................................................................6
•    Changed ΨJT for NS package from: 57.8°C/W to: 86.2°C/W............................................................................ 6
•    Changed ΨJB for NS package from: 28.7°C/W to: 43.9°C/W............................................................................6
•    Changed RθJC(bot) for NS package from: 57.4°C/W to: 85.5°C/W...................................................................6
•    Changed RθJA for PW package from: 100.8°C/W to: 120.3°C/W..................................................................... 6
•    Changed RθJC(top) for PW package from: 35.2°C/W to: 62.5°C/W.................................................................. 6
•    Changed ΨJT for PW package from: 51.8°C/W to: 82.4°C/W........................................................................... 6
•    Changed ΨJB for PW package from: 2.2°C/W to: 16°C/W................................................................................ 6
•    Changed RθJC(bot) for PW package from: 51.2°C/W to: 81.5°C/W.................................................................. 6
•    Added parallel trace spacing recommendation to layout guidelines. Changed wording of "Avoid branches;
     buffer signals that must branch separately" to "Avoid branches; buffer each signal that must branch
     separately"........................................................................................................................................................ 14



Changes from Revision M (May 2005) to Revision N (June 2014)                                                                                               Page
• Updated document to new TI data sheet format................................................................................................ 1
• Removed Ordering Information table................................................................................................................. 1
• Updated Ioff Feature bullet.................................................................................................................................. 1
• Updated Features to include Military Disclaimer................................................................................................ 1
• Added Device Information table......................................................................................................................... 1
• Added Applications ............................................................................................................................................1
• Changed MAX operating free-air temperature from 85°C to 125°C for SN74LVC541A.....................................6
• Updated Thermal Information table. .................................................................................................................. 6
• Added –40°C TO 125°C temperature range to Electrical Characteristics table for SN74LVC541A................... 7
• Added Switching Characteristics table –40°C TO 125°C temperature range for SN74LVC541A...................... 8
• Added Typical Characteristics............................................................................................................................ 8




Copyright © 2026 Texas Instruments Incorporated                                                                                 Submit Document Feedback                17
                                                     Product Folder Links: SN54LVC541A SN74LVC541A
```

## Page 18

```text
SN54LVC541A, SN74LVC541A
SCAS298O – JANUARY 1993 – REVISED JUNE 2026                                                                             www.ti.com

11 Mechanical, Packaging, and Orderable Information
The following pages include mechanical, packaging, and orderable information. This information is the most
current data available for the designated devices. This data is subject to change without notice and revision of
this document. For browser-based versions of this data sheet, refer to the left-hand navigation.




18    Submit Document Feedback                                                         Copyright © 2026 Texas Instruments Incorporated

                                       Product Folder Links: SN54LVC541A SN74LVC541A
```

## Page 19

```text
                                                                                                                                 PACKAGE OPTION ADDENDUM

  www.ti.com                                                                                                                                                    18-Sep-2026




PACKAGING INFORMATION

 Orderable part number   Status   Material type    Package | Pins    Package qty | Carrier    RoHS      Lead finish/       MSL rating/       Op temp (°C)    Part marking
                           (1)         (2)                                                     (3)      Ball material      Peak reflow                            (6)
                                                                                                             (4)                (5)

    5962-9759501Q2A      Active    Production      LCCC (FK) | 20         55 | TUBE            No          SNPB          N/A for Pkg Type     -55 to 125        5962-
                                                                                                                                                             9759501Q2A
                                                                                                                                                              SNJ54LVC
                                                                                                                                                               541AFK
    5962-9759501QRA      Active    Production       CDIP (J) | 20         20 | TUBE            No          SNPB          N/A for Pkg Type     -55 to 125    5962-9759501QR
                                                                                                                                                                   A
                                                                                                                                                            SNJ54LVC541AJ
    5962-9759501QSA      Active    Production       CFP (W) | 20          25 | TUBE            No          SNPB          N/A for Pkg Type     -55 to 125    5962-9759501QS
                                                                                                                                                                   A
                                                                                                                                                            SNJ54LVC541AW
   SN74LVC541ADBR        Active    Production      SSOP (DB) | 20     2000 | LARGE T&R         Yes        NIPDAU        Level-1-260C-UNLIM    -40 to 125       LC541A
  SN74LVC541ADBR.A       Active    Production      SSOP (DB) | 20     2000 | LARGE T&R         Yes        NIPDAU        Level-1-260C-UNLIM    -40 to 125       LC541A
  SN74LVC541ADBR.B       Active    Production      SSOP (DB) | 20     2000 | LARGE T&R         Yes        NIPDAU        Level-1-260C-UNLIM    -40 to 125       LC541A
  SN74LVC541ADBRG4       Active    Production      SSOP (DB) | 20     2000 | LARGE T&R         Yes        NIPDAU        Level-1-260C-UNLIM    -40 to 125       LC541A
   SN74LVC541ADGSR       Active    Production     VSSOP (DGS) | 20    5000 | LARGE T&R         Yes        NIPDAU        Level-1-260C-UNLIM    -40 to 125        C541A
   SN74LVC541ADGVR       Active    Production     TVSOP (DGV) | 20    2000 | LARGE T&R         Yes        NIPDAU        Level-1-260C-UNLIM    -40 to 125       LC541A
  SN74LVC541ADGVR.B      Active    Production     TVSOP (DGV) | 20    2000 | LARGE T&R         Yes        NIPDAU        Level-1-260C-UNLIM    -40 to 125       LC541A
 SN74LVC541ADGVRE4       Active    Production     TVSOP (DGV) | 20    2000 | LARGE T&R         Yes        NIPDAU        Level-1-260C-UNLIM    -40 to 125       LC541A
 SN74LVC541ADGVRG4       Active    Production     TVSOP (DGV) | 20    2000 | LARGE T&R         Yes        NIPDAU        Level-1-260C-UNLIM    -40 to 125       LC541A
    SN74LVC541ADW        Active    Production      SOIC (DW) | 20         25 | TUBE            Yes        NIPDAU        Level-1-260C-UNLIM    -40 to 125       LVC541A
   SN74LVC541ADW.B       Active    Production      SOIC (DW) | 20         25 | TUBE            Yes        NIPDAU        Level-1-260C-UNLIM    -40 to 125       LVC541A
  SN74LVC541ADWG4        Active    Production      SOIC (DW) | 20         25 | TUBE            Yes        NIPDAU        Level-1-260C-UNLIM    -40 to 125       LVC541A
 SN74LVC541ADWG4.B       Active    Production      SOIC (DW) | 20         25 | TUBE            Yes        NIPDAU        Level-1-260C-UNLIM    -40 to 125       LVC541A
   SN74LVC541ADWR        Active    Production      SOIC (DW) | 20     2000 | LARGE T&R         Yes        NIPDAU        Level-1-260C-UNLIM    -40 to 125       LVC541A
  SN74LVC541ADWR.A       Active    Production      SOIC (DW) | 20     2000 | LARGE T&R         Yes        NIPDAU        Level-1-260C-UNLIM    -40 to 125       LVC541A
  SN74LVC541ADWR.B       Active    Production      SOIC (DW) | 20     2000 | LARGE T&R         Yes        NIPDAU        Level-1-260C-UNLIM    -40 to 125       LVC541A
  SN74LVC541ADWRE4       Active    Production      SOIC (DW) | 20     2000 | LARGE T&R         Yes        NIPDAU        Level-1-260C-UNLIM    -40 to 125       LVC541A
   SN74LVC541ANS.B       Active    Production      SOP (NS) | 20          40 | TUBE            Yes        NIPDAU        Level-1-260C-UNLIM     -40 to 85       LVC541A
   SN74LVC541ANSG4       Active    Production      SOP (NS) | 20          40 | TUBE            Yes        NIPDAU        Level-1-260C-UNLIM    -40 to 125       LVC541A
  SN74LVC541ANSG4.B      Active    Production      SOP (NS) | 20          40 | TUBE            Yes        NIPDAU        Level-1-260C-UNLIM    -40 to 125       LVC541A
   SN74LVC541ANSR        Active    Production      SOP (NS) | 20      2000 | LARGE T&R         Yes        NIPDAU        Level-1-260C-UNLIM    -40 to 125       LVC541A


                                                                                      Addendum-Page 1
```

## Page 20

```text
                                                                                                                                                     PACKAGE OPTION ADDENDUM

       www.ti.com                                                                                                                                                                   18-Sep-2026




       Orderable part number          Status     Material type      Package | Pins      Package qty | Carrier    RoHS      Lead finish/       MSL rating/        Op temp (°C)    Part marking
                                        (1)            (2)                                                        (3)      Ball material      Peak reflow                             (6)
                                                                                                                                (4)                 (5)

        SN74LVC541ANSR.A              Active      Production            SOP (NS) | 20    2000 | LARGE T&R         Yes        NIPDAU        Level-1-260C-UNLIM     -40 to 125       LVC541A
        SN74LVC541ANSR.B              Active      Production            SOP (NS) | 20    2000 | LARGE T&R         Yes        NIPDAU        Level-1-260C-UNLIM     -40 to 125       LVC541A
         SN74LVC541APW                Active      Production       TSSOP (PW) | 20           70 | TUBE            Yes        NIPDAU        Level-1-260C-UNLIM     -40 to 125       LC541A
        SN74LVC541APW.B               Active      Production       TSSOP (PW) | 20           70 | TUBE            Yes        NIPDAU        Level-1-260C-UNLIM     -40 to 125       LC541A
        SN74LVC541APWG4               Active      Production       TSSOP (PW) | 20           70 | TUBE            Yes        NIPDAU        Level-1-260C-UNLIM     -40 to 125       LC541A
         SN74LVC541APWR               Active      Production       TSSOP (PW) | 20       2000 | LARGE T&R         Yes      NIPDAU | SN     Level-1-260C-UNLIM     -40 to 125       LC541A
        SN74LVC541APWR.A              Active      Production       TSSOP (PW) | 20       2000 | LARGE T&R         Yes        NIPDAU        Level-1-260C-UNLIM     -40 to 125       LC541A
        SN74LVC541APWR.B              Active      Production       TSSOP (PW) | 20       2000 | LARGE T&R         Yes        NIPDAU        Level-1-260C-UNLIM     -40 to 125       LC541A
       SN74LVC541APWRE4               Active      Production       TSSOP (PW) | 20       2000 | LARGE T&R         Yes        NIPDAU        Level-1-260C-UNLIM     -40 to 125       LC541A
       SN74LVC541APWRG4               Active      Production       TSSOP (PW) | 20       2000 | LARGE T&R         Yes        NIPDAU        Level-1-260C-UNLIM     -40 to 125       LC541A
      SN74LVC541APWRG4.A              Active      Production       TSSOP (PW) | 20       2000 | LARGE T&R         Yes        NIPDAU        Level-1-260C-UNLIM     -40 to 125       LC541A
      SN74LVC541APWRG4.B              Active      Production       TSSOP (PW) | 20       2000 | LARGE T&R         Yes        NIPDAU        Level-1-260C-UNLIM     -40 to 125       LC541A
         SN74LVC541APWT               Active      Production       TSSOP (PW) | 20        250 | SMALL T&R         Yes        NIPDAU        Level-1-260C-UNLIM     -40 to 125       LC541A
        SN74LVC541APWT.B              Active      Production       TSSOP (PW) | 20        250 | SMALL T&R         Yes        NIPDAU        Level-1-260C-UNLIM     -40 to 125       LC541A
        SN74LVC541ARGYR               Active      Production       VQFN (RGY) | 20       3000 | LARGE T&R         Yes        NIPDAU        Level-2-260C-1 YEAR    -40 to 125       LC541A
       SN74LVC541ARGYR.A              Active      Production       VQFN (RGY) | 20       3000 | LARGE T&R         Yes        NIPDAU        Level-2-260C-1 YEAR    -40 to 125       LC541A
       SN74LVC541ARGYR.B              Active      Production       VQFN (RGY) | 20       3000 | LARGE T&R         Yes        NIPDAU        Level-2-260C-1 YEAR    -40 to 125       LC541A
      SN74LVC541ARGYRG4               Active      Production       VQFN (RGY) | 20       3000 | LARGE T&R         Yes        NIPDAU        Level-2-260C-1 YEAR    -40 to 125       LC541A
         SNJ54LVC541AFK               Active      Production        LCCC (FK) | 20           55 | TUBE            No          SNPB           N/A for Pkg Type     -55 to 125        5962-
                                                                                                                                                                                 9759501Q2A
                                                                                                                                                                                  SNJ54LVC
                                                                                                                                                                                   541AFK
          SNJ54LVC541AJ               Active      Production            CDIP (J) | 20        20 | TUBE            No          SNPB           N/A for Pkg Type     -55 to 125    5962-9759501QR
                                                                                                                                                                                       A
                                                                                                                                                                                SNJ54LVC541AJ
          SNJ54LVC541AW               Active      Production            CFP (W) | 20         25 | TUBE            No          SNPB           N/A for Pkg Type     -55 to 125    5962-9759501QS
                                                                                                                                                                                       A
                                                                                                                                                                                SNJ54LVC541AW

(1)
      Status: For more details on status, see our product life cycle.




                                                                                                         Addendum-Page 2
```

## Page 21

```text
                                                                                                                                                                      PACKAGE OPTION ADDENDUM

       www.ti.com                                                                                                                                                                                                   18-Sep-2026




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

Multiple part markings will be inside parentheses. Only one part marking contained in parentheses and separated by a "~" will appear on a part. If a line is indented then it is a continuation of the previous line and the two
combined represent the entire part marking for that device.

Important Information and Disclaimer:The information provided on this page represents TI's knowledge and belief as of the date that it is provided. TI bases its knowledge and belief on information provided by third parties, and
makes no representation or warranty as to the accuracy of such information. Efforts are underway to better integrate information from third parties. TI has taken and continues to take reasonable steps to provide representative
and accurate information but may not have conducted destructive testing or chemical analysis on incoming materials and chemicals. TI and TI suppliers consider certain information to be proprietary, and thus CAS numbers
and other limited information may not be available for release.

In no event shall TI's liability arising out of such information exceed the total purchase price of the TI part(s) at issue in this document sold by TI to Customer on an annual basis.


OTHER QUALIFIED VERSIONS OF SN54LVC541A, SN74LVC541A :

• Catalog : SN74LVC541A
• Automotive : SN74LVC541A-Q1, SN74LVC541A-Q1
• Enhanced Product : SN74LVC541A-EP, SN74LVC541A-EP
• Military : SN54LVC541A

NOTE: Qualified Version Definitions:

           • Catalog - TI's standard catalog product


                                                                                                          Addendum-Page 3
```

## Page 22

```text
                                                                                                                      PACKAGE OPTION ADDENDUM

www.ti.com                                                                                                                              18-Sep-2026




   • Automotive - Q100 devices qualified for high-reliability automotive applications targeting zero defects
   • Enhanced Product - Supports Defense, Aerospace and Medical Applications
   • Military - QML certified for Military and Defense Applications




                                                                                                    Addendum-Page 4
```

## Page 23

```text
                                                                               PACKAGE MATERIALS INFORMATION

www.ti.com                                                                                                                                     10-Aug-2026



TAPE AND REEL INFORMATION

       REEL DIMENSIONS                                                                      TAPE DIMENSIONS
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


                                                 Q1        Q2          Q1    Q2

                                                 Q3        Q4          Q3    Q4                  User Direction of Feed



                                                            Pocket Quadrants


*All dimensions are nominal
             Device           Package Package Pins              SPQ        Reel   Reel   A0                  B0         K0     P1     W     Pin1
                               Type Drawing                              Diameter Width (mm)                (mm)       (mm)   (mm)   (mm) Quadrant
                                                                           (mm) W1 (mm)
   SN74LVC541ADBR              SSOP      DB           20        2000        330.0        16.4        8.2     7.5       2.5    12.0   16.0    Q1
  SN74LVC541ADGSR             VSSOP     DGS           20        5000        330.0        16.4        5.4     5.4       1.45   8.0    16.0    Q1
  SN74LVC541ADGVR             TVSOP     DGV           20        2000        330.0        12.4        6.9     5.6       1.6    8.0    12.0    Q1
   SN74LVC541ADWR              SOIC      DW           20        2000        330.0        24.4        10.8   13.3       2.7    12.0   24.0    Q1
   SN74LVC541ANSR              SOP       NS           20        2000        330.0        24.4        8.4    13.0       2.5    12.0   24.0    Q1
   SN74LVC541APWR             TSSOP      PW           20        2000        330.0        16.4        6.95    7.0       1.4    8.0    16.0    Q1
   SN74LVC541APWR             TSSOP      PW           20        2000        330.0        16.4        6.95    7.1       1.6    8.0    16.0    Q1
  SN74LVC541APWRG4            TSSOP      PW           20        2000        330.0        16.4        6.95    7.0       1.4    8.0    16.0    Q1
   SN74LVC541APWT             TSSOP      PW           20         250        330.0        16.4        6.95    7.0       1.4    8.0    16.0    Q1
  SN74LVC541ARGYR              VQFN     RGY           20        3000        330.0        12.4        3.71   4.71       1.1    8.0    12.0    Q1




                                                                       Pack Materials-Page 1
```

## Page 24

```text
                                                                PACKAGE MATERIALS INFORMATION

www.ti.com                                                                                                              10-Aug-2026



 TAPE AND REEL BOX DIMENSIONS




                                                               Width (mm)
                                                                              H
                      W




                                                          L




*All dimensions are nominal
             Device           Package Type   Package Drawing   Pins         SPQ    Length (mm)   Width (mm)   Height (mm)
    SN74LVC541ADBR               SSOP              DB           20          2000      353.0        353.0         32.0
   SN74LVC541ADGSR              VSSOP             DGS           20          5000      353.0        353.0         32.0
   SN74LVC541ADGVR              TVSOP             DGV           20          2000      353.0        353.0         32.0
   SN74LVC541ADWR                SOIC             DW            20          2000      356.0        356.0         45.0
    SN74LVC541ANSR                SOP              NS           20          2000      356.0        356.0         45.0
   SN74LVC541APWR               TSSOP              PW           20          2000      353.0        353.0         32.0
   SN74LVC541APWR               TSSOP              PW           20          2000      364.0        364.0         27.0
  SN74LVC541APWRG4              TSSOP              PW           20          2000      353.0        353.0         32.0
    SN74LVC541APWT              TSSOP              PW           20          250       353.0        353.0         32.0
   SN74LVC541ARGYR               VQFN             RGY           20          3000      353.0        353.0         32.0




                                                        Pack Materials-Page 2
```

## Page 25

```text
                                                               PACKAGE MATERIALS INFORMATION

www.ti.com                                                                                                   10-Aug-2026



TUBE

       T - Tube
        height                                                     L - Tube length


                      W - Tube
                       width


         B - Alignment groove width

*All dimensions are nominal
             Device           Package Name   Package Type   Pins       SPQ     L (mm)   W (mm)   T (µm)   B (mm)
    5962-9759501Q2A               FK            LCCC         20         55     506.98   12.06    2030      NA
    5962-9759501QSA                W             CFP         20         25     506.98   26.16    6220      NA
    SN74LVC541ADW                 DW            SOIC         20         25      507     12.83    5080      6.6
   SN74LVC541ADW.B                DW            SOIC         20         25      507     12.83    5080      6.6
   SN74LVC541ADWG4                DW            SOIC         20         25      507     12.83    5080      6.6
  SN74LVC541ADWG4.B               DW            SOIC         20         25      507     12.83    5080      6.6
   SN74LVC541ANS.B                NS             SOP         20         40      530      10.5    4000      4.1
   SN74LVC541ANSG4                NS             SOP         20         40      530      10.5    4000      4.1
  SN74LVC541ANSG4.B               NS             SOP         20         40      530      10.5    4000      4.1
    SN74LVC541APW                 PW           TSSOP         20         70      530      10.2    3600      3.5
   SN74LVC541APW.B                PW           TSSOP         20         70      530      10.2    3600      3.5
   SN74LVC541APWG4                PW           TSSOP         20         70      530      10.2    3600      3.5
    SNJ54LVC541AFK                FK            LCCC         20         55     506.98   12.06    2030      NA
     SNJ54LVC541AW                 W             CFP         20         25     506.98   26.16    6220      NA




                                                       Pack Materials-Page 3
```

## Page 26

```text
                                                                                                        PACKAGE OUTLINE
DB0020A                                                        SCALE 2.000
                                                                                                        SSOP - 2 mm max height
                                                                                                                 SMALL OUTLINE PACKAGE




                                                                                                                   C
                                    8.2
                                        TYP
       A                            7.4
                                                                                                               0.1 C
                                       PIN 1 INDEX AREA                                                                              SEATING
                                                                                     18X 0.65                                        PLANE
                                                                             20
             1




                                                                                      2X
     7.5
                                                                                     5.85
     6.9
    NOTE 3




            10
                                                             11                          0.38
                                                                                   20X
                                                                                         0.22
                                     5.6                                                 0.1    C A B
                 B
                                     5.0
                                    NOTE 4




                                                                                                                                     2 MAX
                                                      (0.15) TYP                         0.25
                                SEE DETAIL A                                      GAGE PLANE




                                                                                                        0.95                          0.05 MIN
                                                                                     0 -8               0.55

                                                                                                                 DETAIL A
                                                                                                                       A 15




                                                                                                                   TYPICAL

                                                                                                                              4214851/B 08/2019

NOTES:

1. All linear dimensions are in millimeters. Any dimensions in parenthesis are for reference only. Dimensioning and tolerancing
   per ASME Y14.5M.
2. This drawing is subject to change without notice.
3. This dimension does not include mold flash, protrusions, or gate burrs. Mold flash, protrusions, or gate burrs shall not
   exceed 0.15 mm per side.
4. This dimension does not include interlead flash. Interlead flash shall not exceed 0.25 mm per side.
5. Reference JEDEC registration MO-150.




                                                                              www.ti.com
```

## Page 27

```text
                                                                                   EXAMPLE BOARD LAYOUT
DB0020A                                                                                     SSOP - 2 mm max height
                                                                                                          SMALL OUTLINE PACKAGE




                                        20X (1.85)                    SYMM

                                  1                                                                        (R0.05) TYP

                      20X (0.45)                                                                     20




                                                                                                          SYMM
                     18X (0.65)




                                  10                                                                 11


                                                                       (7)


                                                       LAND PATTERN EXAMPLE
                                                         EXPOSED METAL SHOWN
                                                              SCALE: 10X




              SOLDER MASK                                                     METAL UNDER                 SOLDER MASK
                                                     METAL
                  OPENING                                                     SOLDER MASK                 OPENING


      EXPOSED METAL                                                                                              EXPOSED METAL

                                       0.07 MAX                                             0.07 MIN
                                       ALL AROUND                                           ALL AROUND

                           NON-SOLDER MASK                                                  SOLDER MASK
                               DEFINED                                                        DEFINED
                             (PREFERRED)
                                                         SOLDER MASK DETAILS
                                                             15.000




                                                                                                                 4214851/B 08/2019
NOTES: (continued)

6. Publication IPC-7351 may have alternate designs.
7. Solder mask tolerances between and around signal pads can vary based on board fabrication site.




                                                                      www.ti.com
```

## Page 28

```text
                                                                               EXAMPLE STENCIL DESIGN
DB0020A                                                                                      SSOP - 2 mm max height
                                                                                                           SMALL OUTLINE PACKAGE




                                       20X (1.85)               SYMM
                                                                                                            (R0.05) TYP
                                  1
                      20X (0.45)                                                                      20




                                                                                                        SYMM
                     18X (0.65)




                                  10                                                                  11



                                                                  (7)



                                                     SOLDER PASTE EXAMPLE
                                                    BASED ON 0.125 mm THICK STENCIL
                                                              SCALE: 10X




                                                                                                                  4214851/B 08/2019
NOTES: (continued)

8. Laser cutting apertures with trapezoidal walls and rounded corners may offer better paste release. IPC-7525 may have alternate
   design recommendations.
9. Board assembly site may have different recommendations for stencil design.




                                                                 www.ti.com
```

## Page 29

```text

```

## Page 30

```text

```

## Page 31

```text
                                                                  GENERIC PACKAGE VIEW
RGY 20                                                                     VQFN - 1 mm max height
3.5 x 4.5, 0.5 mm pitch                                                   PLASTIC QUAD FGLATPACK - NO LEAD




               This image is a representation of the package family, actual package may vary.
                             Refer to the product data sheet for package details.




                                                                                                  4225264/A




                                                    www.ti.com
```

## Page 32

```text
                                                                  GENERIC PACKAGE VIEW
FK 20                                                                  LCCC - 2.03 mm max height
8.89 x 8.89, 1.27 mm pitch                                                   LEADLESS CERAMIC CHIP CARRIER




               This image is a representation of the package family, actual package may vary.
                             Refer to the product data sheet for package details.




                                                                                                  4229370\/A\




                                                    www.ti.com
```

## Page 33

```text
                                                                                                           PACKAGE OUTLINE
DW0020A                                                         SCALE 1.200
                                                                                                       SOIC - 2.65 mm max height
                                                                                                                                          SOIC



                                                                                                                           C

                                    10.63                                                                  SEATING PLANE
                                          TYP
                                    9.97
                                           PIN 1 ID                                                                  0.1 C
         A
                                           AREA
                                                                                     18X 1.27
                                                                              20
               1




       13.0                                                                          2X
       12.6                                                                         11.43
      NOTE 3




               10
                                                               11
                                                                                         0.51
                                                                                   20X
                                       7.6                                               0.31                2.65 MAX
                    B                                                                     0.25     C A B
                                       7.4
                                      NOTE 4




                                                                                    0.33
                                                                                         TYP
                                                                                    0.10


                                                                                           0.25
                                 SEE DETAIL A                                       GAGE PLANE



                                                                                                                        1.27              0.3
                                                                                            0 -8                        0.40              0.1

                                                                                                                        DETAIL A
                                                                                                                          TYPICAL


                                                                                                                               4220724/A 05/2016

NOTES:

1. All linear dimensions are in millimeters. Dimensions in parenthesis are for reference only. Dimensioning and tolerancing
   per ASME Y14.5M.
2. This drawing is subject to change without notice.
3. This dimension does not include mold flash, protrusions, or gate burrs. Mold flash, protrusions, or gate burrs shall not
   exceed 0.15 mm per side.
4. This dimension does not include interlead flash. Interlead flash shall not exceed 0.43 mm per side.
5. Reference JEDEC registration MS-013.




                                                                              www.ti.com
```

## Page 34

```text
                                                                               EXAMPLE BOARD LAYOUT
DW0020A                                                                                 SOIC - 2.65 mm max height
                                                                                                                           SOIC




                               20X (2)                           SYMM

                                           1
                                                                                              20

                          20X (0.6)



                             18X (1.27)



                                                                                                     SYMM




                            (R0.05)
                            TYP




                                          10                                                  11


                                                                 (9.3)


                                                    LAND PATTERN EXAMPLE
                                                               SCALE:6X




                SOLDER MASK                                         METAL UNDER                             SOLDER MASK
                                                   METAL                                                    OPENING
                OPENING                                             SOLDER MASK




                                      0.07 MAX                                           0.07 MIN
                                      ALL AROUND                                         ALL AROUND

                              NON SOLDER MASK                                            SOLDER MASK
                                  DEFINED                                                  DEFINED

                                                         SOLDER MASK DETAILS
                                                                                                                4220724/A 05/2016
NOTES: (continued)

6. Publication IPC-7351 may have alternate designs.
7. Solder mask tolerances between and around signal pads can vary based on board fabrication site.




                                                                www.ti.com
```

## Page 35

```text
                                                                               EXAMPLE STENCIL DESIGN
DW0020A                                                                                   SOIC - 2.65 mm max height
                                                                                                                                SOIC




                                 20X (2)
                                                                  SYMM
                                            1
                                                                                               20

                           20X (0.6)



                              18X (1.27)



                                                                                                    SYMM




                                           10                                                  11

                                                                   (9.3)



                                                     SOLDER PASTE EXAMPLE
                                                   BASED ON 0.125 mm THICK STENCIL
                                                              SCALE:6X




                                                                                                                  4220724/A 05/2016
NOTES: (continued)

8. Laser cutting apertures with trapezoidal walls and rounded corners may offer better paste release. IPC-7525 may have alternate
   design recommendations.
9. Board assembly site may have different recommendations for stencil design.




                                                                 www.ti.com
```

## Page 36

```text

```

## Page 37

```text
                                                                                                            PACKAGE OUTLINE
PW0020A                                                        SCALE 2.500
                                                                                                     TSSOP - 1.2 mm max height
                                                                                                                SMALL OUTLINE PACKAGE




                                                                                                                                SEATING
                                       6.6                                                                       C
                                           TYP                                                                                  PLANE
          A                            6.2
                                                                                                                                 0.1 C
                                          PIN 1 INDEX AREA
                                                                                      18X 0.65
                                                                              20
                1




                                                                                      2X
        6.6                                                                           5.85
        6.4
       NOTE 3




                10
                                                                              11
                                                                                             0.30
                                                                                      20X
                                        4.5                                                  0.19               1.2 MAX
                     B
                                        4.3
                                       NOTE 4                                             0.1       C A B




                                                          (0.15) TYP
                                     SEE DETAIL A


                                                                                    0.25
                                                                             GAGE PLANE                                          0.15
                                                                                                                                 0.05



                                                                                                       0.75
                                                                                                       0.50
                                                                                      0 -8
                                                                                                               DETAIL A
                                                                                                                  A 20




                                                                                                                TYPICAL

                                                                                                                          4220206/A 02/2017

NOTES:

1. All linear dimensions are in millimeters. Any dimensions in parenthesis are for reference only. Dimensioning and tolerancing
   per ASME Y14.5M.
2. This drawing is subject to change without notice.
3. This dimension does not include mold flash, protrusions, or gate burrs. Mold flash, protrusions, or gate burrs shall not
   exceed 0.15 mm per side.
4. This dimension does not include interlead flash. Interlead flash shall not exceed 0.25 mm per side.
5. Reference JEDEC registration MO-153.




                                                                             www.ti.com
```

## Page 38

```text
                                                                                     EXAMPLE BOARD LAYOUT
PW0020A                                                                                   TSSOP - 1.2 mm max height
                                                                                                          SMALL OUTLINE PACKAGE




                                            20X (1.5)                   SYMM
                                                                                                       (R0.05) TYP
                                       1
                           20X (0.45)                                                             20




                                                                                                       SYMM
                          18X (0.65)




                                       10                                                         11



                                                                        (5.8)


                                                        LAND PATTERN EXAMPLE
                                                          EXPOSED METAL SHOWN
                                                               SCALE: 10X




               SOLDER MASK                                                      METAL UNDER              SOLDER MASK
                                                  METAL                         SOLDER MASK              OPENING
                   OPENING


        EXPOSED METAL                                                                                          EXPOSED METAL

                                   0.05 MAX                                                     0.05 MIN
                                   ALL AROUND                                                   ALL AROUND

                            NON-SOLDER MASK                                                   SOLDER MASK
                                DEFINED                                                         DEFINED
                              (PREFERRED)                SOLDER MASK DETAILS
                                                               15.000




                                                                                                                     4220206/A 02/2017
NOTES: (continued)

6. Publication IPC-7351 may have alternate designs.
7. Solder mask tolerances between and around signal pads can vary based on board fabrication site.




                                                                        www.ti.com
```

## Page 39

```text
                                                                               EXAMPLE STENCIL DESIGN
PW0020A                                                                                 TSSOP - 1.2 mm max height
                                                                                                         SMALL OUTLINE PACKAGE




                                            20X (1.5)           SYMM
                                                                                                     (R0.05) TYP
                                       1
                           20X (0.45)                                                           20




                                                                                                  SYMM
                          18X (0.65)




                                       10                                                       11



                                                                 (5.8)



                                                        SOLDER PASTE EXAMPLE
                                                    BASED ON 0.125 mm THICK STENCIL
                                                              SCALE: 10X




                                                                                                                   4220206/A 02/2017
NOTES: (continued)

8. Laser cutting apertures with trapezoidal walls and rounded corners may offer better paste release. IPC-7525 may have alternate
   design recommendations.
9. Board assembly site may have different recommendations for stencil design.




                                                                 www.ti.com
```

## Page 40

```text
                                                                                                PACKAGE OUTLINE
DGS0020A                                                                                  VSSOP - 1.1 mm max height
                                                                                                             SMALL OUTLINE PACKAGE




             PIN 1 INDEX
                    AREA                                                                                 C
                                                                                                                               SEATING
                                          5.1
                   A                          TYP                                                    0.1 C                     PLANE
                                          4.7
                                                                            18X 0.5
                          1                                       20




                 5.2
                                                                          2X 4.5
                 5.0
                NOTE 3


                                                                                           4X (0 -15 )


                         10
                                                                  11
                                                                                 0.275
                                                                           20X
                                             3.1                                 0.165
                           B
                                             2.9                                 0.1   C A B




     SEE DETAIL A                                           4X (7 -15 )


                                                                           (0.15) TYP




                                                                                 0.25
                                                                          GAGE PLANE                                             1.1 MAX




                                                                                                           0.7                     0.15
                                                                              0 -8                         0.4                     0.05
                                                                                                             DETAIL A
                                                                                                                   A 20




                                                                                                                 TYPICAL


                                                                                                                          4226367/A 10/2020
                                                                                          PowerPAD is a trademark of Texas Instruments.
NOTES:

1. All linear dimensions are in millimeters. Any dimensions in parenthesis are for reference only. Dimensioning and tolerancing
   per ASME Y14.5M.
2. This drawing is subject to change without notice.
3. This dimension does not include mold flash, protrusions, or gate burrs. Mold flash, protrusions, or gate burrs shall not
   exceed 0.15 mm per side.
4. No JEDEC registration as of September 2020.
5. Features may differ or may not be present.




                                                                  www.ti.com
```

## Page 41

```text
                                                                                     EXAMPLE BOARD LAYOUT
DGS0020A                                                                                      VSSOP - 1.1 mm max height
                                                                                                            SMALL OUTLINE PACKAGE




                  20X (1.45)                                            SYMM


                                1                                                                         20

               20X (0.3)

             (R0.05) TYP



                18X (0.5)

                                                                                                            SYMM




                               10                                                                         11



                                                                        (4.4)
                                                    LAND PATTERN EXAMPLE
                                                                    SCALE: 16X




                SOLDER MASK                        METAL                        METAL UNDER                 SOLDER MASK
                    OPENING                                                     SOLDER MASK                 OPENING




                 0.05 MAX                             EXPOSED METAL
                                                                                0.05 MIN                          EXPOSED METAL
             ALL AROUND                                                     ALL AROUND
                               NON-SOLDER MASK                                                SOLDER MASK
                                   DEFINED                                                      DEFINED
                                 (PREFERRED)
                                                       SOLDER MASK DETAILS
                                                               15.000




                                                                                                                     4226367/A 10/2020
NOTES: (continued)

 6. Publication IPC-7351 may have alternate designs.
 7. Solder mask tolerances between and around signal pads can vary based on board fabrication site.
 8. This package is designed to be soldered to a thermal pad on the board. For more information, see Texas Instruments literature
    numbers SLMA002 (www.ti.com/lit/slma002) and SLMA004 (www.ti.com/lit/slma004).
 9. Size of metal pad may vary due to creepage requirement.
10. Vias are optional depending on application, refer to device data sheet. It is recommended that vias under paste be filled, plugged
    or tented.




                                                                        www.ti.com
```

## Page 42

```text
                                                                              EXAMPLE STENCIL DESIGN
DGS0020A                                                                                VSSOP - 1.1 mm max height
                                                                                                         SMALL OUTLINE PACKAGE




                 20X (1.45)                                     SYMM
               20X (0.3)

                              1                                                                        20




            (R0.05) TYP




                                                                                                         SYMM

              (18X 0.5)




                              10                                                                       11


                                                                 (4.4)
                                                   SOLDER PASTE EXAMPLE
                                                 BASED ON 0.125 mm THICK STENCIL
                                                           SCALE: 16X




                                                                                                                  4226367/A 10/2020
NOTES: (continued)

11. Laser cutting apertures with trapezoidal walls and rounded corners may offer better paste release. IPC-7525 may have alternate
    design recommendations.
12. Board assembly site may have different recommendations for stencil design.




                                                                 www.ti.com
```

## Page 43

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

                                                Copyright © 2026, Texas Instruments Incorporated
                                                                Last updated 10/2025
```
