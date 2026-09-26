"""Generic development-board signal names; electrical endpoints are unchanged."""
def apply(parts):
 names={'GPIO0':'ESP_GPIO0_BOOT','CHIP_PU':'ESP_EN','ESP_TXD':'ESP_GPIO43_TXD','ESP_RXD':'ESP_GPIO44_RXD','PPS':None,'CRESET_B':'FPGA_CRESET_N','CDONE':'FPGA_CDONE','FSPI_CLK':'LINK_SCK','FSPI_CS':'LINK_CS_N','FSPI_MOSI':'LINK_MOSI','FSPI_MISO':'LINK_MISO','FSPI_HD':'LINK_IO3','FSPI_WP':'LINK_IO2','VDD_CPU_MAIN':'ESP_VDD3P3','LNA_IN':'RF_IN','ANTENNA':'RF_ANT'}
 for pin in parts['U2']['pins'].values():
  net=pin['net']
  if net and (net.startswith('BIT') or net in ['F2','F3','F4','F6','F9','F10','F19','F20','F23','F25','HQ_OSC','EXT_33','EXT_EN','RGB_0','RGB_1','RGB_2']):
   names[net]='FPGA_'+pin['name']
 for c in parts.values():
  for pin in c['pins'].values():pin['net']=names.get(pin['net'],pin['net'])
 gpio={5:0,6:1,7:2,8:3,9:4,10:5,11:6,12:7,13:8,14:9,15:10,16:11,17:12,18:13,19:14,21:15,22:16,23:17,24:18,25:19,26:20,28:21,37:33,38:34,39:35,40:36,41:37,42:38,43:39,44:40,46:41,47:42,48:43,49:44,50:45,55:46}
 for pin,n in gpio.items():parts['U1']['pins'][str(pin)]['name']=f'GPIO{n}'
 parts['U1']['pins']['25']['name']='GPIO19/USB_D-';parts['U1']['pins']['26']['name']='GPIO20/USB_D+'
 return names
