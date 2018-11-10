from tweepy import StreamListener, OAuthHandler, Stream
import socket

consumer_token = "A416DpVGgr6ojpB3ITnnh3ZIe"
consumer_secret = "CJbxJRIxRpmVsGg5d8bxRzpSW0qMuaeRuCRyl2bSI9KISGPo92"
access_token = "379895356-xWon3y2j9ZLPeGbnZOpHUMy7dT5siXTic5BtHIXY"
access_token_secret = "aCFWjzo7J6D5ok7bXCTss8y2NTJeqvKpsbKCi6jovP9a1"


class TweetsListener(StreamListener):

    def __init__(self, csocket):
        super().__init__()
        self.client_socket = csocket

    def on_data(self, data):
        try:
            # Pass the data to spark for processing
            self.client_socket.send(bytes(data, 'UTF-8'))
            return True
        except BrokenPipeError as e:
            print(e)
            print("Exiting program.")
            exit()
        return True

    def on_error(self, status):
        print(status)
        return True


def send_data(c_socket):
    auth = OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    twitter_stream = Stream(auth, TweetsListener(c_socket))
    twitter_stream.filter(track=['earthquake', 'flood', 'tornado'])


if __name__ == "__main__":
    s = socket.socket()  # Create a socket object
    host = "localhost"  # Get local machine name
    port = 5555  # Reserve a port for your service.
    s.bind((host, port))  # Bind to the port

    print("Listening on port: %s" % str(port))

    s.listen(5)  # Now wait for client connection.
    c, addr = s.accept()  # Establish connection with client.

    print("Received request from: " + str(addr))
    try:
        send_data(c)
    except BrokenPipeError or KeyboardInterrupt:
        c.close()
        exit()
    except Exception as e:
        print(e)
        c.close()