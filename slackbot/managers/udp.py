import socket
import threading

class UdpManager:
    def __init__(self, bot, event_handler):
        self.bot = bot
        self.udp_open = False
        self.udp_socket = None
        self.udp_thread = None
        self.event_handler = event_handler

        self.open()
    
    def open(self):
        if self.udp_open:
            self.udp_socket.close()
            self.udp_open = False
            self.udp_thread.kill()
    
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bot.log.info('binding udp socket on %s:%s' % (self.bot.state['udp_ip'], self.bot.state['udp_port']))
        self.udp_socket.bind((self.bot.state['udp_ip'], self.bot.state['udp_port']))
        self.udp_open = True

        self.udp_thread = UdpThread(self.bot, self.udp_socket, self.event_handler)
        self.udp_thread.start()

class UdpThread(threading.Thread):
    def __init__(self, bot, sock, event_handler):
        super().__init__()
        self.bot = bot
        self.socket = sock
        self.killed = False
        self.event_handler = event_handler
    
    def run(self):
        self.bot.log.info('starting udp loop')
        while not self.killed:
            try:
                data, addr = self.socket.recvfrom(1024)
                self.event_handler(data.decode('utf-8').rstrip('\n'))
            except:
                pass
        self.bot.log.info('udp loop killed')
    
    def kill(self):
        self.killed = True