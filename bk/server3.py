import socket
import os
import time


HOST = '192.168.61.101'
PORT = 5991
ADDR = (HOST,PORT)
BUFSIZE = 4096
OFFSET = BUFSIZE*8 + BUFSIZE

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


serv.bind(ADDR)
serv.listen(5)

print ('listening ...')

while True:
  titleBin=""
  title=""
  titleData=0
  conn, addr = serv.accept()
  print ('client connected ... ', addr)
  start_time = time.time()
  titleFile = open('temp_title', 'wb')
  dataFile = open('temp_data', 'wb')
  while True:
    data = conn.recv(BUFSIZE)
    if not data: break
    if titleData>=4096:
      dataFile.write(data)
      print ('writing file .... temp_data ... ',len(data))
    if titleData<4096:
      if titleData+len(data)>4096:
        print('EXCEPTION')
        titleFile.write(data[:4096-titleData])
        print ('writing file .... temp_title ... ',4096-titleData)
        dataFile.write(data[4096-titleData:])
        print ('writing file .... temp_data ... ',len(data[4096-titleData:]))
        titleData=titleData+len(data)
      else:
        titleFile.write(data)
        print ('writing file .... temp_title ... ',len(data))
        titleData=titleData+len(data)

  print('split done')

  titleFile.close()
  dataFile.close()
  print ('finished writing file')
  conn.close()
  print ('client disconnected')
  with open('temp_title', 'rb') as fobj:
    raw_bytes = fobj.read()
    titleBin =' '.join(map(lambda x: '{:08b}'.format(x), raw_bytes))
  STARTINDEX = titleBin.find('1')
  titleBin = titleBin[STARTINDEX:]
  SPACEINDEX = titleBin.find(' ')
  tempStr = titleBin[:SPACEINDEX]
  for x in range(8-len(tempStr)):
    tempStr='0'+tempStr
  titleBin = tempStr + titleBin[SPACEINDEX:]
  print(titleBin)
  elapsed_time = time.time() - start_time
  print('Elapsed Time: ',elapsed_time)
  for word in titleBin.split():
    title=title+chr(int(word, 2))
  print(title)
  try:
    os.rename('temp_data', title)
  except FileExistsError as e:
    print('File Already exists, Overriding the file...')
    os.remove(title)
    os.rename('temp_data', title)





