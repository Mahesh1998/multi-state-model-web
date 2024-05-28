# multi-state-model-web
## Steps to run the project
1. Install python-3.12.3, if not exists.
2. Outside of project directory create vitual environment.
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
5. Run the project
```bash
python manage.py runserver
```
Now you should be able to access the web application on [localhost:8000](http://localhost:8000/)
