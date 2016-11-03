#!/usr/bin/python
#coding:utf-8

import myltpmodel as ltp
import sys
import os
import codecs

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print 'usage:%s file\n' %sys.argv[0]
    exit()

  filename = sys.argv[1]

  #load ltpmodel
  ltpmodel = ltp.LtpModel(os.getenv('EVA_MODEL_HOME'))

  rows = None
  with open(filename, 'rb') as f:
    rows = f.readlines()

  with open(filename + '.xml.txt', 'wb') as f:
    utf8_f = codecs.EncodedFile(f, 'utf-8', 'gbk', 'ignore')
    for a in rows:
      row = ltp.Row(a)
      xmlstr= ltpmodel.GetLtpResultXmlString(row.GetSentence())

      utf8_f.write(xmlstr)

    utf8_f.flush()

