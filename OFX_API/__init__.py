#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.
import random, string, json

from django.apps import apps
import re
from uuid import UUID
from datetime import datetime, timedelta
from .celery import app as celery_app
__all__ = ('celery_app',)

class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)

def getRandomStrings(str_length = 32):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=str_length))

# class magicSerializer(object):
#     dateFormat='%Y-%m-%d'
#     dateTimeFormat='%Y-%m-%dT%H:%M:%S'
#     def daysRange(self,from_date='2022-01-04',to_date='2022-02-20'):
#         return (datetime.strptime(to_date, self.dateFormat) - datetime.strptime(from_date, self.dateFormat)).days+1
    
#     def weeksRange(self,from_date='2022-01-04',to_date='2022-02-20'):
#         dt1 = datetime.strptime(from_date, self.dateFormat)
#         dt2 = datetime.strptime(to_date, self.dateFormat)
#         day1 = (dt1 - timedelta(days=dt1.weekday()))
#         day2 = (dt2 - timedelta(days=dt2.weekday()))
#         return int(((day2 - day1).days / 7)+1)

#     def addDays(self,date='2022-01-04',days=1):
#         return datetime.strptime(date, self.dateFormat) + timedelta(days=days)

#     def makeKey(self,strd=''): 
#         return re.sub("[^A-Za-z0–9]","",strd).lower()

#     def orderedDictToDict(self,data={}):
#         if isinstance(data,list) is True:
#             rd = []
#             for x in data:
#                 rd.append(x if isinstance(x, str) or isinstance(x, int) or isinstance(x, float) else self.orderedDictToDict(data=x))
#             return rd
#         elif isinstance(data,dict) is True:
#             rd = {}
#             for x in list(data.keys()):
#                 rd[x] = data[x] if isinstance(data[x], str) or isinstance(data[x], int) or isinstance(data[x], float) else self.orderedDictToDict(data=data[x])
#             return rd
#         else:
#            return data if isinstance(data, str) or isinstance(data, int) or isinstance(data, float) else dict(data)


#     def readArguments(self,data={},readData={},onlyArguments=True):
#         rData = {}
#         for x in data.query_params:
#             if x in list(readData.keys()):
#                 if isinstance(data.query_params[x],list):
#                     rData[x] = []
#                     for y in data.query_params[x]:
#                         rData[x].append(self.readArguments(data={"query_params":data.query_params[x][y]},readData=readData[x],onlyArguments=True)["data"])
#                 else:
#                     if readData[x]=='split':
#                         rData[x] = [stkr for stkr in data.query_params[x].split('|')]
#                     elif x=='id' or x=='pk':
#                         if len(str(data.query_params[x])) < 20:
#                             rData[x] = int(data.query_params[x])
#                         else:
#                             rData[x] = data.query_params[x] 
#                     else:
#                         rData[x] = data.query_params[x]
#         if onlyArguments is not True:
#             if data.headers.get('required',None) is not None:
#                 reqData = json.loads(data.headers['required'])
#                 if 'id' not in reqData and 'pk' not in reqData:
#                     reqData.insert(0,'id')
#             else:
#                 reqData = '__all__'
#         else:
#             reqData = None
#         return {"data": rData, "required": reqData}

#     def readPOSTArguments(self,data={},readData={},onlyArguments=True):
#         rData = {}
#         for x in data.data:
#             if x in list(readData.keys()):
#                 if isinstance(data.data[x],list):
#                     rData[x] = []
#                     for y in data.data[x]:
#                         rData[x].append(self.readArguments(data={"query_params":data.data[x][y]},readData=readData[x],onlyArguments=True)["data"])
#                 else:
#                     if readData[x]=='split':
#                         rData[x] = [stkr for stkr in str(data.data[x]).split('|')]
#                     elif x=='id' or x=='pk':
#                         if len(str(data.data[x])) < 20:
#                             rData[x] = int(data.data[x])
#                         else:
#                             rData[x] = data.data[x] 
#                     else:
#                         rData[x] = data.data[x]
#         if onlyArguments is not True:
#             if data.headers.get('required',None) is not None:
#                 reqData = json.loads(data.headers['required'])
#                 if 'id' not in reqData and 'pk' not in reqData:
#                     reqData.insert(0,'id')
#             else:
#                 reqData = '__all__'
#         else:
#             reqData = None
#         return {"data": rData, "required": reqData}

#     def sanitizeObject(self,writeOn={},obj={},manyFeilds=[]):
#         # print("obj",obj)
#         try:
#             for j in obj:
#                 splt = j.split('__')
#                 if splt[0] in manyFeilds or len(manyFeilds)==0:
#                     if len(splt)>1:
#                         if writeOn.get(splt[0],None) is None:
#                             writeOn[splt[0]] = {}
#                         objX = {}
#                         objX["__".join(splt[1:])] = obj[j]
#                         writeOn[splt[0]] = self.sanitizeObject(writeOn=writeOn[splt[0]],obj=objX)
#                     else:
#                         writeOn[j] = obj[j]
#         except Exception as e:
#             print("Data_Object_Error:",obj,writeOn)
#         return writeOn

#     def compareAndJoin(self,obj=[],manyFeilds=[],modelFeilds=[],queryPerams=[]):
#         writeOnX={}
#         for i in json.loads(json.dumps(obj[0])):
#             if i in modelFeilds and i in queryPerams:
#                 writeOnX[i] = json.loads(json.dumps(obj[0]))[i]
#         for i in manyFeilds:
#             if i in queryPerams:
#                 if writeOnX.get(i,None) is None:
#                     writeOnX[i] = []
#                 else:
#                     writeOnX[i] = [writeOnX[i]]
#         for i in manyFeilds:
#             if i in queryPerams:
#                 for j in range(1, len(obj)):
#                     if obj[j].get(i,None) is not None:
#                         writeOnX[i].append(json.loads(json.dumps(obj[j][i])))
#                     elif writeOnX.get(i,None) is not None:
#                         del writeOnX[i]
#         for i in manyFeilds:
#             if writeOnX.get(i,None) is not None and len(writeOnX[i])==1:
#                 isValid = False
#                 for ii in writeOnX[i][0]:
#                     if writeOnX[i][0][ii] is not None:
#                         isValid = True
#                 if isValid is False:
#                     del writeOnX[i][0]
#         # for i in writeOnX:
#         #     if isinstance(writeOnX[i],dict):
#         #         isValid = False
#         #         for ii in writeOnX[i]:
#         #             if writeOnX[i][ii] is not None:
#         #                 isValid = True
#         #         if isValid is False:
#         #             writeOnX[i] = None

#         return writeOnX

#     def serializerObject(self,dbObj,model=None,queryPerams=[]):
#         queryPeramsX = [x.split('__')[0] for x in queryPerams]
#         json_data = list(dbObj)
#         rDbObj = {}
#         manyFeildsX = [{"name":f.name,"type":f.__class__.__name__} for f in model._meta.get_fields()] if model is not None else []
#         for xr in json_data:
#             key = 'id_{id}'.format(id=xr["id"])
#             if rDbObj.get(key, None) is None:
#                 rDbObj[key] = []
#             rDbObj[key].append(json.loads(json.dumps(self.sanitizeObject(obj=xr,manyFeilds=[ii["name"] for ii in manyFeildsX]), cls=UUIDEncoder, default=str)))
#         manyFeilds = []
#         modelFeilds = []
#         for x in manyFeildsX:
#             if x["type"]=='ManyToManyField':
#                 manyFeilds.append(x["name"])
#             modelFeilds.append(x["name"])
#         for x in rDbObj:
#             rDbObj[x] = self.compareAndJoin(obj=rDbObj[x],manyFeilds=manyFeilds,modelFeilds=modelFeilds,queryPerams=queryPeramsX)
#         return list(rDbObj.values())

# class apiRequestManager(magicSerializer):

#     def getValidObject(self,model=None,data={}):
#         modelFeilds = [{"name":f.name,"type":f.__class__.__name__} for f in model._meta.get_fields()]
#         rData = {}
#         for x in modelFeilds:
#             if data.get(x["name"],None) is not None:
#                 if (x["type"]!='ManyToManyField' or (x["type"]=='ManyToManyField' and isinstance(data[x["name"]],list))) and x["name"] != 'id':
#                     rData[x["name"]] = data[x["name"]]
#         return rData
    
#     def getRequestdData(self,request=None,model=None):
#         rxData = []
#         for x in request.data if isinstance(request.data,list) else [request.data]:
#             xcon =  {
#                 'query': x["__SELECT__"] if x.get("__SELECT__",None) is not None else {},
#                 'isNew': x.get("__NEW__",None),
#                 'data':{}
#                 }
#             xcon['data'] = self.getValidObject(model=model,data=x)
#             rxData.append(xcon)
#         return rxData

#     def getDBData(self,model=None,queryFilter={},select_related=[],queryPerams=[]):
#         modelData = model.objects.filter(**queryFilter).select_related(*select_related).values(*queryPerams)
#         return self.serializerObject(dbObj=modelData,model=model,queryPerams=queryPerams)

#     def getLastObject(self,model=None,queryFilter={},select_related=[],queryPerams=[]):
#         queryPeramsX = [x.split('__')[0] for x in queryPerams]
#         modelData = model.objects.filter(**queryFilter).select_related(*select_related).values(*queryPerams).last()
#         manyFeildsX = [{"name":f.name,"type":f.__class__.__name__} for f in model._meta.get_fields()] if model is not None else []
#         qObj = json.loads(json.dumps(self.sanitizeObject(obj=modelData,manyFeilds=[ii["name"] for ii in manyFeildsX]), cls=UUIDEncoder, default=str))
#         manyFeilds = []
#         modelFeilds = []
#         for x in manyFeildsX:
#             if x["type"]=='ManyToManyField':
#                 manyFeilds.append(x["name"])
#             modelFeilds.append(x["name"])
#         return  self.compareAndJoin(obj=[qObj],manyFeilds=manyFeilds,modelFeilds=modelFeilds,queryPerams=queryPeramsX)

#     def isJson(self,myjson):
#         if isinstance(myjson,int):
#             return False
#         try:
#             json.loads(myjson)
#         except ValueError as e:
#             return False
#         return True

#     def read(self,request=None,model=None,select_related=[],collectArguments={},isGet=True):
#         if isGet:
#             query = self.readArguments(
#                 data=request,
#                 readData=collectArguments,
#                 onlyArguments=False
#                 )
#         else:
#             query = self.readPOSTArguments(
#                 data=request,
#                 readData=collectArguments,
#                 onlyArguments=False
#                 )
#         queryData = {keyX:query['data'][keyX] if isinstance(query['data'][keyX],list) or self.isJson(query['data'][keyX]) is False else json.loads(query['data'][keyX]) for keyX in query['data'] }
#         colQ = {}
#         for xd in queryData:
#             xdp = xd.split("__")
#             if len(xdp)> 1 and xdp[-1] in ["from_date","to_date"]:
#                 xdx = "__".join(xdp[:-1])
#                 if colQ.get(xdx,None) is None:
#                     colQ[xdx] = []
#                 colQ[xdx].append(queryData[xdp])
#         for xd in colQ:
#             if len(colQ[xd])==2:
#                 queryData[xd] = [queryData[xd+"__from_date"],queryData[xd+"__to_date"]]
#                 del queryData[xd+"__from_date"]
#                 del queryData[xd+"__to_date"]
                
#         if query["required"]=="__all__":
#             queryPerams = [f.name for f in model._meta.get_fields() if f.__class__.__name__!='ManyToManyField']
#         else:
#             queryPerams = query["required"]
#         return self.getDBData(model=model,queryFilter=queryData,select_related=select_related,queryPerams=queryPerams)

#     def insert(self,model=None,data={}):
#         x = model(**data)
#         return True if x.save() else False

#     def update(self,query={},model=None,select_related=[],data={}):
#         return True if model.objects.filter(**query).select_related(*select_related).update(**data) else False
        
#     def delete_row(self,request=None,model=None,useArguments={}):
#         query = self.readArguments(
#             data=request,
#             readData=useArguments,
#             onlyArguments=False
#             )
#         model_object = model.objects.filter(**query['data']).values('id')
#         if len(list(model_object))>0:
#             model.objects.filter(**query['data']).delete()
#             return True
#         else:
#             return False
class apiRequestManager(object):
    dateFormat='%Y-%m-%d'
    dateTimeFormat='%Y-%m-%dT%H:%M:%S'
    def daysRange(self,from_date='2022-01-04',to_date='2022-02-20'):
        return (datetime.strptime(to_date, self.dateFormat) - datetime.strptime(from_date, self.dateFormat)).days+1
    
    def weeksRange(self,from_date='2022-01-04',to_date='2022-02-20'):
        dt1 = datetime.strptime(from_date, self.dateFormat)
        dt2 = datetime.strptime(to_date, self.dateFormat)
        day1 = (dt1 - timedelta(days=dt1.weekday()))
        day2 = (dt2 - timedelta(days=dt2.weekday()))
        return int(((day2 - day1).days / 7)+1)

    def addDays(self,date='2022-01-04',days=1):
        return datetime.strptime(date, self.dateFormat) + timedelta(days=days)

    def makeKey(self,strd=''): 
        return re.sub("[^A-Za-z0–9]","",strd).lower()
    
    def readParams(self,data={},readData={}):
        rData = {}
        for x in list(readData.keys()):
            if data.get(x,'__blank__') != '__blank__':
                if readData[x]=='split':
                    rData[x] = [stkr if str(stkr).lower() not in ['null','none'] else None  for stkr in str(data[x]).split('|')]
                elif x=='id' or x=='pk':
                    if len(str(data[x])) < 20:
                        rData[x] = int(data[x])
                    else:
                        rData[x] = data[x] 
                else:
                    rData[x] = data[x]
        return rData
    
    def getAllModel(self):
        _all_models = {}
        for app in apps.get_app_configs():
            for _model_ in app.get_models():
                _all_models[_model_.__module__+'.'+_model_.__name__] = _model_
        return _all_models

    def getModelFields(self,model=None):
        _fM = {}
        _pk = model._meta.pk.name
        for f in model._meta.get_fields():
            _fM[f.name] = {
                "type": f.__class__.__name__,
                "field": f,
                "isPK": True if _pk==f.name else False
                }
        return _fM

    def getAllModelWithFields(self):
        _models_ = {}
        for x, y in self.getAllModel().items():
            _models_[x] = {
                'model': y,
                'fields': self.getModelFields(model=y)
                }
        return _models_
    
    def getPkNameFromModel(self,model=None):
        return model._meta.pk.name
    
    def readRequest(self,model=None,request=None,readData={}, prefetch_related=[],select_related=[],exclude={}):
        _all_Feilds = self.getModelFields(model=model)
        if request.headers.get('required',None) is not None:
            reqData = json.loads(request.headers['required'])
            if 'id' not in reqData and 'pk' not in reqData:
                reqData.insert(0,'id')
        else:
            reqData = '__all__'
        _prefetch_related = json.loads(json.dumps(json.loads(request.headers['prefetch_related']) if request.headers.get('prefetch_related',None) is not None else []))
        for _x in prefetch_related:
            if _x not in _prefetch_related:
                _prefetch_related.append(_x)
        _select_related = json.loads(json.dumps(json.loads(request.headers['select_related']) if request.headers.get('select_related',None) is not None else []))
        for _x in select_related:
            if _x not in _select_related:
                _select_related.append(_x)
        _exclude = json.loads(json.dumps(json.loads(request.headers['exclude']) if request.headers.get('exclude',None) is not None else {}))
        for _y,_x in exclude.items():
            if _y not in list(_exclude.keys()):
                _exclude[_y] = _x
        for name, f in _all_Feilds.items():
            if f["type"]=='ManyToManyField':
                if name not in _prefetch_related:
                    _prefetch_related.append(name)
            elif f["type"]=='ForeignKey':
                if name not in _select_related:
                    _select_related.append(name)
        return {
            'GET': json.loads(json.dumps(self.readParams(data=request.query_params,readData=readData))),
            'POST': json.loads(json.dumps(self.readParams(data=request.data,readData=readData))),
            'prefetch_related': json.loads(json.dumps(_prefetch_related)),
            'select_related': json.loads(json.dumps(_select_related)),
            'exclude': json.loads(json.dumps(_exclude)),
            "required": json.loads(json.dumps([name for name, f in _all_Feilds.items() if f["type"]!='ManyToManyField'])) if reqData=='__all__' else json.loads(json.dumps(reqData))
            }
    
    def joinObject(self,model=None,obj=[]):
        _all_Feilds = self.getModelFields(model=model)
        rObj={}
        for itm in obj:
            queryPeramsX = list(itm.keys())
            for _x,x in _all_Feilds.items():
                if _x in queryPeramsX:
                    _rvK = []
                    if isinstance(itm[_x],dict):
                        for _x_ in obj:
                            if _x_.get(_x,'__BLANK__')!='__BLANK__':
                                _rvK.append(_x_[_x])
                        if x["type"]=='ManyToManyField':
                            _pkName = self.getPkNameFromModel(model=x["field"].remote_field.model)
                            _robj = {}
                            for xy in _rvK:
                                if xy is not None:
                                    key = 'id_{id}'.format(id=xy[_pkName])
                                    if _robj.get(key, None) is None:
                                        _robj[key] = []
                                    _robj[key].append(xy)
                            rObj[_x]=[]
                            for xy in list(_robj.values()):
                                _iObj = self.joinObject(model=x["field"].remote_field.model,obj=xy)
                                if _iObj is not None:
                                    rObj[_x].append(_iObj)
                        else:
                            rObj[_x] = self.joinObject(model=x["field"].remote_field.model,obj=_rvK)
                    else:
                        rObj[_x]=itm[_x]
        return None if isinstance(rObj[self.getPkNameFromModel(model=model)],type(None)) else rObj
    
    def patronizeObject(self,obj={},rObj={}):
        ignoreK = []
        for _x,_y in obj.items():
            _key = _x.split('__')
            if len(_key) > 1:
                if _key[0] not in ignoreK:
                    ignoreK.append(_key[0])
                    _rvK = {}
                    for _x_,_y_ in obj.items():
                        _key_ = _x_.split('__')
                        if _key[0]==_key_[0]:
                            _rvK['__'.join(_key_[1:])] = _y_
                    rObj[_key[0]] = self.patronizeObject(obj=_rvK,rObj={})
            else:
                rObj[_key[0]] = _y
        return rObj

    def serializerObject(self,dbObj=[],model=None,queryPerams=[]):
        _pkName = self.getPkNameFromModel(model=model)
        _returnObjects = {}
        _queryPerams = []
        for _qx in queryPerams:
            if _qx.split('__')[0] not in _queryPerams:
                _queryPerams.append(_qx.split('__')[0])
        for xp in list(dbObj):
            if xp is not None:
                key = 'id_{id}'.format(id=xp[_pkName])
                if _returnObjects.get(key, None) is None:
                    _returnObjects[key] = []
                _reData = self.patronizeObject(obj=xp)
                _returnObjects[key].append(json.loads(json.dumps({dk:_reData.pop(dk) for dk in list(_reData.copy().keys()) if dk in _queryPerams}, cls=UUIDEncoder, default=str)))
        return [self.joinObject(obj=_returnObjects.pop(ky),model=model) for ky in list(_returnObjects.copy().keys())]

    def read(self,request=None,model=None,prefetch_related=[],select_related=[],exclude={},collectArguments={},isGet=True):
        query = self.readRequest(
            model=model,
            request=request,
            readData=collectArguments,
            prefetch_related=prefetch_related,
            select_related=select_related,
            exclude=exclude)
        # return query
        return self.getDBData(model=model,queryFilter=query[('GET' if isGet else 'POST')],prefetch_related=query['prefetch_related'],select_related=query['select_related'],exclude=query['exclude'],queryPerams=query["required"])
    
    def getValidObject(self,model=None,data={}):
        modelFeilds = [{"name":f.name,"type":f.__class__.__name__} for f in model._meta.get_fields()]
        rData = {}
        for x in modelFeilds:
            if data.get(x["name"],None) is not None:
                if (x["type"]!='ManyToManyField' or (x["type"]=='ManyToManyField' and isinstance(data[x["name"]],list))) and x["name"] != 'id':
                    rData[x["name"]] = data[x["name"]]
        return rData

    def getRequestdData(self,request=None,model=None):
        rxData = []
        for x in request.data if isinstance(request.data,list) else [request.data]:
            xcon =  {
                'query': x["__SELECT__"] if x.get("__SELECT__",None) is not None else {},
                'customizedHistory': x["__CUSTOMIZED_HISTORY__"] if x.get("__CUSTOMIZED_HISTORY__",None) is not None else {},
                'isNew': x.get("__NEW__",None),
                'data':{}
                }
            xcon['data'] = self.getValidObject(model=model,data=x)
            rxData.append(xcon)
        return rxData

    def autoQuerySanitizer(self,model=None,queryPerams=[],prefetch_related=[],select_related=[],preFix=''):
        ingonreX = []
        _all_Feilds = self.getModelFields(model=model)
        _pkname = self.getPkNameFromModel(model=model)
        if _pkname not in queryPerams:
            queryPerams.append(_pkname)
        _queryPerams = [parm for parm in queryPerams if _all_Feilds.get(parm.split('__')[0],None) is not None]
        _rKey = [parm.split('__')[0] for parm in _queryPerams ]
        for parm in _queryPerams:
            _key_ = parm.split('__')
            if len(_key_) > 1:
                if _key_[0] not in ingonreX:
                    ingonreX.append(_key_[0])
                    _rSelect = []
                    inMulti = False
                    for parm_ in _queryPerams:
                        _key = parm_.split('__')
                        if _key[0]==_key_[0]:
                            _rSelect.append('__'.join(_key[1:]))
                            if len(_key)>2:
                                inMulti = True
                    if len(_rSelect)>0 and _all_Feilds.get(_key_[0],None) is not None:
                        ax = self.autoQuerySanitizer(model=_all_Feilds[_key_[0]]["field"].remote_field.model,queryPerams=_rSelect,prefetch_related=[],select_related=[],preFix=_key_[0])
                        if inMulti:
                            for ay in ax['prefetch_related']:
                                if ay not in prefetch_related:
                                    prefetch_related.append(ay)
                            for ay in ax['select_related']:
                                if ay not in select_related:
                                    select_related.append(ay)
                        for ay in ax['queryPerams']:
                            if _key_[0]+"__"+ay not in _queryPerams:
                                _queryPerams.append(_key_[0]+"__"+ay)
                        for ay in ax['prefetch_related']:
                            if ay not in prefetch_related:
                                prefetch_related.append(ay)
                else:
                    for name, f in _all_Feilds.items():
                        _skey = (preFix+'__' if len(preFix) > 0 else '')+name
                        if f["type"]=='ManyToManyField':
                            if _skey not in prefetch_related and name in _rKey:
                                prefetch_related.append(_skey)
                        elif f["type"]=='ForeignKey':
                            if _skey not in select_related and name in _rKey:
                                select_related.append(_skey)
        return {
            "queryPerams": json.loads(json.dumps(_queryPerams)),
            "prefetch_related": json.loads(json.dumps(prefetch_related)),
            "select_related": json.loads(json.dumps(select_related)),
            }
    
    def getDBData(self,model=None,queryFilter={},prefetch_related=[],select_related=[],exclude={},queryPerams=[]):
        _pkname = self.getPkNameFromModel(model=model)
        if _pkname not in queryPerams:
            queryPerams.append(_pkname)
        r = self.autoQuerySanitizer(model=model,queryPerams=queryPerams,prefetch_related=prefetch_related,select_related=select_related)
        modelData = model.objects.filter(**queryFilter).prefetch_related(*r["prefetch_related"]).select_related(*r["select_related"]).values(*[i for i in r["queryPerams"] if i]).exclude(**exclude)
        return self.serializerObject(dbObj=modelData,model=model,queryPerams=r["queryPerams"] if len(queryPerams)==0 else queryPerams)
    
    def getLastObject(self,model=None,queryFilter={},prefetch_related=[],select_related=[],exclude={},queryPerams=[]):
        _pkname = self.getPkNameFromModel(model=model)
        if _pkname not in queryPerams:
            queryPerams.append(_pkname)
        r = self.autoQuerySanitizer(model=model,queryPerams=queryPerams,prefetch_related=prefetch_related,select_related=select_related)
        modelData = model.objects.filter(**queryFilter).prefetch_related(*r["prefetch_related"]).select_related(*r["select_related"]).values(*[i for i in r["queryPerams"] if i]).exclude(**exclude).last()
        _robj = self.serializerObject(dbObj=[modelData],model=model,queryPerams=r["queryPerams"] if len(queryPerams)==0 else queryPerams)
        return _robj[0] if len(_robj) > 0 else {}
    
    def insert(self,model=None,data={}):
        _data = {}
        for y,x in self.getModelFields(model=model).items():
            if data.get(y,'__BLANK__')!='__BLANK__':
                if x["type"]=='ForeignKey' and (isinstance(data[y],int) or isinstance(data[y],str)):
                    try:
                        _data[y] = x["field"].remote_field.model.objects.get(pk=data[y])
                    except Exception as e:
                        _data[y] = data[y]
                # elif x["type"]=='ManyToManyField':
                else:
                    _data[y] = data[y]
        x = model(**_data)
        return True if x.save() else False

    def update(self,query={},model=None,prefetch_related=[],select_related=[],data={}):
        return True if model.objects.filter(**query).prefetch_related(*prefetch_related).select_related(*select_related).update(**data) else False
        
    def delete_row(self,request=None,model=None,useArguments={}):
        query = self.readRequest(
            model=model,
            request=request,
            readData=useArguments
            )
        model_object = model.objects.filter(**query['GET']).values('id')
        if len(list(model_object))>0:
            model.objects.filter(**query['GET']).delete()
            return True
        else:
            return False
    
    def historyStringReplacer(self,stringData='',fromData={},toData={}):
        _keys = [ x.split('#!')[-1] for x in stringData.split('!#') if len(x.split('#!')[-1]) > 0 ]
        for x in _keys:
            if x.split('.')[0]=="from" and fromData.get(x.split('.')[1],'__BLANK__')!='__BLANK__':
                stringData = stringData.replace('#!from.'+x.split('.')[1]+'!#', str(fromData[x.split('.')[1]]) if x.split('.')[1]!='compiler' else 'Compiler' if fromData[x.split('.')[1]]==2 else 'Non-Compiler')
            if x.split('.')[0]=="to" and toData.get(x.split('.')[1],'__BLANK__')!='__BLANK__':
                stringData = stringData.replace('#!to.'+x.split('.')[1]+'!#', str(toData[x.split('.')[1]]) if x.split('.')[1]!='compiler' else 'Compiler' if toData[x.split('.')[1]]==2 else 'Non-Compiler')
        return stringData

    
    modelHistory = {}

    def getModelHistoryFields(self,model=None,data={},parentField=None,defaultMsgMap={}):
        fields = self.getModelFields(model=model)
        _qF = [self.getPkNameFromModel(model=model)]
        if parentField is not None:
            _qF.append(parentField)
        # _qR = {}
        for name, f in fields.items():
            if f["type"] != 'ManyToManyField' and data.get(name,None) is not None and name in list(defaultMsgMap.keys()):
                if f["type"]=='ForeignKey':
                    _qF.extend(defaultMsgMap[name]["queryFeilds"])
                else:
                    _qF.append(name)
            # elif f["type"] != 'ManyToManyField' and name in list(defaultMsgMap.keys()) and defaultMsgMap[name]["model"] is None and isinstance(defaultMsgMap[name]["queryFeilds"],list):
            #     _qF.extend(defaultMsgMap[name]["queryFeilds"])
        return _qF

    def prepareHistoryLog(self,model=None,targetModel=None,parentField=None,query={},data={},request=None,requestType='POST|PUT|DELETE',defaultMsgMap={},customizedMsgMap={}):
        '''
        model="HistoryModel",
        targetModel="TargetModel",
        parentField=if it's None there is no Parent Model else specify the "TargetModel.field",
        query=query filters used for append the data,
        requestType='POST|PUT|DELETE',
        defaultMsgMap={
            'dataField': {
                "model": None,
                "queryFeilds": ['status__code'],
                "dataType":'DATETIME|STRING|INT|FLOAT',
                "title": "XYZ is updated",
                "message": "XYZ is updated from #!from.status__code!# to #!to.status__code!#"
                }
            },
        customizedMsgMap={
            'dataField': "Own message"
            }
        From these function before updating the changes it will create a log for previous one.
        If model exist in the modelHistory then it will satisfy the condition and the requested data and query are passed in modelData.
        history log is created.

        '''
        if self.modelHistory.get(model.__name__,None) is None:
            self.modelHistory[model.__name__] = {}
        _data_ = data if data else request.data
        _qF = self.getModelHistoryFields(model=targetModel,data=_data_,parentField=parentField,defaultMsgMap=defaultMsgMap)
        modelData = list(targetModel.objects.filter(**query).values(*_qF))
        self.modelHistory[model.__name__] = json.loads(json.dumps(modelData[0], default=str)) if len(modelData) > 0 else None
        if self.modelHistory[model.__name__] is not None and requestType=='DELETE':
            _pk = self.modelHistory[model.__name__][self.getPkNameFromModel(model=targetModel)]
            self.update(query={'target__pk':_pk},model=model,data={
                'target':None
                })
        return True if self.modelHistory[model.__name__] is not None else False
    
    def createHistoryLog(self,model=None,targetModel=None,parentModel=None,parentField=None,query={},data={},request=None,requestType='POST|PUT|DELETE',defaultMsgMap={},customizedMsgMap={},employeeModel=None):
        '''
        model="HistoryModel",
        targetModel="TargetModel",
        parentModel="parentModel",
        parentField=if it's None there is no Parent Model else specify the "TargetModel.field",
        query=query filters used for append the data,
        data={ "status": 1 }
        request=request,
        requestType='POST|PUT|DELETE',
        defaultMsgMap={
            'dataField': {
                "model": None,
                "queryFeilds": ['status__code'],
                "dataType":'DATETIME|STRING|INT|FLOAT',
                "title": "XYZ is updated",
                "message": "XYZ is updated from #!from.status__code!# to #!to.status__code!#"
                }
            },
        customizedMsgMap={
            'dataField': "Own message"
            },
        employeeModel=Employee

        From these function we are creating the log. If requestType = 'POST','PUT' and  modelData index is greater than [0] it will take
        modelData. If requestType = "DELETE" it will delete the log...


        '''
        if self.modelHistory.get(model.__name__,None) is None:
            self.modelHistory[model.__name__] = {}
        if requestType in ['POST','PUT']:
            _data_ = data if data else request.data
            _qF = self.getModelHistoryFields(model=targetModel,data=_data_,parentField=parentField,defaultMsgMap=defaultMsgMap)
            modelData = list(targetModel.objects.filter(**query).values(*_qF))
            modelData = json.loads(json.dumps(modelData[0], default=str)) if len(modelData) > 0 else None
            if requestType=='POST':
                self.modelHistory[model.__name__] = modelData
            for name, f in _data_.items():
                if defaultMsgMap.get(name,None) is not None:
                    if requestType=='PUT':
                        _isDiff = False
                        if defaultMsgMap[name].get("model",None) is not None:
                            _pkname = self.getPkNameFromModel(model=defaultMsgMap[name]["model"])
                            _isDiff = True if self.modelHistory[model.__name__][name+"__"+_pkname]!=modelData[name+"__"+_pkname] else False
                        else:
                            _isDiff = True if self.modelHistory[model.__name__][name]!=modelData[name] else False
                    else:
                        _isDiff = True
                    if _isDiff:
                        pkname = self.getPkNameFromModel(model=targetModel)
                        _histNew = {
                            'target': targetModel.objects.get(pk=modelData[pkname]),
                            "dataField":name,
                            "requestType":requestType,
                            "title": defaultMsgMap[name]["title"], 
                            "fromData": str(self.modelHistory[model.__name__][name+'__'+ self.getPkNameFromModel(model=defaultMsgMap[name]["model"])] if defaultMsgMap[name].get("model",None) is not None else self.modelHistory[model.__name__][name]), 
                            "toData": str(modelData[name+'__'+ self.getPkNameFromModel(model=defaultMsgMap[name]["model"])] if defaultMsgMap[name].get("model",None) is not None else modelData[name]),
                            "message": self.historyStringReplacer(stringData=defaultMsgMap[name]["message"],fromData=self.modelHistory[model.__name__],toData=modelData)+ ((', '+customizedMsgMap[name]) if customizedMsgMap.get(name,'__BLANK__')!='__BLANK__' else ''), 
                            "who": employeeModel.objects.get(pk=request.user.employee.id),
                            }
                        if parentField is not None and parentModel is not None:
                            _histNew['parent_target'] = parentModel.objects.get(pk=modelData[parentField])
                        model.objects.create(**_histNew)
            return True
        elif requestType=='DELETE':
            name = list(data.keys())[0]
            pkname = self.getPkNameFromModel(model=targetModel)
            _histNew = {
                "dataField":pkname,
                "requestType":requestType,
                "title": defaultMsgMap[name]["title"], 
                "fromData": 'N/A', 
                "toData": 'N/A',
                "message": self.historyStringReplacer(stringData=defaultMsgMap[name]["message"],fromData=self.modelHistory[model.__name__],toData=self.modelHistory[model.__name__])+ ((', '+customizedMsgMap[name]) if customizedMsgMap.get(name,'__BLANK__')!='__BLANK__' else ''), 
                "who": employeeModel.objects.get(pk=request.user.employee.id),
                }
            if parentField is not None and parentModel is not None:
                _histNew['parent_target'] = parentModel.objects.get(pk=self.modelHistory[model.__name__][parentField])
            model.objects.create(**_histNew)
            return True
        return False