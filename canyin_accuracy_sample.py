#!/usr/bin/python
#coding:utf8
import model_test as mymodel
import myltpmodel as myltp
import mltoolkits.mylog as mylog
import logging
import sys
import os
import time
reload(sys)
sys.setdefaultencoding('utf8')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if __name__ == '__main__':
  # check and process input arguments
  if len(sys.argv) < 5:
    print '参数少'
    sys.exit()

  #加载模型
  userdict_file, vector_file, sample_file, rules_file = sys.argv[1:5]
  canyin_model = mymodel.SentModel()
  canyin_model.Load(userdict_file, vector_file, sample_file, rules_file)

  #准确率
  N = 0
  T = 0
  with open(sample_file, 'rb') as rf:
    lines = rf.readlines()
    N = len(lines)
    for line in lines:
      row = myltp.Row(line)
      params,re_type = canyin_model.GenParamAndReturntype(row.GetSentence())
      keys = params.keys()
      i = 0
      #
#      for key in row.ParamKeys():
#        logger.debug('%s=%s', key, row.ParamValue(key))
#      time.sleep(1)
      #
      for key in keys:
        value = row.ParamValue(key)
        logger.debug('%s %s %s %s', row.GetSentence(), key, params[key], value)
        if value is None or value != params[key]:
          logger.info('%s,%s, %s %s', row.GetSentence(), key, value, params[key])
          break
        i+=1
      if len(params) == len(keys) and i >= len(keys):
        T+=1
        logger.debug('参数相同')
#      else:
#        logger.debug('sent:%s, i:%d,参数个数:%d:%d', row.GetSentence(), i, len(keys), len(params))
#      time.sleep(1)
  logger.info('N:%d,T:%d', N, T)
  logger.info('准确率:%f', T*1.0/N)
