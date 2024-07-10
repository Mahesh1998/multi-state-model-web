# multi-state-model-web
## Steps to run the project
1. Install python-3.12.3, if not exists.
2. Outside of project directory, create vitual environment.
```bash
python3 -m venv "virtual environment name" --system-site-packages
```
3. Activate the virtual environment.
```bash
source "virtual environment name"/bin/activate
```
4. Once the virtual environment activated successfully, navigate to project directory and install the required packages.
```bash
pip install -r requirements.txt
```
5. Navigate to the below directory to run the project.
```bash
cd prediction_of_charge_delocalization_in_oligomer/ 
```
6. Run the project
```bash
python manage.py runserver
```
Now you should be able to access the web application on [localhost:8000](http://localhost:8000/)


## Steps to run the project using podman

1. Install podman, if not exists.
```bash
sudo apt-get update
sudo apt-get -y install podman
```
2. Navigate to project directory("multi-state-model-web") and build podman image
```bash
podman build -t prediction_of_charge_delocalization_in_oligomer .
```
3. Run podman container using podman image
```bash
podman run -d --name oligomer_container --restart=always -p 55080:8000 prediction_of_charge_delocalization_in_oligomer:latest
```
Now you should be able to access the web application on [localhost:8000](http://localhost:8000/)


## Steps to auto restart the podman container after reboot using systemd.

Pre-requisite: Podman container should be running.

1. change the current working directory to systemd user.
```bash
cd ~/.config/systemd/user/
```
Create if not exists.
```bash
mkdir -p ~/.config/systemd/user/
```
2. Generate "oligomer_application.service" file.
```bash
podman generate systemd --new --name oligomer_container > oligomer_application.service
``` 
3. Reload the systemd deamon
```bash
systemctl --user daemon-reload
``` 
4. Enable oligomer_application.service
```bash
systemctl --user enable oligomer_application.service
``` 
5. Check the status of oligomer_application service. They should be enabled/active.
```bash
systemctl --user status oligomer_application.service
``` 
Now podman container should restart automaticaly upon reboot. If not, then please recheck all the steps.

