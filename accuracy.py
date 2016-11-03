#!/usr/bin/py
#coding:utf-8

import myltpmodel as ltp
import sys
import os

total_param = 0
correct = 0
def Statistic(row, process, rules):
  global total_param
  global correct

  for key in row.ParamKeys():
    total_param += 1

    if total_param % 1000 == 0:print 'have processed:%d'%(total_param)
    #原始币种 的值
    try:
      rule = rules[key]
    except:
      print key
      exit()

    found = False
    #{'relate':['SBV']}
    for label_name in rule.keys():
      #['SBV'] labels
      labels = rule[label_name]
      for label in labels:
        cont = process.Get(label_name, label)
        if cont == None: continue
        
        if cont.strip() == row.ParamValue(key):
          if found == False:
            correct += 1
          found = True
          break
#        else:
#          print cont,row.ParamValue(key)

if __name__ == '__main__':
  filename = sys.argv[1]
  if filename == None or len(filename) == 0:
    exit()

  #加载模型
  ltpmodel = ltp.LtpModel(os.getenv('EVA_MODEL_HOME'))
  rows = None
  with open(filename, 'rb') as f:
    rows = f.readlines()

  rules_param = rules = {'币种':{'relate':['ATT','VOB']},'数字':{'relate':['ATT'], 'pos':['m']},
              '原始币种':{'relate':['SBV']}, 
        '目标币种':{'relate':['POB','VOB']}, '原始币种金额':{'relate':['ATT']}, '汇率时间参数':{'relate':['ATT','ADV']}}
  for a in rows:
    row = ltp.Row(a)
    sentence = row.GetSentence()
    xmlstr = ltpmodel.GetLtpResultXmlString(sentence)
    xmlprocess = ltp.SentenceXmlProcessor()
    xmlprocess.FromXmlString(xmlstr)

    Statistic(row, xmlprocess, rules_param)

  print 'total:%d,correct:%d,accuracy:%g'%(total_param, correct, float(correct)/total_param)
