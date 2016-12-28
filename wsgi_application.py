#!/usr/bin/python
#coding:utf8

import mymodel
import mybaselib
import logging
import sys
import os

from spyne.model.primitive._base import Any
from spyne.model.primitive._base import AnyDict
from spyne.model.primitive._base import AnyHtml
from spyne.model.primitive._base import AnyXml
from spyne.model.primitive._base import Boolean

from spyne.model.primitive.string import Unicode
from spyne.model.primitive.string import String
from spyne.model.primitive.string import AnyUri
from spyne.model.primitive.string import Uuid
from spyne.model.primitive.string import ImageUri
from spyne.model.primitive.string import Ltree

reload(sys)
sys.setdefaultencoding('utf8')

from spyne import Application, rpc, ServiceBase,\
    Integer, Unicode
from spyne import Iterable
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument
from spyne.server.wsgi import WsgiApplication

class SentenceModeldService(ServiceBase):
  #远程服务
  @rpc(String, _returns=AnyDict())#Iterable(Unicode))
  def canyin(ctx, sentence):
#    global logger
#    global canyin_model

    logger.debug('调用餐饮接口')
    logger.debug('句子:%s', sentence)
    logger.debug('type:%s', sentence.__class__)

    result_dict = {}
    result_params = []
    result_dict['params'] = result_params

    params, return_type = canyin_model.GenParamAndReturntype(sentence)
    logger.info('return_type:%s', return_type)
    for key in params.keys():
      logger.debug('%s:%s', key, params[key])
      logger.debug('type:%s', params[key].__class__)

      obj = {}
      obj['attr_name'] = key
      obj['attr_value'] = params[key]
      result_params.append(obj)

    result_dict['return_type'] = return_type
    return result_dict
    
if __name__ == '__main__':
  if len(sys.argv) < 5:
    print '参数少'
    sys.exit()

  logger = logging.getLogger(sys.argv[0])
  logger.setLevel(logging.DEBUG)

  userdict_file, vector_file, sample_file, rules_file = sys.argv[1:5]
  canyin_model = mymodel.SentModel()
  canyin_model.Load(userdict_file, vector_file, sample_file, rules_file)

  # You can use any Wsgi server. Here, we chose
  # Python's built-in wsgi server but you're not
  # supposed to use it in production.
  #定义应用
  application = Application([SentenceModeldService],
    tns='spyne.sentmodel',
    in_protocol=HttpRpc(validator='soft'),
    out_protocol=JsonDocument(),
  )
  from wsgiref.simple_server import make_server
  wsgi_app = WsgiApplication(application)
  server = make_server('0.0.0.0', 8000, wsgi_app)
  server.serve_forever()

