import serial
#a=['02', '03', '04', '04']
a=['03', '03', '04', '04', '03', '04', '03', '04', '03', '04', '04', '04', '03', '03', '03', '04', '04', '03', '03', '03', '03', '04', '04', '04', '03', '03', '04', '03', '03', '04', '03', '04', '03', '04', '03', '06', '08', '04', '03', '01', '04', '03', '03', '04', '03', '03', '03', '06', '07', '04', '04', '01', '04', '03', '03', '04', '04', '03', '03']
#output_str=[elem.strip() for elem in a]
print("arr is",a)
output_str = ' '.join(a)
output_str_f="'{}'".format(output_str)
print(output_str_f)
ser=serial.Serial('/dev/ttyTHS1',115200)
data=bytes.fromhex(output_str)
print("fromhex is:",data)
ser.write(data)
ser.close()
