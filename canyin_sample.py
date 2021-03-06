#!/usr/bin/python
#coding:utf8
import mymodel
import mybaselib
import logging
import sys
import os
reload(sys)
sys.setdefaultencoding('utf8')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
  # check and process input arguments
  if len(sys.argv) < 5:
    print '参数少'
    sys.exit()

  userdict_file, vector_file, sample_file, rules_file = sys.argv[1:5]
  canyin_model = mymodel.SentModel()
  canyin_model.Load(userdict_file, vector_file, sample_file, rules_file)

  sentence = '我想吃罗望子鲈鱼'
  logger.info('%s', sentence)
  logger.info('%s', canyin_model.GenHttpInterface(sentence))
  while True:
    sentence = raw_input('输入句子:')
    http = canyin_model.GenHttpInterface(sentence)
    logger.info('%s', http)
    #
    params, re_type = canyin_model.GenParamAndReturntype(sentence)
    logger.info('return_type:%s', re_type)
    for key in params.keys():
      logger.info('%s:%s', key, params[key])
    
