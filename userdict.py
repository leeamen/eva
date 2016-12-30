#!/usr/bin/python
#coding:utf8
import mybaselib
import logging
import os
import stat
import sys
import numpy as np
import multiprocessing
import jieba

reload(sys)
sys.setdefaultencoding('utf8')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def walktree(dirname, callback, userdata):
  for f in os.listdir(dirname):
    pathname = os.path.join(dirname, f)
    mode = os.stat(pathname).st_mode
    if stat.S_ISDIR(mode):
      pass
      # It's a directory, recurse into it
      #walktree(pathname, callback)
    elif stat.S_ISREG(mode):
      # It's a file, call the callback function
      callback(pathname, userdata)
    else:
      # Unknown file type, print a message
      logger.error('Skipping %s', pathname)

def GenUserdict(fname, userdata):
  if '.txt' != fname[-4:]:
    return
  logger.info('start process file:%s', fname)
  wf = open(userdata['output'], 'a')
  with open(fname, 'rb') as rf:
    while True:
      line = rf.readline()
      if line is None or len(line) == 0:
        break;
      row = mybaselib.Row(line)
      for key in row.ParamKeys():
        #词 + 词频(可省略) + 属性(可省略)
#        wf.write(row.ParamValue(key) + ' 3' + '\n')
        wf.write(row.ParamValue(key) + '\n')
  wf.flush()
  wf.close()

if __name__ == '__main__':
  logger.debug('start...')

  userdata = {}
  userdata['output'] = './data/userdict.data'
  os.system('rm -f ' + userdata['output'])
  walktree('data', GenUserdict, userdata)

  sys.exit()

#  input1 = sys.argv[1]
#  output = './data/userdict.data'
#  GenUserdict(input1, output)

  #test
#  jieba.load_userdict('./data/userdict.data')
#  sentence = '乡村之屋饭店日落是较快的吗'
#  logger.debug('%s', '|'.join(jieba.lcut(sentence, cut_all = False)))

