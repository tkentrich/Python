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

def bamatch(pbam, sol):
  if sol >= 2 ** len(pbam):
    return False
  bsol = bin(sol)[2:].zfill(len(pbam))[0:len(pbam)]
  for i,c in enumerate(pbam):
    if c in ['0','1'] and c != bsol[i]:
      return False
  return True

def humanize(string):
    newname=''
    chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ-_0123456789'
    for c in string:
        newname += chars[c % len(chars)]
    return newname

def parse(data):
  dict = {}
  (dict['direction'], 
   dict['magnitude'], # unsigned int
   dict['name'],
   dict['id']
  ) = struct.unpack('<Ii10sB', data)
  dict['name'] = humanize(dict['name'])
  dict['direction'] = bam(dict['direction'], 360, 16)
  return dict

def main():
  # Demonstrate parsing data from random byte stream
  data = [random.randint(0,255) for x in range(19)]
  d = parse(bytes(data))
  for k in d:
    print("%s: %s"%(k, d[k]))

  # Demonstrate effect of bits on BAM
  moredata = sorted(bytes([random.randint(0,255) for x in range(10)] + [0,1,2,4,8,16,32,64,128,255]))
  for x in moredata:
      print("{0:02x} {0:08b} {1}".format(x,bam(x, 360, 8)))
    
if __name__ == '__main__':
  main()
