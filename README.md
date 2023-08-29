# Automate QoS Adjusment

A collection of Python Code Samples to automate the QoS queue adjustment in Cisco routers running IOS XR. This development includes the use of CISCO EPN-M's APIs to detect drops in the configured priority queues of the routers and CISCO NSO's APIs to send and validate the changes to the network, depending on the thresholds configured by the customer.

![](QoS&FO.png)

## Installation (required)

**Steps:**

The first step is clone the repository
```bash
git clone git@github.com:SDNETMEX/FailOverQoSDevNet.git
```

Go to the project folder
```bash
cd  FailOverQoSDevNet
```

The project consists of two parts, the first one is a websocket that connects to EPN Manager, and receives every alert that this tool generates. To make it run, set up a python2 virtual environment

First you need to have identified the path to the version of python2 installed, example:

```bash
/home/username/opt/python-2.7.15/bin/python
```

Install virtualenv via pip
```bash
pip install virtualenv
```

Navigate to the path where the virtual environment will be created

```bash
cd /path
```

Create the virtual environment
```bash
virtualenv -p /home/username/opt/python-2.7.15/bin/python venv
```

Make sure that the next dependencies are installed using pip
```bash
pip install ws4py requests
```

Now there is all set to execute the websocket that will make the connection to EPN Manager

The second part of the development is a web portal which works as a management tool to control the upper and lower limits of the QoS queues, as well as the rest of the intelligence which is also written in python 3. This app uses flask, between other dependencies, which can be installed using another virtual environment, but this time, using python3, executing the following commands:

First you need to have identified the path to the version of python3 installed, example:

```bash
/home/username/opt/python-3.10/bin/python
```

Install virtualenv via pip
```bash
pip3 install virtualenv
```

Navigate to the path where the virtual environment will be created

```bash
cd /path
```

Create the virtual environment
```bash
virtualenv -p /home/username/opt/python-3.10/bin/python venv
```

Make sure that the next dependencies are installed using pip
```bash
pip3 install -r requirements.txt
```
# RSA Key Generation

Below are the steps to generate an RSA key pair for use in this project.

## Steps to Generate an RSA Key Pair
1. Open a terminal on your system.

2. Run the following command to generate an RSA private key:

```bash
openssl genpkey -algorithm RSA -out private_key.pem
```
3. This private key should exist as a file within the repository. The file path to this private key should be defined in the environment variables.

4. Run the following command to generate the corresponding public key:
```
openssl rsa -pubout -in private_key.pem -out public_key.pem
```
5. This public key should also exist in the repository, and the file path to this public key should be defined in the environment variables.

## Configuration (optional)
The code uses some variables such as IP's for both NSO and EPN manager, as well as the authorization keys to use the REST API's of these tools. You can edit the code to place those variables, but it is recommended to set environment variables, which is the way that the code is designed natively.
Such variables as well as the command to set them, are the following:

This variable is the IP of your EPN Manager
export IP_EPN=x.x.x.x

The authorization key for the use of the EPN Manager API's
export AUTH_EPN=x.x.x.x

The cookie needed for EPN Manager
export COOKIE=x.x.x.x

The username for EPN Manager
export username=x.x.x.x

The password for EPN Manager
export password=x.x.x.x

This variable is the IP of your NSO
export IP_NSO=x.x.x.x

The authorization key for the use of the NSO API's
export AUTH_NSO=x.x.x.x

There is also a script that connects to a device using ssh, which needs the following variables

The username for SSH
export username_ssh=x.x.x.x

The password for SSH
export password_ssh=x.x.x.x

## Usage (required)

Once the python2 virtual environment is all set, it can be executed with the following command

```bash
nohup python rest_alarms.py
```

This will be enough to get most of the development running, because it will detect certain kind of alarms and act accordingly, but there is also the management portal which needs the next dependencies, that are also necessary to run some of the python3 code of the application. To do so, run the next command.

```bash
pip install requirements.txt
```

Then, to make the flask app run, execute the following command

```bash
python3 mainfoqos.py
```

Finally, you can access web development as follows:

```bash
x.x.x.x:80
```
----

## Setting Up Enviroment Variables
This project relies on environment variables to securely store sensitive information, paths, and configuration settings. Environment variables are used to keep confidential data, such as API keys, passwords, and file paths, separate from the codebase. This approach enhances security and makes it easier to manage sensitive information.

Follow these steps to set up the required environment variables:

1. Create a file named .env in the root directory of your project. This file will store the environment variables.

2. Open the .env file in a text editor.

3. Add the necessary environment variables in the format VARIABLE_NAME=value, one per line. For example:
```
secret_key=<KEY>
ip_nso=X.X.X.X
AUTH_NSO=#####
IP_NSO=X.X.X.X
PORT_NSO=X.X.X.X
IP_EPN=X.X.X.X
AUTH_EPN=####
COOKIE=X.X.X.X
USERNAME_SSH=####
PASSWORD_SSH=####
DEFAULT_USERNAME= {Aqui elegir username para las credenciales de acceso}
DEFAULT_PASSWORD= {Aqui elegir password para las credenciales de acceso}
MAIN_PATH= /Path/to/DIR/MAIN_PATH
LOGS_FILES= /Path/to/DIR/LOGS_FILES
JSON_FILES= /Path/to/DIR/JSON_FILES
EXCEL_FOLDER= /Path/to/DIR/EXCEL_FOLDER
MAIL_JSON_FILES= /Path/to/DIR/MAIL_JSON_FILES
PVTKEY= /Path/from/your/DIR/Private_key.pem
```
4. Replace VARIABLE_NAME with the appropriate variable name and value with the corresponding value.

5. Save and close the .env file.

6. In your code, reference the environment variables using the os library (Python) or the appropriate method for your programming language. For example:
```
import os

ip_nso = os.environ['ip_nso']
username = os.environ['DEFAULT_USERNAME']
password = os.environ['DEFAULT_PASSWORD']
```
7. This ensures that sensitive data is loaded securely from the environment variables.

Remember to never commit your .env file to version control systems like Git, as it contains sensitive information. Add .env to your .gitignore file to prevent accidental commits.
By following these steps, you'll be able to easily manage sensitive information, customize configuration settings, and maintain security best practices within your project.
