from zope.interface import implements
from random import choice
from collective.cdn.core.interfaces import ICDNProvider


class cdn(object):
    
    implements(ICDNProvider)
    
    def __init__(self,hostname=[],port=80,path='', per_registry=False):
        ''' Initialize
        '''
        if not isinstance(hostname,(list,tuple)):
            hostname = [hostname,]
        self.hostname = hostname
        self.port = port
        self.path = path
        self.per_registry = per_registry
    
    def select_host(self,relative_path=''):
        '''>>> obj = cdn()
           >>> obj.hostname = ['foo','bar',]
           >>> obj.port = 80
           >>> obj.path = ''
           >>> hostname = obj.select_host()
           >>> assert (hostname in ['foo', 'bar',])
           >>> hostname = obj.select_host('path/to/somefile.js')
           >>> assert (hostname == 'bar')
           >>> hostname = obj.select_host('path/to/base.css')
           >>> assert (hostname == 'foo')
        '''       
        if not relative_path:
            return choice(self.hostname)
        index = sum([ord(c) for c in relative_path.split('/')[-1]]) % len(self.hostname)
        return self.hostname[index]
    
    def process_url(self,url,relative_path=''):
        '''Given a base url we return an url pointing to 
           the hostname and path informed
           >>> obj = cdn()
           >>> obj.hostname = ['foo','bar',]
           >>> obj.port = 80
           >>> obj.path = ''
           >>> url = obj.process_url('http://nohost/plone/')
           >>> assert (url in ['http://foo/plone/', 'http://bar/plone/',])
           >>> url = obj.process_url('http://nohost:80/plone/')
           >>> assert (url in ['http://foo/plone/','http://bar/plone/'])
           >>> url = obj.process_url('http://nohost:8080/plone/')
           >>> assert (url in ['http://foo/plone/','http://bar/plone/'])
           >>> obj = cdn()
           >>> obj.hostname = ['bar',]
           >>> obj.port = 80
           >>> obj.path = 'somelongpath'
           >>> assert obj.process_url('http://nohost/plone/') == 'http://bar/somelongpath/plone/'
           >>> assert obj.process_url('http://nohost:80/plone/') == 'http://bar/somelongpath/plone/'
           >>> assert obj.process_url('http://nohost/plone/') == 'http://bar/somelongpath/plone/'
           >>> obj = cdn()
           >>> obj.hostname = ['foobar','barfoo',]
           >>> obj.port = 8080
           >>> obj.path = 'shrtpth'
           >>> url = obj.process_url('http://nohost/plone/')
           >>> assert (url in ['http://foobar:8080/shrtpth/plone/','http://barfoo:8080/shrtpth/plone/',])
           >>> url = obj.process_url('http://nohost:80/plone/')
           >>> assert (url in ['http://foobar:8080/shrtpth/plone/','http://barfoo:8080/shrtpth/plone/',])
           >>> url = obj.process_url('http://nohost/plone/')
           >>> assert (url in ['http://foobar:8080/shrtpth/plone/','http://barfoo:8080/shrtpth/plone/',])
        '''
        # splits url parts
        protocol,path = url.split('://')
        path = path.split('/')        
        hostname = self.select_host(relative_path)
        if not self.port in [80,]:
            hostname = '%s:%s' % (hostname, self.port)
        
        path[0] = hostname
        # add path, if supplied
        if self.path:
            path.insert(1,self.path)
        
        # join everything
        path = '/'.join(path)
        url = '%s://%s' % (protocol, path)
        return url