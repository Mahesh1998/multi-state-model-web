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
podman run -d --name oligomer_container --restart=always -p 8000:8000 prediction_of_charge_delocalization_in_oligomer:latest
```
podman run -d --name oligomer_container --restart=always -p 8000:8000 prediction_of_charge_delocalization_in_oligomer:latest


