import struct
import json
import random

def bam(data, highrange, bitlength):
  multiplier = 1
  if data < 0:
    multiplier = -1
  data *= multiplier
  bitstring = bin(data)[2:].zfill(bitlength)[0:bitlength]
  result = 0.
  diff = highrange * .5
  for b in bitstring:
    if b == '1':
      result += diff
    diff *= 0.5
  return result * multiplier
  
def parse(data):
  dict = {}
  (dict['direction'], unsigned int
   dict['magnitude'],
   dict['name'],
   dict['id']
  ) = struct.unpack('<Ii10sB', data)
  dict['field2'] = bam(dict['field2'], 360, 16)
  return dict

def main():
  data = [random.randint(0,255) for x in range(19)]
  d = parse(data)
  for k,v in d:
    print "%s: %s"%(k, v)
    
if __name__ == '__main__':
  main()
