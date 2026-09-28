# HUSB238-registers

Original PDF: [HUSB238-registers.pdf](HUSB238-registers.pdf)

SHA-256: `6d034fc83971f89558e091929567e6bbfa11bd93bd443cd94ce0a831a6fd4e4a`

Source: https://www.hynetek.com/uploadfiles/site/219/news/c3afa59e-1c03-4b92-8525-873c152bae4b.pdf

Parts: HUSB238_002DD

GPS calibrator references: U11

Machine-extracted text; consult the original PDF for drawings, symbols and table alignment.

## Page 1

```text
HUSB238

REGISTER INFORMATION

REV. 1.1
Date: 01/14/2021




©2021 Hynetek Semiconductor Co., Ltd. All rights reserved.   www.hynetek.com
```

## Page 2

```text
  HUSB238                                                                                                                    Register Information

CONTENTS
Contents ........................................................................................................................................................................... 2
Registers .......................................................................................................................................................................... 3
   PD_STATUS0 ............................................................................................................................................................... 3
   PD_STATUS1 ............................................................................................................................................................... 4
   SRC_PDO_5V .............................................................................................................................................................. 4
   SRC_PDO_9V .............................................................................................................................................................. 5
   SRC_PDO_12V ............................................................................................................................................................ 5
   SRC_PDO_15V ............................................................................................................................................................ 6
   SRC_PDO_18V ............................................................................................................................................................ 6
   SRC_PDO_20V ............................................................................................................................................................ 7
   SRC_PDO ..................................................................................................................................................................... 7
   GO_COMMAND ........................................................................................................................................................... 7
Important Notice ............................................................................................................................................................... 8




 ©2021 Hynetek Semiconductor Co., Ltd. All rights reserved.                                                                                                           Page 2 of 8
```

## Page 3

```text
 Register Information                                                                                               HUSB238

REGISTERS
The HUSB238 has registers to store source capabilities, PD status and configure functions. The registers are
accessed by I2C interface through SDA and SCL pins. The I2C slave address of the HUSB238 is 0x08.
Table 1 is the summary of the registers.
Table 1. Register Summary
 Address        Register Name                                                                                        Default
 0x00               PD_STATUS0                                                                                       0x00
 0x01               PD_STATUS1                                                                                       0x00
 0x02               SRC_PDO_5V                                                                                       0x00
 0x03               SRC_PDO_9V                                                                                       0x00
 0x04               SRC_PDO_12V                                                                                      0x00
 0x05               SRC_PDO_15V                                                                                      0x00
 0x06               SRC_PDO_18V                                                                                      0x00
 0x07               SRC_PDO_20V                                                                                      0x00
 0x08               SRC_PDO                                                                                          0x00
 0x09               GO_COMMAND                                                                                       0x00


PD_STATUS0
Table 2. PD_STATUS0 (0x00)
 Bits    Field Name                       Type        Description                                                           Reset
 [7:4]    PD_SRC_VOLTAGE                  R           The voltage information when an explicit contract is established.     0000
                                                      0000 = Unattached
                                                      0001 = PD 5V
                                                      0010 = PD 9V
                                                      0011 = PD 12V
                                                      0100 = PD 15V
                                                      0101 = PD 18V
                                                      0110 = PD 20V
                                                      Others = Reserved
 [3:0]    PD_SRC_CURRENT                  R           The current information when an explicit contract is established.     0000
                                                      0000 = 0.5A
                                                      0001 = 0.7A
                                                      0010 = 1A
                                                      0011 = 1.25A
                                                      0100 = 1.5A
                                                      0101 = 1.75A
                                                      0110 = 2A
                                                      0111 = 2.25A
                                                      1000 = 2.5A
                                                      1001 = 2.75A
                                                      1010 = 3A
                                                      1011 = 3.25A
                                                      1100 = 3.5A
                                                      1101 = 4A
                                                      1110 = 4.5A
                                                      1111 = 5A




 ©2021 Hynetek Semiconductor Co., Ltd. All rights reserved.                                                                   Page 3 of 8
```

## Page 4

```text
 HUSB238                                                                                     Register Information
PD_STATUS1
Table 3. PD_STATUS1 (0x01)
 Bits    Field Name                       Type        Description                                                    Reset
 7        CC_DIR                          R           0 = CC1 is connected to CC line or unattached mode             0
                                                      1 = CC2 is connected to CC line
 6        ATTACH                          R           0 = HUSB238 is in unattached mode                              0
                                                      1 = HUSB238 is in modes other than unattached mode
 [5:3]    PD_RESPONSE                     R           000 = No response                                              000
                                                      001 = Success
                                                      011 = Invalid command or argument
                                                      100 = Command not supported
                                                      101 = Transaction fail. No GoodCRC is received after sending
                                                      Others = Reserved
 2        5V_VOLTAGE                      R           Voltage information of 5V contract                             0
                                                      0 = Others
                                                      1 = 5V
 [1:0]    5V_CURRENT                      R           Current information of 5V contract                             00
                                                      00 = Default current
                                                      01 = 1.5A
                                                      10 = 2.4A
                                                      11 = 3A


SRC_PDO_5V
Table 4. SRC_PDO_5V (0x02)
 Bits    Field Name                       Type        Description                                                    Reset
 7        SRC_5V_DETECT                   R           0 = Not detected                                               0
                                                      1 = Detected
 [6:4]    RESERVED                        R           Reserved                                                       000
 [3:0]    SRC_5V_CURRENT                  R           0000 = 0.5A                                                    0000
                                                      0001 = 0.7A
                                                      0010 = 1A
                                                      0011 = 1.25A
                                                      0100 = 1.5A
                                                      0101 = 1.75A
                                                      0110 = 2A
                                                      0111 = 2.25A
                                                      1000 = 2.50A
                                                      1001 = 2.75A
                                                      1010 = 3A
                                                      1011 = 3.25A
                                                      1100 = 3.5A
                                                      1101 = 4A
                                                      1110 = 4.5A
                                                      1111 = 5A




 ©2021 Hynetek Semiconductor Co., Ltd. All rights reserved.                                                               Page 4 of 8
```

## Page 5

```text
Register Information                                                     HUSB238
SRC_PDO_9V
Table 5. SRC_PDO_9V (0x03)
 Bits    Field Name                       Type        Description          Reset
 7        SRC_9V_DETECT                   R           0 = Not detected     0
                                                      1 = Detected
 [6:4]    RESERVED                        R           Reserved             000
 [3:0]    SRC_9V_CURRENT                  R           0000 = 0.5A          0000
                                                      0001 = 0.7A
                                                      0010 = 1A
                                                      0011 = 1.25A
                                                      0100 = 1.5A
                                                      0101 = 1.75A
                                                      0110 = 2A
                                                      0111 = 2.25A
                                                      1000 = 2.50A
                                                      1001 = 2.75A
                                                      1010 = 3A
                                                      1011 = 3.25A
                                                      1100 = 3.5A
                                                      1101 = 4A
                                                      1110 = 4.5A
                                                      1111 = 5A


SRC_PDO_12V
Table 6. SRC_PDO_12V (0x04)
 Bits    Field Name                       Type        Description          Reset
 7        SRC_12V_DETECT                  R           0 = Not detected     0
                                                      1 = Detected
 [6:4]    RESERVED                        R           Reserved             000
 [3:0]    SRC_12V_CURRENT                 R           0000 = 0.5A          0000
                                                      0001 = 0.7A
                                                      0010 = 1A
                                                      0011 = 1.25A
                                                      0100 = 1.5A
                                                      0101 = 1.75A
                                                      0110 = 2A
                                                      0111 = 2.25A
                                                      1000 = 2.50A
                                                      1001 = 2.75A
                                                      1010 = 3A
                                                      1011 = 3.25A
                                                      1100 = 3.5A
                                                      1101 = 4A
                                                      1110 = 4.5A
                                                      1111 = 5A




 ©2021 Hynetek Semiconductor Co., Ltd. All rights reserved.                    Page 5 of 8
```

## Page 6

```text
 HUSB238                                                                 Register Information
SRC_PDO_15V
Table 7. SRC_PDO_15V (0x05)
 Bits    Field Name                       Type        Description                     Reset
 7        SRC_15V_DETECT                  R           0 = Not detected                0
                                                      1 = Detected
 [6:4]    RESERVED                        R           Reserved                        000
 [3:0]    SRC_15V_CURRENT                 R           0000 = 0.5A                     0000
                                                      0001 = 0.7A
                                                      0010 = 1A
                                                      0011 = 1.25A
                                                      0100 = 1.5A
                                                      0101 = 1.75A
                                                      0110 = 2A
                                                      0111 = 2.25A
                                                      1000 = 2.50A
                                                      1001 = 2.75A
                                                      1010 = 3A
                                                      1011 = 3.25A
                                                      1100 = 3.5A
                                                      1101 = 4A
                                                      1110 = 4.5A
                                                      1111 = 5A


SRC_PDO_18V
Table 8. SRC_PDO_18V (0x06)
 Bits    Field Name                       Type        Description                     Reset
 7        SRC_18V_DETECT                  R           0 = Not detected                0
                                                      1 = Detected
 [6:4]    RESERVED                        R           Reserved                        000
 [3:0]    SRC_18V_CURRENT                 R           0000 = 0.5A                     0000
                                                      0001 = 0.7A
                                                      0010 = 1A
                                                      0011 = 1.25A
                                                      0100 = 1.5A
                                                      0101 = 1.75A
                                                      0110 = 2A
                                                      0111 = 2.25A
                                                      1000 = 2.50A
                                                      1001 = 2.75A
                                                      1010 = 3A
                                                      1011 = 3.25A
                                                      1100 = 3.5A
                                                      1101 = 4A
                                                      1110 = 4.5A
                                                      1111 = 5A




 ©2021 Hynetek Semiconductor Co., Ltd. All rights reserved.                               Page 6 of 8
```

## Page 7

```text
Register Information                                                                               HUSB238
SRC_PDO_20V
Table 9. SRC_PDO_20V (0x07)
 Bits    Field Name                       Type        Description                                    Reset
 7        SRC_20V_DETECT                  R           0 = Not detected                               0
                                                      1 = Detected
 [6:4]    RESERVED                        R           Reserved                                       000
 [3:0]    SRC_20V_CURRENT                 R           0000 = 0.5A                                    0000
                                                      0001 = 0.7A
                                                      0010 = 1A
                                                      0011 = 1.25A
                                                      0100 = 1.5A
                                                      0101 = 1.75A
                                                      0110 = 2A
                                                      0111 = 2.25A
                                                      1000 = 2.50A
                                                      1001 = 2.75A
                                                      1010 = 3A
                                                      1011 = 3.25A
                                                      1100 = 3.5A
                                                      1101 = 4A
                                                      1110 = 4.5A
                                                      1111 = 5A


SRC_PDO
Table 10. SRC_PDO (0x08)
 Bits   Field Name                        Type        Description                                    Reset
 [7:4]    PDO_SELECT                      RW          0000 = Not selected                            0000
                                                      0001 = SRC_PDO_5V
                                                      0010 = SRC_PDO_9V
                                                      0011 = SRC_PDO_12V
                                                      1000 = SRC_PDO_15V
                                                      1001 = SRC_PDO_18V
                                                      1010 = SRC_PDO_20V
                                                      Others = Reserved
 [3:0]    RESERVED                        R           Reserved                                       0000


GO_COMMAND
Table 11. GO_COMMAND (0x09)
 Bits   Field Name          Type                      Description                                    Reset
 [7:5]    RESERVED                        R           Reserved                                       000
 [4:0]    COMMAND_FUNC                    RW          00001 = Requests the PDO set by PDO_SELECT     00000
                                                      00100 = Send out Get_SRC_Cap command
                                                      10000 = Send out hard reset command
                                                      Others = Reserved




 ©2021 Hynetek Semiconductor Co., Ltd. All rights reserved.                                              Page 7 of 8
```

## Page 8

```text
 HUSB238                                                                                   Register Information

IMPORTANT NOTICE
Hynetek Semiconductor Co., Ltd. and its subsidiaries (Hynetek) reserve the right to make corrections, enhancements,
improvements and other changes to its semiconductor products and services per JESD46, latest issue, and to discontinue any
product or service per JESD48, latest issue. Buyers should obtain the latest relevant information before placing orders and should
verify that such information is current and complete. All semiconductor products (also referred to herein as “components”) are sold
subject to Hynetek’s terms and conditions of sale supplied at the time of order acknowledgment.
Hynetek warrants performance of its components to the specifications applicable at the time of sale, in accordance with the
warranty in Hynetek’s terms and conditions of sale of semiconductor products. Testing and other quality control techniques are
used to the extent Hynetek deems necessary to support this warranty. Except where mandated by applicable law, testing of all
parameters of each component is not necessarily performed.
Hynetek assumes no liability for applications assistance or the design of Buyers’ products. Buyers are responsible for their
products and applications using Hynetek components. To minimize the risks associated with Buyers’ products and applications,
Buyers should provide adequate design and operating safeguards.
Hynetek does not warrant or represent that any license, either express or implied, is granted under any patent right, copyright,
mask work right, or other intellectual property right relating to any combination, machine, or process in which Hynetek components
or services are used. Information published by Hynetek regarding third-party products or services does not constitute a license to
use such products or services or a warranty or endorsement thereof. Use of such information may require a license from a third
party under the patents or other intellectual property of the third party, or a license from Hynetek under the patents or other
intellectual property of Hynetek.
Reproduction of significant portions of Hynetek information in Hynetek data books or data sheets is permissible only if reproduction
is without alteration and is accompanied by all associated warranties, conditions, limitations, and notices. Hynetek is not
responsible or liable for such altered documentation. Information of third parties may be subject to additional restrictions.
Resale of Hynetek components or services with statements different from or beyond the parameters stated by Hynetek for that
component or service voids all express and any implied warranties for the associated Hynetek component or service and is an
unfair and deceptive business practice.
Hynetek is not responsible or liable for any such statements.
Buyer acknowledges and agrees that it is solely responsible for compliance with all legal, regulatory and safety-related
requirements concerning its products, and any use of Hynetek components in its applications, notwithstanding any applications-
related information or support that may be provided by Hynetek. Buyer represents and agrees that it has all the necessary
expertise to create and implement safeguards which anticipate dangerous consequences of failures, monitor failures and their
consequences, lessen the likelihood of failures that might cause harm and take appropriate remedial actions. Buyer will fully
indemnify Hynetek and its representatives against any damages arising out of the use of any Hynetek components in safety-critical
applications.
In some cases, Hynetek components may be promoted specifically to facilitate safety-related applications. With such components,
Hynetek’s goal is to help enable customers to design and create their own end-product solutions that meet applicable functional
safety standards and requirements. Nonetheless, such components are subject to these terms.
No Hynetek components are authorized for use in FDA Class III (or similar life-critical medical equipment) unless authorized
officers of the parties have executed a special agreement specifically governing such use.
Only those Hynetek components which Hynetek has specifically designated as military grade or “enhanced plastic” are designed
and intended for use in military/aerospace applications or environments. Buyer acknowledges and agrees that any military or
aerospace use of Hynetek components which have not been so designated is solely at the Buyer's risk, and that Buyer is solely
responsible for compliance with all legal and regulatory requirements in connection with such use.
Hynetek has specifically designated certain components as meeting ISO/TS16949 requirements, mainly for automotive use. In any
case of use of non-designated products, Hynetek will not be responsible for any failure to meet ISO/TS16949.
Please refer to below URL for other products and solutions of Hynetek Semiconductor Co., Ltd.




 ©2021 Hynetek Semiconductor Co., Ltd. All rights reserved.
 Trademarks and registered trademarks are the property of their respective owners.
 www.hynetek.com




 ©2021 Hynetek Semiconductor Co., Ltd. All rights reserved.                                                              Page 8 of 8
```
