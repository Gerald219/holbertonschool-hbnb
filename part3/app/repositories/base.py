class BaseRepository:
    
    def add(self, obj):
        raise NotImplementedError

    
    def get(self, obj_id):
        raise NotImplementedError

    
    def list(self):
        raise NotImplementedError

    
    def update(self, obj_id, data):
        raise NotImplementedError


    def delete(self, obj_id):
        raise NotImplementedError

