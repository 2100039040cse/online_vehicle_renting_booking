Frontend Technologies: HTML,CSS,JS.  
Backend Technologies : Django,Python,MySQL.  
Deployment           : Pythonanywhere. 

Webapplication link-> [2100039040.pythonanywhere.com](https://2100039040.pythonanywhere.com/)  

-> Architected and implemented ’TransportLink Solutions,’ a feature-rich Online Vehicle Booking System using
Django. Enabled Admin, Staff, and Users to effortlessly navigate the platform and achieve optimal function-
ality.  
-> Implemented an advanced feature set for administrators, enabling efficient system management: added vehi-
cles, resulting in streamlined operations and enhanced scalability. Admins gained full oversight of vehicles,
bookings, cancellations, and partnership inquiries via notifications.  
-> For Staff members, the system provides access to view bookings, offer user support, and submit analyses to
the Admin. This ensures efficient communication and support within the system.  
->Users, the end consumers of the service, have a user-friendly interface allowing them to choose locations,
stations, vehicle types, and specific vehicles. They can seamlessly book vehicles, update booking completion
status, cancel bookings, and provide valuable feedback.  
-> To enhance business growth,a Partner Inquiry form is incorporated, facilitating user expression of interest
in partnerships; empowered admins to review and initiate contact with potential partners, driving strategic
business collaborations and expanding the user base.
  
Project Setup  

Djang setup in VS Code YOUTUBE LINK--->>> https://youtu.be/eOVLhM6_6t0

(or)

DOWNLOAD GIT BASH
open new terminal
select gitbash from plus button:

python -m venv environment-name
source environment-name/Scripts/activate
pip freeze
pip install django
pip freeze
django-admin startproject project-name
cd project-name
django-admin startapp appname
ls
python manage.py migrate
python manage.py createsuperuser
username --optional
email --optional
password --give your password
password(again) --give your password
python manage.py runserver
go to your created app and create a new templates folder(html files)
now create a new floder in templates appname
now create a new file in the templates\appname folder and name it
filename.html
go to settings.py file and insert appname in installed apps
('app-name',)
go to url.py file
in second import line afte path add ",include"
(from django.urls import path,include)
in url patterns:
add,
path('',include("app-name.urls")),
go to views.py click on views.py and create a new file called "urls.py"
in the created urls.py file enter the below codes:
from.import views
from django.urls import path

urlpatterns = [  
	path("",views.file-name, name="file-name"),  
	]  
go to views.py
type the below code:

def file-name(request):  
	context={}  
	return render(request, "app-name/file-name.html", context)  
Installation and Setup Guide

MySQL Installation:
Download and install MySQL from the official website: https://dev.mysql.com/downloads/installer/
Follow the installation instructions for your operating system.
During the installation, set a root password for MySQL.
Visual Studio Code Setup:
Download and install Visual Studio Code (VS Code) from: https://code.visualstudio.com/
Open VS Code.
Python Installation:
Download and install Python from the official website: https://www.python.org/downloads/
During installation, make sure to check the option to add Python to your system's PATH.
Django Installation:
Open a terminal in VS Code.
Run the following command to install Django using pip:
Copy code
pip install Django
Common Extensions for Django Development in VS Code:
Python Extension:
Install the "Python" extension by Microsoft from the VS Code marketplace.
This extension provides code analysis, debugging, and other features for Python development.
Django Extension:
Install the "Django" extension by Baptiste Darthenay from the VS Code marketplace.
This extension adds features specifically tailored for Django development, including template language support, code snippets, and more.
Git Extension:
If not already installed, install the "GitLens" extension by Eric Amodio.
This extension enhances Git integration within VS Code, providing inline blame annotations, code lens for Git information, and more.
Database Extension (optional):
Install a database extension like "SQLite" or "MySQL" to interact with your database directly from VS Code.
Search for and install the appropriate extension for your chosen database.
Running the Project:
Clone or download this repository to your local machine.
Navigate to the project directory using the terminal in VS Code.
Set up your MySQL database configurations in your Django project's settings.
Run migrations using the python manage.py migrate command.
Create a superuser using the python manage.py createsuperuser command. Start the development server with python manage.py runserver. Access the project in your web browser at http://127.0.0.1:8000/
This README file provides a basic guide to set up your development environment for a Django project using MySQL, VS Code, and essential VS Code extensions. Remember to customize the instructions according to the specifics of your project.
