import boto3
import botocore
import paramiko
import sounddevice
import numpy as np
import time
import gc

from botocore.client import Config

duration = 0.01  # seconds
sample_rate=44100


ACCESS_KEY_ID = 'AKIAI3GG45ZOXLW5C2XA'
ACCESS_SECRET_KEY = 'Qd+blzLHW8ea+PLCiyl/JPtPAIfuHlJOJDmDgOHP'
BUCKET_NAME = 'prova-bucket2'

while(1):
    
    X = sounddevice.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sounddevice.wait()

    print("Ascolta")
    sounddevice.play(X, sample_rate)
    np.savetxt('miofile.txt', X)



    data = open('miofile.txt', 'rb')


                       
    s3 = boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY,
        config=Config(signature_version='s3v4')
    )

    s3.Bucket(BUCKET_NAME).put_object(Key='miofile.txt', Body=data)




    print ("Done - Caricato. Adesso eseguo il comando su EC2")


    cert = paramiko.RSAKey.from_private_key_file("random.pem")
    c = paramiko.SSHClient()

    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print ("connecting...")
    c.connect( hostname = "ec2-54-200-218-31.us-west-2.compute.amazonaws.com", 
              username = "ec2-user", pkey = cert)
    print ("connected!!!")

    comando_2= 'python ClassiPi.py'

    #salvo prima X in un file 
    stdin_2, stdout_2, stderr_2 = c.exec_command(comando_2)

    #print ('Output del programma: ',stdout_2.readlines())


    # use readline() to read the first line 
    testsite_array = []
    testsite_array = stdout_2.readlines()

    print(testsite_array)

    val = testsite_array[3]

    print("VAL: ",type(val),len(val))
    
    print("Primo valore: ",val[0])
    
    if "0" in val:
        print("trovato")

        

        
    c.close()