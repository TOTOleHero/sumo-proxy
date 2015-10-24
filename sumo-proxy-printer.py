import threading
import SocketServer


def repr_bytes(bytes, maximum=25):
    """ Nicer data printing.
    """
    return ''.join('\\x{:02x}'.format(ord(c)) for c in bytes[:maximum])


if __name__ == '__main__':
    # Patch to recieve video packets (+ direction indicator)
    SocketServer.UDPServer.max_packet_size = 65000

    # Create server
    class Handler(SocketServer.BaseRequestHandler):

        def handle(self):
            data = self.request[0]

            # From client to sumo
            if data[0] == '>':
                print '> {}'.format(repr_bytes(data[1:]))
            # From sumo to client
            elif data[0] == '<':
                print '< {}'.format(repr_bytes(data[1:]))

    server = SocketServer.UDPServer(('127.0.0.1', 65432), Handler)
    t = threading.Thread(target=server.serve_forever)
    t.start()
    t.join()
