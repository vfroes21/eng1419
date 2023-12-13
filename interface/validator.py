from serial import Serial

from pymongo import MongoClient
import database

from threading import Thread
from time import sleep


# serial config 
serial = Serial("COM5", baudrate=9600)

# connecting to db
connection_str = database.get_string()
client = MongoClient(connection_str)

db = client["moradores"]
collection = db["casa1"]

def thread_serial():
            # this reads the tag id
            while True:
                txt = serial.readline().decode().strip()
                
                if txt != "":
                    if txt.startswith("In hex:"):
                        print(txt[8:].strip())

                        busca = {"Tag ID": txt[8:].strip()}

                        # first step: check if Tag ID exists
                        result = collection.find_one(busca)
                        if result:
                              print("Found matching Tag ID")

                              # verificar se precisa de senha, tem cadastrada ou n? tb precisa saber se precisa de reconhecimento facial.
                              # ou precisa de um, ou de outro, ou dos dois. precisa cobrir esses 3 casos

                              # caso precisa de senha
                              if result["Password"]:
                                print(result)
                                print("\nEnviando senha\n")
                                # send cmd to ask for password
                                t = "pass\n"
                                serial.write(t.encode("UTF-8"))

                              # caso precisa de facial

                        else:
                              print("Tag ID not found")

                    elif txt.startswith("Password: "):
                          print(txt)


# star thread that keep reading rfid from serial
thread = Thread(target=thread_serial)
thread.daemon = True
thread.start()

sleep(1)
print("Sending read cmd...")
t = "ler\n"
serial.write(t.encode("UTF-8"))

print("Awaiting RFID...")
while True:
       pass