
## User Administration

This is a Django app to manage users and their bank accounts. It is a completely based on the Django Admin.

### Quick Setup
1. Open a terminal and clone the repository 
```bash
git clone https://github.com/criped/User-Administration.git
```
2.	Build the docker images. It will create a Postgres container a Python container and will install all the required packages 
sudo docker-compose build
```bash
sudo docker-compose build
```
3.	Create the tables needed for the project:
```bash
sudo docker-compose run web python manage.py makemigrations
sudo docker-compose run web python manage.py migrate
```
4.	Create a superuser to start using the app:
```bash
sudo docker-compose run web python manage.py createsuperuser
```
5.	Launch the app:
```bash
sudo docker-compose up
```
It is now available on localhost:8000. To stop it: Ctrl+C or, more elegantly: 
```bash
sudo docker-compose down
```
So far, we have a superuser to manage all the ins and outs of the app. The rest of users logging via Google+ does not have any permissions. 
Head to Administrators Configuration section to continue.  

### Administrators Configuration

Let’s now create a Group for the Administrators and grant it the permissions we want them to have.

- Log in using the superuser account and, once on the main page, click on Group. Let’s call it Administrators.
- Grant add, edit and delete permissions on “My User” table, as shown below.
- Save it and go back to the main page. 

Now, we just need to include the administrators users in the Administrators group. To do so, go to the main page, click on User. You will find all the existing users currently and edit them by pressing on their username.

Note that you need to have previously logged in with your google account to find your google user.

After including the administrators in the Administrator group, they will be able to manage users of “My User” table.  


