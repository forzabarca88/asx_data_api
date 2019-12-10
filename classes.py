class json_response(object):
    '''
    Represents the response from this api
    Args:
        status:
        links:
        data:
    '''
    status = None
    links = None
    data = None

    def __init__(self, status : int, links : list, data : dict) -> None:
        self.status = status
        self.links = links
        self.data = data

    @property
    def value(self) -> dict:
        return {
        "data": self.data,
        "status": self.status,
        "links": self.links
        }

    def __repr__(self) -> str:
        return self.value



class link(object):
    '''
    Represents an instance of link from a json_response
    '''
    rel = None
    href = None
    method = None
    def __init__(self, rel : str, href : str, method : str = 'GET') -> None:
        self.rel = rel
        self.href = href
        self.method = method

    @property
    def value(self) -> dict:
        return {
            "rel": self.rel, 
            "href": self.href, 
            "method": self.method
        }

    def __repr__(self) -> str:
        return self.value
