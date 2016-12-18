# eva
执行步骤：
1.创建用户字典
py userdict.py

2.切文件
py cutwords.py

3.生成词向量
py word2vec.py ./data/all.cuts ./data/model.bin ./data/model.vector

4. 餐饮句子测试
py canyin_sample.py ./data/userdict.data ./data/model.vector ./data/gen_question_canyin.txt ./data/canyin.return.rules

6.餐饮样本准确率测试
py canyin_accuracy_sample.py ./data/userdict.data ./data/model.vector ./data/gen_question_canyin.txt ./data/canyin.return.rules

说明：
词向量100维，窗口2，阈值0.7

