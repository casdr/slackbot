class User:
    def __init__(self, manager, data):
        self.manager = manager
        self.id = data['user_id']
        self.perms = data['perms']
        self.is_registered = data['is_registered']

    def has_perm(self, perms):
        if not isinstance(perms, list):
            perms = [perms]
        for perm in perms:
            if perm in self.perms or 'admin' in self.perms:
                return True
        return False

    def add_perm(self, perm):
        if perm in self.perms:
            return False
        self.manager.add_perm(self.id, perm)
        return True

    def del_perm(self, perm):
        if perm not in self.perms:
            return False
        self.manager.del_perm(self.id, perm)
        return True
