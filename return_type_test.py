#!/usr/bin/python
#coding:utf8
import mybaselib
import logging
import jieba
import jieba.analyse
import numpy as np
import csv
import sys
import stat
import os
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
  fname = sys.argv[1]
  logger.debug(fname)
  return_rules = mybaselib.ReturnRules()
  return_rules.Load(fname)

  sentence = '向日葵餐厅秩怎么样'
  return_type = return_rules.GetReturnType(sentence)
  logger.debug('%s', return_type)

