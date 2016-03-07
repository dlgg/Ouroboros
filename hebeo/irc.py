#!/usr/bin/env python
# -*- coding: utf-8 -*-

print("Loading class Irc :", end=" ")

import socket, sys, select, time
from . import tools
from colorama import Fore, Style

class Irc(object):

    def __init__(self, o, s):
        self.name = s['name']
        self.host = s['host']
        self.port = int(s['port'])
        self.nick = s['nick']
        self.ident = s['ident']
        self.realname = s['realname']
        self.chans = s['chans'].split()
        self.adminchan = o['adminchan']
        self.encoding = o['encoding']

    def status(self):
        print(Fore.CYAN + "Object is configured as follow :")
        print()
        print(Fore.CYAN + "Network name           : " + Fore.RESET + "{0}".format(self.name))
        print(Fore.CYAN + "Host:port              : " + Fore.RESET + "{0}:{1}".format(self.host, self.port))
        print(Fore.CYAN + "Identification         : " + Fore.RESET + "{0}!{1}@host:{2}".format(self.nick, self.ident, self.realname))
        print(Fore.CYAN + "Channels               : " + Fore.RESET + "{0}".format(self.chans))
        print(Fore.CYAN + "Administrative channel : " + Fore.RESET + "{0}".format(self.adminchan))
        print(Fore.CYAN + "Encoding               : " + Fore.RESET + "{0}".format(self.encoding))

    def connect(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.settimeout(180)
        try:
            self.s.connect((self.host, self.port))
        except socket.error:
            tools.prtErr("Connection failed.")
        except socket.timeout:
            tools.prtErr("Connection has timed out.")
        self._boot()
        self.flag = True;
        while self.flag:
            try:
                input,output,exception = select.select([0, self.s], [], [])
                for i in input:
                    if i == self.s:
                        try:
                            for line in self.s.makefile(mode='r', newline='\r\n', encoding=self.encoding):
                                if not line:
                                    tools.prtErr('Shutting down')
                                    #sys.exit()
                                else:
                                    tools.debug(Fore.MAGENTA + "S " + line)
                                    self._parse(line)
                        except KeyboardInterrupt:
                            tools.prtErr("Interrupted.")
                            self._cmdQuit("")
                        except UnicodeDecodeError:
                            pass
                        except (ConnectionResetError, BrokenPipeError):
                            self.flag = False;
                            pass
                        except:
                            tools.prtErr('Problem with the reading !!' + str(sys.exc_info()))
                            continue
            except KeyboardInterrupt:
                tools.prtErr("Interrupted.")
                self._cmdQuit("")
                break

    def _boot(self):
        self.send("USER {0} 0 0 :{1}".format(self.ident, self.realname))
        self.send("NICK {0}".format(self.nick))

    def send(self, msg):
        toSend = msg + '\r\n'
        tools.debug(Fore.CYAN + Style.BRIGHT + "C " + msg)
        self.s.send(toSend.encode(self.encoding))

    def _parse(self, msg):
        msgs = msg.split()
        raw = { 'PING':self._rawPing}
        raw.get(msgs[0], self._cmdUnknown)(msg)
        cmd = { 'PRIVMSG':self._privmsg, 'NOTICE':self._notice,
                '005':self._raw005, 332:self._raw332, 333:self._raw333, 353:self._raw353, 366:self._raw366, 372:self._raw372, 375:self._raw375, 376:self._raw376 }
        cmd.get(msgs[1], self._cmdUnknown)(msg)

    def _privmsg(self, msg):
        msgs = msg.split()
        fullnick = msgs[0][1:]
        nick = fullnick.split("!")[0]
        #ident = fullnick.split("!")[1].split("@")[0]
        #hostname = fullnick.split("@")[1]
        dest = msgs[2]
        if dest.lower() == self.adminchan.lower():
            tools.debug(msgs[3][1:])
            cmd = { '%join': self._cmdJoin, '%part':self._cmdPart, '%quit':self._cmdQuit }
            try:
                cmd.get(msgs[3][1:])(msg)
            except:
                #self.send("PRIVMSG {0} :Message reçu de {1} pour {2} > {3}".format(adminchan, nick, dest, ' '.join(msgs[3:])[1:]))
                pass
        else:
            self.send("PRIVMSG {0} :Message reçu de {1} pour {2} > {3}".format(self.adminchan, nick, dest, ' '.join(msgs[3:])[1:]))

    def _notice(self, msg):
        msgs = msg.split()
        print("Notice reçue : {0}".format(msgs[2:]))

    def _cmdUnknown(self, msg):
        "Affiche en console toutes les commandes inconnues"
        #print("Commande inconnue :", msg)

    def _rawPing(self, msg):
        msgs = msg.split()
        srv = msgs[1]
        self.send("PONG {0}".format(srv))

    def _raw005(self, msg):
        self.send("JOIN {0}".format(self.adminchan))
        self.send("JOIN {0}".format(",".join(self.chans)))

    def _raw332(self, msg):
        "Topic content"
        pass

    def _raw333(self, msg):
        "Topic setter"
        pass

    def _raw353(self, msg):
        "/Names content"
        pass

    def _raw366(self, msg):
        "End of /names"
        pass

    def _raw372(self, msg):
        "MOTD Content"
        pass

    def _raw375(self, msg):
        "MOTD Start"
        pass
    def _raw372(self, msg):
        "MOTD Content"
        pass
    def _raw376(self, msg):
        "MOTD End"
        pass

    def _cmdJoin(self, msg):
        msgs = msg.split()
        self.send("JOIN {0}".format(msgs[4]))

    def _cmdPart(self, msg):
        msgs = msg.split()
        if msgs[4].lower() != self.adminchan.lower():
            self.send("PART {0} :On ne veut plus de moi ici :'(".format(msgs[4]))
        else:
            self.send("PRIVMSG {0} :Je ne peux pas partir de {0}".format(self.adminchan))

    def _cmdQuit(self, msg):
        self.send("QUIT :On ne veut plus de moi ici :'(")
        time.sleep(2)
        self.flag = False
        self.s.close()

print("\033[92mOK\033[0m")
