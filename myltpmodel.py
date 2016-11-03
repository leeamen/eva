#!/usr/bin/python
#coding:utf8

#美化
import sys
import xml.etree.cElementTree as et
import os
import re
import pyltp as ltp

reload(sys)
sys.setdefaultencoding('utf-8')

class Row:
  def __init__(self, row):
    self.row = row

    #参数表
    self.parameter = {}

    #
    self.array = filter(lambda x:len(x.strip()) > 0, re.split('{|}', self.row))

    self.sentence = self.array[0].strip()
    param = self.array[1]
    for a in param.split(','):
      try:
        key = a.split('=')[1].strip()
        value = a.split('=')[0].strip()
        self.parameter[key] = value
      except:
        print a
      #  exit()

    #参数多态标志
#    self.choice = int(self.array[2].strip()[0])

  def GetSentence(self):
    return self.sentence

  def ParamKeys(self):
    return self.parameter.keys()

  def ParamValue(self, key):
    try:
      return self.parameter[key]
    except:
      return None

class SentenceXmlProcessor:
  def __init__(self):
    self.xmlstr = ''
    self.root = None

  def FromXmlString(self, xmlstr):
    self.xmlstr += xmlstr
    self.root = et.fromstring(self.xmlstr)

  def GetPos(self, val):
    if self.root == None: return None

    for e in self.root.iter('word'):
      if e.attrib['pos'] == val:
        return e.attrib['cont']
    return None

  def GetRelate(self, val):
    if self.root == None: return None
    for e in self.root.iter('word'):
      if e.attrib['relate'] == val:
        return e.attrib['cont']
    return None

  def Get(self, key, value):
    if self.root == None:return None

    for e in self.root.iter('word'):
      if e.attrib[key] == value:
        return e.attrib['cont']
    return None

  def GetContTagDic(self, cont):
    taglist = {}
    if self.root == None:return None
    for e in self.root.iter('word'):
      if e.attrib['cont'] == cont:
        taglist['cont'] = cont
    #    taglist['id'] = e.attrib['id']
        taglist['ne'] = e.attrib['ne']
    #    taglist['parent'] = e.attrib['parent']
        taglist['pos'] = e.attrib['pos']
        taglist['relate'] = e.attrib['relate']
        return taglist

class LtpModel:
  def __init__(self, ltp_data_dir):
    self.ltp_data_dir = ltp_data_dir
    cws_model = ltp_data_dir + 'cws.model'
    self.segmentor = ltp.Segmentor()
    self.segmentor.load(cws_model)
    pos_model = ltp_data_dir + 'pos.model'
    self.postagger = ltp.Postagger() # 初始化实例
    self.postagger.load(pos_model)  # 加载模型
    ner_model = ltp_data_dir + 'ner.model'
    self.recognizer = ltp.NamedEntityRecognizer() # 初始化实例
    self.recognizer.load(ner_model)  # 加载模型
    parser_model = ltp_data_dir + 'parser.model'                                            
    self.parser = ltp.Parser() # 初始化实例                                                                     
    self.parser.load(parser_model)  # 加载模型
  def __del__(self):
    self.parser.release()#释放模型
    self.recognizer.release()#释放模型
    self.postagger.release()#释放模型
    self.segmentor.release()

  def indent(self, elem, level=0):
    i = "\n" + level*"\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            self.indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

  def GetSentenceFromXml(self, xmlfile):
    tree = et.ElementTree(file = xmlfile)
    sentence = ''
    for e in tree.iter('word'):
      sentence += e.attrib['cont']
      #print e.attrib['cont']
    return sentence
  
  def GetSentenceFromXmlString(self, xmlstr):
    root = et.fromstring(xmlstr)
    sentence = ''
    for e in root.iter('word'):
      sentence += e.attrib['cont']
    return sentence
  
  def WriteXmlStr2File(self, xmlstring, xmlfile):
    with open(xmlfile, 'wb') as f:
      f.write(xmlstring)
  
  def GetLtpResultXmlString(self, sentences):
    root = et.Element('doc')
    para = et.Element('para', {'id':'0'})
    root.append(para)
    #ltp_data_dir = os.getenv('EVA_MODEL_HOME')
    #words = segmentor.segment(ltp.SentenceSplitter.split(sentence)[0])
    i = 0
    for sentence in ltp.SentenceSplitter.split(sentences):
      cont_list = []
      pos_list = []
      ne_list = []
      parent_list =[]
      relate_list =[]
  
      # get result
      self.GenSentenceLabelList(sentence, cont_list, pos_list, ne_list, parent_list, relate_list)
  
      #print cont_list
      #print relate_list
  
      #element
      elem = self._getElement(i, sentence, cont_list,pos_list,ne_list,parent_list,relate_list)
      para.append(elem)
      i+=1
  
    #write to xml
    self.indent(root)
    tree = et.ElementTree(root)
    #tree.write(xmlfile, encoding = 'UTF-8',  method = 'xml')
    return et.tostring(root, encoding = 'UTF-8', method = 'xml')
    
  def _getElement(self, i, sentence, cont_list,pos_list,ne_list,parent_list,relate_list):
    root = et.Element('sent')
    root.set('id', str(i))
    root.set('cont', sentence)
  
    for i in range(0, len(cont_list)):
      elem = et.Element('word')
      elem.set('id', str(i))
      elem.set('cont', cont_list[i])
      elem.set('pos', pos_list[i])
      elem.set('ne', ne_list[i])
      elem.set('parent', str(parent_list[i]))
      elem.set('relate', relate_list[i])
      
      #append
      root.append(elem)
  
    return root
  
  #  cws_model = ltp_data_dir + 'cws.model'
  #  
  #  #分词
  #  segmentor = ltp.Segmentor()
  #  segmentor.load(cws_model)
    
  def GenSentenceLabelList(self, sentence, cont_list, pos_list, ne_list, parent_list, relate_list):
   # cws_model = ltp_data_dir + 'cws.model'
  #  
  #  #分词
   # segmentor = ltp.Segmentor()
   # segmentor.load(cws_model)
    
   # sentence = '中国进出口银行与中国银行加强合作。'
  #  sentence = '300欧元相当于多少美元？'
    words = self.segmentor.segment(sentence)
    for word in words:
      cont_list.append(word)
  
  #  print "\t".join(words)
    
    #词性标注
   # pos_model = os.getenv('EVA_MODEL_HOME') + 'pos.model'
   # postagger = ltp.Postagger() # 初始化实例
   # postagger.load(pos_model)  # 加载模型
    #print 'load %s ok!' %(pos_model)
    postags = self.postagger.postag(words)  # 词性标注
    for postag in postags:
      pos_list.append(postag)
  #  print '\t'.join(postags)
    
    #命名实体识别
#    ner_model = os.getenv('EVA_MODEL_HOME') + 'ner.model'
#    recognizer = ltp.NamedEntityRecognizer() # 初始化实例
#    recognizer.load(ner_model)  # 加载模型
    netags = self.recognizer.recognize(words, postags)  # 命名实体识别
    for netag in netags:
      ne_list.append(netag)
  #  print '\t'.join(netags)
    
    #依存句法分析
#    parser_model = os.getenv('EVA_MODEL_HOME') + 'parser.model'
#    parser = ltp.Parser() # 初始化实例
#    parser.load(parser_model)  # 加载模型
    arcs = self.parser.parse(words, postags)  # 句法分析
    for arc in arcs:
      parent_list.append(arc.head)
      relate_list.append(arc.relation)
#  print "\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs)
  
  
  #语义角色标注
  #srl_model_dir = os.getenv('EVA_MODEL_HOME') + 'srl/'
  #labeller = ltp.SementicRoleLabeller() # 初始化实例
  #labeller.load(srl_model_dir)  # 加载模型
  #roles = labeller.label(words, postags, netags, arcs)  # 语义角色标注
  #for role in roles:
  #    print role.index, "\t".join(
  #        ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments])
  #labeller.release()  # 释放模型
#  parser.release()  # 释放模型
#  recognizer.release()  # 释放模型
#  postagger.release()  # 释放模型
#  segmentor.release()

if __name__ == '__main__':
  sentences = '1韩元相当于多少欧元'
  sentences = '给我当前加元兑人民币的汇率'
  sentences = '300欧元相当于多少美元  {欧元=原始币种, 300=数字, 美元=目标币种}  2.转化后的金额'
  sentences = '一百港币可以换多少泰铢'
  sentences = '我想吃猪肋排炒饭'
  sentences = '“芒果糯米鸡“用泰米尔语怎么说'
  sentences = '伍拾新加坡元相当于多少马来西亚币 {新加坡元=原始币种, 伍拾=数字, 马来西亚币=目标币种} 2.转化后的金额'
#  sentences = 'http://pan.baidu.com/s/1o7hnpmy'
  sentences = '塔氏视星鲶，为辐鳍鱼纲鲶形目视星鲶科的其中一种，为热带淡水鱼，分布于南美洲乌卡雅利河上游流域，体长可达8公分，栖息在底层水域，生活习性不明。'
  sentences = '300欧元相当于多少美元'
  sentences = '一千马来西亚币可以换成多少韩元'

  sentence = sentences.replace('{', '\t').replace('}', '\t').replace(' ', '').split('\t')[0]
  
  ltpmodel = LtpModel(os.getenv('EVA_MODEL_HOME'))
  xmlstring = ltpmodel.GetLtpResultXmlString(sentence)
  ltpmodel.WriteXmlStr2File(xmlstring, 'b.xml')

#  xmlprocessor = SentenceXmlProcessor()
#  xmlprocessor.FromXmlString(xmlstring)

#  parameters = sentences.replace('{', '\t').replace('}', '\t').replace(' ', '').split('\t')[1]
#  for para in parameters.split(','):
#    cont = para.split('=')[0].replace(' ','')
#    dic = xmlprocessor.GetContTagDic(cont)
#    if dic == None:
#      print cont
#    else:print dic['cont'],dic
#  #原始币种
#  oriCurrency = xmlprocessor.GetRelate('SBV')
#  #目标币种
#  targetCurrency = xmlprocessor.GetRelate('POB')
#  if targetCurrency == None:targetCurrency  = xmlprocessor.GetRelate('VOB')
#  #原始币种金额
#  oriNumber = xmlprocessor.GetPos('m')
#  print '原始币种:%s\n目标币种:%s\n原始币种金额:%s'%(oriCurrency, targetCurrency, oriNumber)



