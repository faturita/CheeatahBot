#coding: latin-1
#!/usr/bin/env python3
#
# Helps to receive commands.

class Surrogator:
    def __init__(self, sock):
        print 'Remote controlling ShinkeyBot'
        self.data = ''
        self.message = ''
        self.controlvalue = 0
        self.command = ''
        self.sock = sock
        self.address = None
        self.keeprunning = True

    def getdata(self):
        return self.data

    def getlengthycommand(self,length):
        self.data = ''
        try:
            # Read from the UDP controller socket non blocking
            self.data, self.address = self.sock.recvfrom(length)
        except Exception as e:
            pass

        return self.data

    def getcommand(self):
        self.data = ''
        try:
            # Read from the UDP controller socket non blocking
            self.data, self.address = self.sock.recvfrom(1)
        except Exception as e:
            pass

    def getmessage(self):
        self.data = ''
        try:
            # Read from the UDP controller socket non blocking
            # The message format is AANNN
            self.message, self.address = self.sock.recvfrom(5)
            self.command = self.message[0]
            self.data = self.message[1]
            self.controlvalue = int(self.message[2:5])
        except Exception as e:
            pass


    def hookme(self):
        while (self.keeprunning):
            nextdata  = ''
            self.getcommand()

            if (self.data == 'X'):
                break

        print 'Stopping surrogate...'
