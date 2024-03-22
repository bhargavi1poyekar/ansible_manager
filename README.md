# Automating VM Management in Cyber Range  by Bhargavi Poyekar

## Objectives:

1. Attained an in-depth understanding of VMware console access, encompassing activities
such as launching VMs, exploring their configurations, and gaining insights into
directory management.
2. Set up Ansible-based VM Orchestration for VMs in Cyber Range through varied access
methods: command-line interaction, Python-based scripting, and web-based interfaces.
3. Set up and configure a dedicated VM for centralized management, thereby facilitating a
user-friendly VM provisioning and management process, all achieved through Ansible
automation.
4. Created a software repository for further enhancement and improvement.

## Environment:

![](https://i.postimg.cc/MTTKpndS/image.png)

1. Ansible Controller consists of the ansible playbooks which are activated using Python. 

2. Ansible Controller launches Virtual Machines (VM) with the given requirements. 

3. It controls the VM's using SSH. 

4. There will be restricted machines in the environment which cannot be directly accessed through Ansible Controller so they will be accessed through the Jump Host, which acts as a proxy. 

5. The DHCP server assigns the IP-addresses to the newly created machines. 

6. Ansible controller can be used to manage users, files, directories, libraries, and file permissions. 

## Setup for Ansible:

1. Install Ansible

        sudo apt update
        sudo apt install ansible

2. Install the required libraries for ansible

        sudo su
        pip3 install —system pyvmomi 
    => (installs pyvmomi systemwide)
ansible-galaxy collection install community.vmware

3. Install ssh

        sudo apt install openssh-server
        sudo systemctl enable ssh && sudo systemctl start ssh

4. Create ssh private-public key pair

        ssh-keygen -t ed25519 -C "ansible"

    If you want to keep the default name, press enter for the filename when prompted. But, if
you want to give a custom filename, copy the default path and change the filename ->
(/home/username/.ssh/ansible)
Provide a passphrase or leave it blank. This will create a public key ansible.pub and a
private key ansible.

5. Install OpenSSH-server on the virtual machines you want to access using the commands
given in step 2. Then copy the ansible.pub key to each virtual machine you want to
access, by using the command on Ansible Controller.

        ssh-copy-id -i ~/.ssh/ansible.pub username@<virtual-machine-ip>

Try to keep the user on all the virtual machines as crange1 (Optional: If don’t want to use
crange1, you need to make some changes in the project env file.)

## Setup for Project

1. Set hostname.
    
        hostnamectl set-hostname <hostname>

2. Add the hostname with ip address to /etc/hosts file.
Open the file in any editor and add the line below 127.0.0.1:
        
        <your machine ip_address> <hostname>

3. Make sure that you have git setup in the ansible controller machine. Then clone the
project using:
        
        git clone git@github.com:bhargavi1poyekar/ansible_manager.git

4. Go into the directory.
        
        cd ansible_manager

5. Set up your virtual environment.
        
        sudo apt-get install python3-venv
        python3 -m venv <venv_name>
        source <venv_name>/activate/bin

6. Install the required libraries

        python3 -m pip install -r requirements.txt

## Setting Up Ansible Vault for Confidential Credentials:

1. Create the encrypted file ‘secret.yml’

        ansible-vault create secret.yml

2. If you are comfortable with vim editor, you can directly edit it using:

        ansible-vault edit secret.yml

    Otherwise, you can use gedit to edit the document.
        
        ansible-vault decrypt secret.yml
        gedit secret.yml

3. Use the following template:

        —
        vcenter_hostname: “”
        vcenter_datacenter: “”
        vcenter_validate_certs: false
        vcenter_cluster: “”
        vm_state: “powered-on”
        vcenter_username: “”
        vcenter_password: “”
        vm_network1: “”
        vm_network2: “”

    Fill your credentials and save and exit.

4. Encrypt again, if used gedit:

        ansible-vault encrypt secret.yml

5. Now put your ansible-vault password in ‘pass.txt’ file and save it.

        gedit pass.txt

## Run Project
Note: For running all the commands in this section, you have to be inside the main

1. Run Migrations:

        python3 manage.py makemigrations
        python3 manage.py migrate

    This will create db.sqlite3 as discussed above.
2. Create superuser
        
        python3 manage.py createsuperuser
    Add user and password for admin.

3. Collect Static files:
        
        python3 manage.py collectstatic

4. Create a .env file as mentioned above(highlighted in red in file structure) and add this
content to it:

        EMAIL_USER=’<Your gmail id>’
        EMAIL_PASS=’<Your gmail password>’
        BECOME_PASSWORD=’<sudo password for vm’s>’
        IP_RANGE_3072=’<ip address ranges separated by ‘;’>’
        IP_RANGE_4093=’<ip address ranges separated by ‘;’>’
    Eg: 130.85.121.25-130.85.121.50; 130.85.220.12-130.85.220.50

    Also, go to your Gmail account=> manage your google account=> Security=> Allow less
    secure apps=> Turn it on.

5. Now generate the ip addresses according to the ranges by:
        
        python3 generate_ip_address.py

6. Now run the project in localhost
        
        python3 manage.py runserver

    Once the project runs in localhost, we can configure Apache to deploy it.

## Apache Installation and Configuration

1. In the settings.py file highlighted in blue color in the file structure, add the ip address of
your machine in ALLOWED_HOSTS
        
        ALLOWED_HOSTS=[‘<ip_address>’]

2. Install apache2 and wsgi

        sudo apt-get install apache2
        sudo apt-get install libapache2-mod-wsgi-py3

3. Create your .conf file

        cd /etc/apache2/sites-available/
        sudo cp 000-default.conf django.conf

4. Open the django.conf and edit it to the following. 

    (Replace /home/crange1/ with
    /home/<your user> Make changes if necessary)

        <VirtualHost *:80>  

            #Include conf-available/serve-cgi-bin.conf
            
            Alias /static /home/crange1/ansible_manager/static
            <Directory /home/crange1/ansible_manager/static>
                Require all granted
            </Directory>
            
            Alias /media /home/crange1/ansible_manager/media
            <Directory /home/crange1/ansible_manager/media>
                Require all granted
            </Directory>
            <Directory /home/crange1/ansible_manager/ansible_manager>
                <Files wsgi.py>
                    Require all granted
                </Files>
            </Directory>
            WSGIScriptAlias / /home/crange1/ansible_manager/ansible_manager/wsgi.py
            WSGIDaemonProcess django_app python-path=/home/crange1/ansible_manager
            python-home=/home/crange1/ansible_manager/myenv
            WSGIProcessGroup django_app
            WSGIApplicationGroup %{GLOBAL}
        
        </VirtualHost>

    Note: The path in above file are assuming that you have cloned the project in `/home/<user>/` folder. If not, make changes to the paths accordingly.

5. Enable our .conf file.

        sudo a2ensite django
        sudo a2dissite 000-default

6. Change the directory permissions:

        sudo chown :www-data -R ansible_manager/
        sudo chmod 775 -R ansible_manager
        sudo chown www-data:www-data /var/www/

7. Load environment variables:

        sudo nano /etc/apache2/envvars
    Add the following line at the beginning of the file:
        
        export $(cat /path/to/your/project/.env | xargs)

    Save and close the file.
8. Allow http/tcp in ufw.
        
        sudo apt-get install ufw
    (if not already present, it is usually present by default in Ubuntu machines)

        sudo ufw enable
        sudo ufw allow http/tcp
9. Check if the project is visible on your IP address. => https://<ip_addr>

10. Edit the settings.py folder in your project and change DEBUG= False.

** Note: If the website is having any trouble: check the apache error log:
sudo cat /var/log/apache2/error.lo
