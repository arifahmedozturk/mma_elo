class FighterQueue:
    def __init__(self):
        self.expanded_urls = set()
        self.unexpanded_urls = set()
    
    def insert(self, url):
        if url in self.expanded_urls or url in self.unexpanded_urls:
            return
        
        self.unexpanded_urls.add(url)
    
    def pop(self):
        if len(self.unexpanded_urls) == 0:
            return None

        url = self.unexpanded_urls.pop()
        self.expanded_urls.add(url)
        return url