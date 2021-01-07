from .data import DataManager

class UserManager:
    def __init__(self, bot):
        self.bot = bot
        self.data = DataManager(self.bot, 'users', {"users": {}})
        self.users = self.data.data['users']
    
    def save(self):
        self.data.set({"users": self.users})

    def get_user(self, user_id):
        if user_id in self.users:
            return User(self, self.users[user_id])
        
        return User(self, {
            "user_id": user_id,
            "perms": [],
            "is_registered": False
        })
    
    def meet(self, user_id):
        if isinstance(user_id, dict):
            user_id = user_id['user_id']
        if user_id in self.users:
            return False
        
        self.users[user_id] = {
            "user_id": user_id,
            "perms": ['user'],
            "is_registered": True
        }
        
        self.save()
        return User(self, self.users[user_id])

    def add_perm(self, user_id, perm):
        user = self.get_user(user_id)
        if perm in user.perms:
            return False
        self.users[user_id]['perms'].append(perm)
        self.save()
        return True
    
    def del_perm(self, user_id, perm):
        user = self.get_user(user_id)
        if perm not in user.perms:
            return False
        self.users[user_id]['perms'].remove(perm)
        self.save()
        return True

    def is_registered(self, user_id):
        return self.get_user(user_id).is_registered
    
    def has_perm(self, user_id, perms):
        if not isinstance(perms, list):
            perms = [perms]
        for perm in perms:
            user = self.get_user(user_id)
            if perm in user.perms or 'admin' in user.perms:
                return True
        return False

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
