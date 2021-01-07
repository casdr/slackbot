def config(bot):
    return {
        'commands': ['whoami', 'perm-add', 'perm-del', 'meet'],
        'events': [],
        'help': 'control users'
    }

def run(bot, event):
    user_id = None
    for block in event.blocks:
        for el in block['elements']:
            for element in el['elements']:
                if element['type'] == 'user':
                    user_id = element['user_id']
    if event.command == 'meet':
        if not event.user.has_perm(['user']):
            return event.reply(text="you don't have permissions for that")
        if not user_id:
            return event.reply(text="what user?")
        if not bot.users.meet(user_id):
            return event.reply(text="user '%s' already exists" % user_id)
        return event.reply(text="user '%s' added" % user_id)

    if event.command == 'perm-add':
        if not event.user.has_perm(['admin']):
            return event.reply(text="you don't have permissions for that")
        if not user_id or len(event.args) < 3:
            return event.reply(text="usage: perm-add <user> <perm>")
        if not bot.users.add_perm(user_id, event.args[2]):
            return event.reply(text="this user already has this perm")
        return event.reply(text="perm added")
    
    if event.command == 'perm-del':
        if not event.user.has_perm(['admin']):
            return event.reply(text="you don't have permissions for that")
        if not user_id or len(event.args) < 3:
            return event.reply(text="usage: perm-del <user> <perm>")
        if not bot.users.del_perm(user_id, event.args[2]):
            return event.reply(text="this user doesn't have this perm")
        return event.reply(text="perm removed")

    if event.command == 'whoami':
        if not event.user.is_registered:
            return event.reply(text="I don't know you :(")
        else:
            return event.reply(text="id: %s, perms: %s" % (event.user.id, ",".join(event.user.perms)))