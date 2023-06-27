# data-oriented rendering framework
from pyquery import PyQuery as pq

class Renderer:
    def __init__(self):
        self.components = {}
    
    def import_components(self, source):
        d = pq(source)
        components = d('component')
        for c in components:
            self.components[c.attrib['name']] = {
                'accepts': c.attrib['accepts'] if 'accepts' in c.attrib else None,
                'content': c.text
            }
        print(self.components)