# AOC97

Original PDF: [AOC97.pdf](AOC97.pdf)

SHA-256: `97f368720dee39bca256cb51d27f5907faeb42621a06fdf04652baa5b84f8772`

Source: https://abracon.com/datasheets/AOC97.pdf

Parts: AOC97FAJC-10.0000

GPS calibrator references: Y1

Machine-extracted text; consult the original PDF for drawings, symbols and table alignment.

## Page 1

```text
AOC97 series
HIGH-STABILITY SMD OCXO

Description
The AOC97 series is an Oven Controlled Crystal Oscillator (OCXO) offered in a 9.7mm x 7.5mm x
3.9mm four-pad SMD package. Tight frequency stability of ±10ppb over an extended operating
temperature range of -40°C to +95°C is achieved using an SC-Cut, High “Q” resonator-based
design. This series offers a CMOS-compatible output with a 3.3Vdc +/-5% supply voltage, common
for most communication infrastructure, base station, and test and measurement equipment
applications. The AOC97 series offers industry standard frequencies in the range of 10MHz to
48MHz with low long-term aging and excellent phase noise.

Features                                                                    Typical Applications
 ▪    SC-Cut, High “Q” resonator-based design                               ▪         Cellular infrastructure; Base stations
 ▪    3.3Vdc supply voltage                                                 ▪         Test & measurement equipment
 ▪    CMOS compatible output logic                                          ▪         Switches & routers
 ▪    9.7mm x 7.5mm x 3.9mm four pad SMD package                            ▪         Time & frequency references
 ▪    Stability over temperature: ±10ppb over -40°C to                      ▪         Precision GPS
      +95°C                                                                 ▪         Satellite Timing and Frequency
 ▪    Low long-term aging: ±500ppb over first year                          ▪         High End Synthesizers
 ▪    Industry standard frequencies available                               ▪         Oil and Gas Exploration
 ▪    Excellent phase noise

Electrical Specifications [Note 1]
 ▪
 Parameters                                          Min.         Typ.      Max.            Units                        Notes
 Frequency Range                                      10                     48             MHz
                                                                                                      Contact Abracon for non-standard
 Standard Available Frequencies                      10,19.2,20,30.72, 38.88,48              MHz
                                                                                                      frequencies
 Supply Voltage (Vdd)                               3.135          3.3      3.456              V
 Input Power (warm-up)                                                       2.1              W
 Input Power (steady-state)                                                  0.8              W
 Operating Temperature Range                         -40                     +95              °C
 Storage Temperature Range                           -55                    +105              °C
 Initial Frequency Tolerance [Note 2]                                        ±1              ppm
 Frequency Stability over Operating Temperature
                                                                            ±10              ppb
 Range [Note 3]
 Temperature Slope [Note 4]                                                  ±1             ppb
 Stability vs. Supply Voltage                                                ±5             ppb       Vdd varied from 3.135V to 3.465V
 Stability vs. Load                                                          ±5             ppb       5% load change
 Aging per Day                                                               ±3             ppb       after 30 days of operation
 Aging per Year                                                             ±500            ppb       after 30 days of operation
 Warm-up Time [Note 5]                                                        3            minutes
 Start-up Time [Note 6]                                                      50              ms
 Output Waveform
 High-level Output Voltage (VOH)                         2.4                                  V
 Low-level Output Voltage (VOL)                                                 0.4           V
 Output Signal                                                   CMOS
 Output Load                                                      15                         pF
 Rise and Fall Time (tr, tf)                                                     6           ns       10% to 90% of waveform
 Duty Cycle                                              45                     55           %        @50% of waveform




                                                                                                                  lign




Revision: A                                                    Disclaimer                                         lign     Check Inventory
Initial Release 9/1/2026                                                                                                  Request Samples

                                                                Page 1
```

## Page 2

```text
AOC97 series
HIGH-STABILITY SMD OCXO



 Electrical Specifications continued [Note 1]


 Parameters                                                          Min.           Typ.         Max.         Units                        Notes
                                                                                     -80          -70                   1Hz offset
                                                                                    -115         -110                   10Hz offset
                                                                                    -146         -138                   100Hz offset
 Phase Noise (@ 10.0000MHz)                                                         -157         -151        dBc/Hz     1kHz offset
                                                                                    -161         -156                   10kHz offset
                                                                                    -164         -159                   100kHz offset
                                                                                    -165         -161                   1MHz offset
                                                                                     -80          -70                   1Hz offset
                                                                                    -115         -110                   10Hz offset
                                                                                    -146         -138                   100Hz offset
 Phase Noise (@ 19.2000MHz)                                                         -160         -154        dBc/Hz     1kHz offset
                                                                                    -164         -159                   10kHz offset
                                                                                    -164         -160                   100kHz offset
                                                                                    -165         -161                   1MHz offset
                                                                                     -75          -65                   1Hz offset
                                                                                    -113         -108                   10Hz offset
                                                                                    -146         -138                   100Hz offset
 Phase Noise (@ 20.0000MHz)                                                         -160         -154        dBc/Hz     1kHz offset
                                                                                    -163         -158                   10kHz offset
                                                                                    -163         -158                   100kHz offset
                                                                                    -163         -158                   1MHz offset
                                                                                     -73          -63                   1Hz offset
                                                                                    -110         -103                   10Hz offset
                                                                                    -140         -130                   100Hz offset
 Phase Noise (@30.7200MHz)                                                          -158         -152        dBc/Hz     1kHz offset
                                                                                    -165         -160                   10kHz offset
                                                                                    -165         -160                   100kHz offset
                                                                                    -165         -160                   1MHz offset
                                                                                     -67          -57                   1Hz offset
                                                                                    -105          -97                   10Hz offset
                                                                                    -135         -125                   100Hz offset
 Phase Noise (@ 38.8800MHz)                                                         -156         -151        dBc/Hz     1kHz offset
                                                                                    -165         -160                   10kHz offset
                                                                                    -165         -160                   100kHz offset
                                                                                    -165         -160                   1MHz offset
                                                                                     -60          -50                   1Hz offset
                                                                                     -99          -90                   10Hz offset
                                                                                    -130         -120                   100Hz offset
 Phase Noise (@ 48.0000MHz)                                                         -155         -150        dBc/Hz     1kHz offset
                                                                                    -165         -160                   10kHz offset
                                                                                    -165         -160                   100kHz offset
                                                                                    -165         -160                   1MHz offset

 Note 1: All measurements guaranteed at +25°C, Vdd = 3.3V, CL =15pf unless otherwise specified.
 Note 2: Measured at +25°C, Vdd=3.3V within 30 days, at time of shipment.
 Note 3: Varied from -40 to +95°C, @ fref =(fmax +fmin )/2, Vdd=3.3V, CL=15pf, less than 2°C per minute
 Note 4: Temperature slope ±1°C/min with any temperature window over -40 to +95°C
 Note 5: Time until RF output is within ± 0.1 ppm referenced to last frequency reading 1 hour after startup T A=25°C.
 Note 6: Time until RF output waveform is within output logic levels, duty cycle and rise/fall time specifications.




                                                                                                                                    lign




Revision: A                                                                    Disclaimer                                           lign     Check Inventory
Initial Release 9/1/2026                                                                                                                    Request Samples

                                                                                 Page 2
```

## Page 3

```text
   AOC97 series
   HIGH-STABILITY SMD OCXO



     Environmental and Mechanical

                              Parameters                                        Description
                              MSL                     3
                              REACH/RoHS II           Compliant
                              ESD                     Sensitive




     Part Identification


                    AOC97                                                        -
                                                                                                                          (6): Packaging
                                                                                                                            Blank = Bulk
                                                                                                                     T = Tape & Reel (1k/reel)
   (1): Type                                  (3): Stability over OTR
F: Fixed Clock                            J: ±10ppb over -40°C to +95°C



                                                                                                  (5): Output
                                                                             (4): RF Output    Frequency in MHz
                                                                                C: CMOS         Please specify the
                                                                                                    frequency in
                          (2): Vdd
                                                                                                    units of MHz
                           A: 3.3V
                                                                                              out to 4-digit accuracy
                                                                                                after the decimal.
                                                                                                      Example:
                                                                                               “20.0000” = 20MHz




      Part Number Example:
      AOC97FAJC-20.0000T
                                                                                                              lign




   Revision: A                                                    Disclaimer                                  lign      Check Inventory
   Initial Release 9/1/2026                                                                                            Request Samples

                                                                    Page 3
```

## Page 4

```text
AOC97 series
HIGH-STABILITY SMD OCXO


 Mechanical Dimensions (10 MHz, 19.2 MHz, 30.72 MHz, 38.88 MHz)




                                                            Pin #         Function
                                                              1     Do Not Connect
                                                              2     Ground
                                                              3     Output
                                                              4     Supply Voltage (Vdd)




         Dimensions: inches [mm]
         Tolerance ±0.3mm without mark
                                                                               lign




Revision: A                                 Disclaimer                         lign    Check Inventory
Initial Release 9/1/2026                                                              Request Samples

                                             Page 4
```

## Page 5

```text
AOC97 series
HIGH-STABILITY SMD OCXO


 Mechanical Dimensions (20 MHz, 48 MHz)




                                                       Pin #         Function
                                                         1     Do Not Connect
                                                         2     Ground
                                                         3     Output
                                                         4     Supply Voltage (Vdd)




         Dimensions: inches [mm]
         Tolerance ±0.3mm without mark
                                                                                lign




Revision: A                               Disclaimer                            lign    Check Inventory
Initial Release 9/1/2026                                                               Request Samples

                                           Page 5
```

## Page 6

```text
AOC97 series
HIGH-STABILITY SMD OCXO


 Reflow Profile [JEDEC J-STD-020]




                                                                                                                         Table 1
                                                                                                                         SnPb Eutectic Process
                                                                                                                         Classification Temperatures (Tc)
                                                                                                                           Package      Volume mm3               Volume mm3
                                                                                                                          Thickness         <350                     >350
                                                                                                                           <2.5 mm           235 °C                 220 °C
                                                                                                                           >2.5 mm           220 °C                 220 °C
                                                                                                                  Table 2
                                                                                                                  Pb-Free Process
                                                                                                                  Classification Temperatures (Tc)
                                                                                                                        Package       Volume mm3         Volume mm3          Volume mm3
                                                                                                                       Thickness          <350            350-2000              >2000
                                                                                                                       <1.6 mm          260 °C                 260 °C          260 °C
                                                                                                                  1.6 mm - 2.5 mm       260 °C                 250 °C          245 °C
                                                                                                                       >2.5 mm          250 °C                 245 °C          245 °C




                                                                                                                           Sn-Pb Eutectic               Pb-Free
                  Profile Feature
                                                                                                                             Assembly                  Assembly
                  Preheat / soak
                    Temperature minimum (Tsmin)                                                                                 100°C                    150°C
                    Temperature maximum (Tsmax)                                                                                 150°C                    200°C
                    Time (Tsmin to Tsmax) (ts)                                                                               60 - 120 sec.            60 - 120 sec.
                  Average ramp-up rate (Tsmax to TP)                                                                         3°C/sec. max             3°C/sec. max
                  Liquidous temperature (TL)                                                                                    183°C                    217°C
                  Time at liquidous (tL)                                                                                     60 - 150 sec.            60 - 150 sec.
                  Peak package body temperature (TP)*                                                                         see Table 1              see Table 2
                  Time (tp)** within 5°C of the specified classification temperature (TC)                                       20 sec.                  30 sec.
                  Ramp-down rate (Tp to Tsmax)                                                                               6°C/sec. max             6°C/sec. max
                  Time 25°C to peak temperature                                                                               6 min. max               8 min. max
                  Reflow cycles                                                                                                 2 max                    2 max
                  *Tolerance for peak profile temperature (T P) is defined as a supplier minimum and a user maximum.
                  **Tolerance for time at peak profile temperature (tp) is defined as supplier minimum and a user maximum.




                                                                                                                                                        lign




Revision: A                                                                         Disclaimer                                                          lign       Check Inventory
Initial Release 9/1/2026                                                                                                                                          Request Samples

                                                                                       Page 6
```

## Page 7

```text
AOC97 series
HIGH-STABILITY SMD OCXO

 Packaging
   T = 1000 pcs/reel




                                                  Tape Specifications (mm)
                 Width        Ao         Bo          Do          D1 (Min)      E1         F               Ko
                 16mm          *          *      1.5+0.1/-0.0       1.50   1.75±0.1    7.125               *
                 Width        P1          P2          P0          T (Max)  T1 (Max)   T2 (Max)          W (Max)
                 16mm      12.0±0.1    2.0±0.1     4.0±0.1           0.3      0.1        8.0             16.0
               *Note: Compliant to EIA-481




                                                                                                 lign




Revision: A                                             Disclaimer                               lign     Check Inventory
Initial Release 9/1/2026                                                                                 Request Samples

                                                          Page 7
```

## Page 8

```text
AOC97 series
HIGH-STABILITY SMD OCXO




                                                  Reel Specifications (mm)
                Width      Qty/Reel      A         B             C           D         N           *W1
                16mm        1000      330±1.0   2.5±0.3      13.0±0.2      22±0.6   99.5±0.5   16.8+1.0/-0.2
                *Note: Measured at Hub




                                                                                                 lign




Revision: A                                              Disclaimer                              lign    Check Inventory
Initial Release 9/1/2026                                                                                Request Samples

                                                          Page 8
```
