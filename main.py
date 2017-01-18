import socketserver
import socket
import threading
import RPi.GPIO as GPIO
import time


class UDPServerHandler(socketserver.BaseRequestHandler):

    def setup(self):
        print("Client connected ", self.client_address)
        super(UDPServerHandler, self).setup()
        self.server.add_client(self)

    def handle(self):
        data = self.request[0].strip().decode()
        socket = self.request[1]
        print(self.client_address[0],' wrote: ', data)
        command, value = str(data).split('|')
        print(command, command.strip(), command == 'steering')
        if command.strip() == 'steering':
            print("steering", self.server.steering, " duty: ", self.server.calculate_steering_duty(value.strip()))
            self.server.steering.ChangeDutyCycle(self.server.calculate_steering_duty(value.strip()))
        socket.sendto(data.encode().upper(), (self.client_address[0], 7777))


class UDPServer(socketserver.ThreadingUDPServer):
    """UDPServer with broadcasting capability"""

    def __init__(self, server_address, request_handler_class):
        """Initializes a ThreadingUDPServer with clients set"""
        print("Server starting at %s:%s..." % (server_address[0], server_address[1]))
        super(UDPServer,self).__init__(server_address, request_handler_class, True)
        self.clients = set()
        GPIO.setmode(GPIO.BCM)
        print("Servo motor is setting up..")
        GPIO.setup(18, GPIO.OUT)
        self.steering = GPIO.PWM(18, 50)
        self.steering.start(5)
        GPIO.setwarnings(False)

        duty = self.calculate_steering_duty(90)
        print("initial duty: ", duty)
        self.steering.ChangeDutyCycle(duty)
        print("Servo motor is ready")
        print("Server started")


    def calculate_steering_duty(self, val):
        return float(val) / 18.0 + 2.5

    def add_client(self, client):
        """Registers a client to clients set"""
        self.clients.add(client)

    def broadcast(self, source, data):
        """Sends data to all clients from the source"""
        for client in self.clients:
            if client is not source:
                client.schedule((source.name, data))

    def remove_client(self, client):
        """Removes clients from the set"""
        self.clients.remove(client)



if __name__ == '__main__':
    HOST, PORT = "192.168.1.1", 7777
    server = UDPServer((HOST,PORT), UDPServerHandler)
    server.serve_forever()
    GPIO.cleanup()
