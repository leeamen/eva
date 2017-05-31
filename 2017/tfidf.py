# coding:utf-8  
import jieba  
import jieba.posseg as pseg  
import os  
import sys  
from sklearn import feature_extraction  
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer  
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
import scipy

reload(sys)


def str2num(data):
   labels = ['ADJ','ATTR_COST','ATTR_POS','FOODNAMELIST','METATYPE','POILIST']
   return labels.index(data)

if __name__ == "__main__":  
    '''
    corpus=["我 来到 北京 清华大学",#第一类文本切词后的结果，词之间以空格隔开  
        "他 来到 了 网易 杭研 大厦",#第二类文本的切词结果  
        "小明 硕士 毕业 与 中国 科学院",#第三类文本的切词结果  
        "我 爱 北京 天安门"]#第四类文本的切词结果  

    '''
    '''
     切词后的文件
    '''
    filename = sys.argv[1]
    corpus = []
    with open(filename, 'rb') as rf:
      rows = rf.readlines()
      for row in rows:
        corpus.append(row)

    print '总长度:%d' %len(corpus)
#    print corpus
    vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频  
    transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值  
 #   print  vectorizer.fit_transform(corpus)
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵  
    print 'is sparse:', scipy.sparse.issparse(tfidf)
    word=vectorizer.get_feature_names()#获取词袋模型中的所有词语  
    print '词长度:%d'%(len(word))
#    print '|'.join(word)
    print 'tfidf.shape:', tfidf.shape
    #tfidf.reshape(tfidf.shape)
    weight = tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重  
    print weight
  #  print tfidf.shape,tfidf.dtype
  #  for i in range(len(weight)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重  
  #      print u"-------这里输出第",i,u"类文本的词语tf-idf权重------"  
  #      for j in range(len(word)):  
  #          print word[j],weight[i][j]
#    print weight.shape
    #arr = np.array(weight, dtype = np.float)
    print weight.shape

    #
    fname = sys.argv[2]
    train_y = np.loadtxt(fname, delimiter = ' ', usecols = (1,), converters = {1:str2num})
    train_x = tfidf.toarray()

    train_data = np.column_stack((train_x, train_y))

    np.random.shuffle(train_data)
    split_idx = int(2./3 * len(train_data))
    train_x = train_data[0:split_idx, 0:-1]
    test_x = train_data[split_idx+1:,0:-1]
    train_y = train_data[0:split_idx, -1]
    test_y = train_data[split_idx+1:, -1]
    print 'train_x:',train_x
    print 'train_y:',train_y
    print 'test_x:',test_x
    print 'test_y:',test_y


    '''
    使用gbdt训练
    '''
    gbdt = GradientBoostingClassifier(verbose = 1)
    gbdt.fit(train_x, train_y)
    pred_tert_y = gbdt.predict(test_x)

    '''
    计算accuracy
    '''
    print 'accuracy:', 1.*np.sum(test_y == pred_tert_y)/len(test_y)

