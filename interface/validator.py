from serial import Serial

from pymongo import MongoClient
import database

from threading import Thread
from time import sleep

# ********* import from Lucca **************
from Recognition import *
# ******************************************

# serial config 
serial = Serial("COM39", baudrate=9600,timeout=1)

# connecting to db
connection_str = database.get_string()
client = MongoClient(connection_str)

db = client["moradores"]
collection = db["casa1"]

only_pass = False
only_facial = False
both = False

# global result of db query
result = None

fr = FaceRecognition()

def thread_serial():
            global result
            global only_pass
            global both
            global only_facial
            global fr
            # this reads the tag id
            while True:
                txt = serial.readline().decode().strip()
    
                if txt != "":
                    # received a tag
                    if txt.startswith("RFID:"):
                        print(txt[5:].strip())

                        busca = {"Tag ID": txt[5:].strip()}

                        # first step: check if Tag ID exists
                        result = collection.find_one(busca)
                        print(result)
                        if result:
                              print("Found matching Tag ID")
                       
                              # caso precisa dos 2
                              if result["Password"] != "" and result["Picture File"] != "":
                                    # send cmd to ask for both
                                    print("This resident need to validate facial and password")
                                    both = True
                                    fr.find_face(result["Picture File"])
                                    print("Sending both command...")
                                    t = "RFID:senhafacial"
                                    serial.write(t.encode("UTF-8"))
                             

                              # caso precisa de senha
                              elif result["Password"] != "":
                                print("This resident only needs password")
                                only_pass = True

                                # send cmd to ask for password
                                print("Sending password command...")
                                t = "RFID:senha\n"
                                serial.write(t.encode("UTF-8"))
                                
                                print("Awaiting password...")

                              # caso precisa de facial
                              elif result["Picture File"] != "":
                                    # send cmd to ask for facial recognition
                                    print("This resident only needs facial recognition")
                                    only_facial = True
                                    
                                    print("Sending facial command...")
                                    
                                    print(result["Picture File"])
                                    fr.find_face(result["Picture File"])
                                    t = "RFID:facial"
                                    serial.write(t.encode("UTF-8"))
                                    
                                    print("Awaiting facial recognition...")


                        else:
                              print("Tag ID not found")
                              # at this point, send cmd to arduino show tag id not found on display
                              t = "RFID:invalido"
                              serial.write(t.encode("UTF-8"))
                    
                    # case where i receive a password from arduino
                    elif txt.startswith("senha:"):
                              # only does something if received a tag first (so these variables are true)
                          
                              # case where password matches: resident is allowed to enter house
                              if result["Password"] == txt[6:]:
                                    print("Password matches. Resident is allowed")
                                    t = "senha:valida"
                                    serial.write(t.encode("UTF-8"))
                              else:
                                    # not allowed to enter
                                    print("Password doesnt match. Resident is not allowed")
                                    t = "senha:invalida"
                                    serial.write(t.encode("UTF-8"))
                          
                                
                    
                    # case where i receive facial recognition data i.e recognized someone or not
                    
                elif fr.achou != None:
                        if fr.achou == True:
                            print("Facial recognition matches. Resident is allowed")
                            t = "face:valido"
                            serial.write(t.encode("UTF-8"))
                            fr.achou = None
                        
                        else:
                            print("Facial recognition doesnt match. Resident is not allowed")
                            t = "face:invalido"
                            serial.write(t.encode("UTF-8"))
                            fr.achou = None



# start thread that keep reading rfid from serial
thread = Thread(target=thread_serial)
thread.daemon = True
thread.start()

sleep(1)

fr.run_recognition()