![Schema](/images/schema.JPG)

# Urban-Sound-Classification-using-AWS-Services
This work is the continuous of "Urban-Sound-Classification-on-Raspberry". In this case I have used as usual Raspebery pi for recording sounds and then saved music  (as txt) in an bucket on S3 of Amazon. Succefully several python's call for run SW on EC2 for classification. 
## Build the project
The building of project follow same procedure of previously work (https://github.com/LuigiRussoDev/Urban-Sound-Classification-on-Raspberry/blob/master/README.md). You need same Python libraries described previously. 

Basically you need first Python 2.7 and download follows library on your EC2:
```bash
boto3, botocore, paramiko
```
```bash
import boto3
import botocore
import paramiko
```

1.  Train the model 
Training your model on workstation "trainModel.py" 
It recommended (in case of trial version of AWS) to train modell using few class because after trained model you'll need "model.data" in EC2 Amazon and the RAM on EC2 could be small. In other case you can train model using all dataset situated in (https://serv.cusp.nyu.edu/projects/urbansounddataset/urbansound8k.html)
2.  Export train model on EC2 in particular ('model.meta', 'model.index', 'checkpoint', 'model.data-00000-of-00001'). 
3.  Export ClassiPi.py on EC2
4.  Run on your Raspberry ClientRasp.py

### Authors 

The first part of work linked previously has beed developed by Gianluca Paolocci and Luigi Russo. 
Second part of this work using integration of AWS Amazon Service (in particular using S3 as Storage of TXT music file recorded and then run of Classification on EC2, has been developed by Luigi Russo)
For more info or info: 
Gianluca Paolocci, University of Naples Parthenope, Science and Techonlogies Departement, Ms.c Applied Computer Science
Luigi Russo, University of Naples Parthenope, Science and Techonlogies Departement, Ms.c Applied Computer Science

### Contacts 

* luigi.russo4@studenti.uniparthenope.it
* gianluca.paolocci@studenti.uniparthenope.it


