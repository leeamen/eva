#!/usr/bin/python
#coding:utf-8

import lltpmodel as lee
import pyltp as ltp
import os
import sys
import re
import csv
import codecs

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
  input_file = './data/gen_question_huilv.txt'
  if len(sys.argv) < 2:
    print 'usage:%s file\n' %sys.argv[0]
    exit()

  input_file = sys.argv[1]
  ltpmodel = lee.LtpModel(os.getenv('EVA_MODEL_HOME'))

  #输出文件
  outputfile = input_file + '.csv'
  out_f = open(outputfile, 'wb')
  out_utf8_f = codecs.EncodedFile(out_f, 'utf-8', 'gbk', 'ignore')
  writer = csv.writer(out_utf8_f)
  writer.writerow(['句子','分词','词性标注','命名实体标注','关系类型'])

  with open(input_file, 'rb') as f:
    line_list = f.readlines()
    i = 0
    for line in line_list:
#      print line.strip('\n')
      sentences = line.strip('\n')

      sentence = filter(lambda x: len(x) > 0, re.split('{|}' , sentences))[0].strip()

      #sentence =  .split()[0]
      #print sentence
      xmlstr = ltpmodel.GetLtpResultXmlString(sentence)
      sentence1 = ltpmodel.GetSentenceFromXmlString(xmlstr)
      #print sentence1
      if not sentence == sentence1:
        print "(%s,%s)(%d,%d)" %(sentence,sentence1,len(sentences),len(sentence1))

      #参数匹配
      #sentences.replace('{', '\t').replace('}', '\t').replace(' ', '').split('\t')[1]
      parameters = filter(lambda x:len(x) > 0, re.split('}|{', sentences))[1].strip()

     # write parameters to file
      xmlprocessor = lee.SentenceXmlProcessor()
      xmlprocessor.FromXmlString(xmlstr)
      for para in filter(lambda x: len(x) > 0, parameters.split(',')):
        cont = filter(lambda x:len(x)>0, re.split('=', para))[0].strip()
        dic = xmlprocessor.GetContTagDic(cont)
        if dic == None:
          writer.writerow([sentence, '%s:没有词汇对应'%(cont)])
        else:
          writer.writerow([sentence, dic['cont'],dic['pos'],dic['ne'],dic['relate']])

      i+=1
      if not i % 1000: print 'Have done %d'%i

  out_f.close()

