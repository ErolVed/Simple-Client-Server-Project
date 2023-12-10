from pecan import expose, abort
import json
from pecanproject import server,ClientInfo as ci
from sqlalchemy.orm import sessionmaker

ci.Base.metadata.create_all(ci.engine)

class ClientController(object):
    def __init__(self, id_, CLIENTS):
      self.id_ = id_
      self.CLIENTS = CLIENTS
      assert self.client

    @property
    def client(self):
      if self.id_ in self.CLIENTS:
        return dict(Name=self.id_, properties=self.CLIENTS[self.id_])
      abort(404)

    @expose(generic=True, template='json')
    def index(self):
      return self.client

class RootController(object):
    
    def __init__(self):
      self.CLIENTS = {}

    @expose(generic=True) #READS
    def index(self):
      return str(self.CLIENTS)

    @index.when(method='POST', template='json') #CREATE
    def index_POST(self, **kw):
      id_ = 'client'+ kw['id']
      self.CLIENTS[id_]= {"id": 1,"ip": "5.5.5.5","cpu": "5","ram": "5","disk": "5","uptime": "55:55:55:55\n"}
      for property in kw:
        if(property == 'id'):
          pass
        elif property in self.CLIENTS[id_]:
          self.CLIENTS[id_][property]= kw[property]
      return self.CLIENTS

    @index.when(method='PUT', template='json') #UPDATE
    def index_PUT(self, **kw):
      id_ = 'client'+ kw['id']
      for property in kw:
        if(property == 'id'):
          pass
        elif property in self.CLIENTS[id_]:
          self.CLIENTS[id_][property]= kw[property]
      return self.CLIENTS

    @index.when(method='DELETE', template='json') #DELETE
    def index_DELETE(self,id_):
        del self.CLIENTS['client'+str(id_)]
        return self.CLIENTS

    @expose()
    def rescan(self):
        server.run_server()
        LocalSession = sessionmaker(bind=ci.engine, autoflush= False)
        session = LocalSession()
        json_data = {}
        for obj in session.query(ci.ClientInfo).all():
            json_data["client"+str(obj.id)]={
            "id" : obj.id,
            "ip" : obj.ip,
            "cpu" : obj.cpu,
            "ram" : obj.ram,
            "disk" : obj.disk,
            "uptime" : obj.upTime
        }
        self.CLIENTS = json_data
        return str(self.CLIENTS)
    
    @expose()
    def _lookup(self, id_,*remainder):
      return ClientController('client'+str(id_),self.CLIENTS),remainder
