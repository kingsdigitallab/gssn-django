# gssn-django

German Screen Studies Network website

## Release 0.2

Minor release

* Changed anchor text styling to make links more visible
* Changed event filter name from Symposium to Symposia
* Changed event category url from Symposiums to Symposia
* Fixed link to membership page in the sidebar widget

## Release 0.1

First stable release deployed.

* Homepage
  - Carousel
  - Dynamic content
  - Twitter feeds
  - Static content list
* Page types with relevant sidebars
* Sidebars with dynamic content
* Search
* Custom Wagtail set up

## Getting started - Set up locally 

1. Clone this repository: `git clone git@github.com:kingsdigitallab/gssn-django.git`
2. Add a `local.py` file in `gssn-django/gssn/settings/`
3. Run `bower install bower.json` to install the dependencies
4. Start the virtual environment: `vagrant up` and then `vagrant ssh`
5. Install the requirements: `pip install -U -r requirements.txt`
6. Start elasticsearch: `sudo service elasticsearch start`
7. Run migrations if necessary: `./manage.py migrate`
8. Start the server: `./manage.py runserver 0:8000`

You can now access the site locally at: `http://localhost:8000/`

## Wagtail
In order to access Wagtail, you might need to create a superuser account.
To do so, run this in the virtual environment: `./manage.py createsuperuser` and follow the instructions in the terminal.

Last few steps to actually get the site running:

1. Access Wagtail at `http://localhost:8000/wagtail`
2. Create a page of type _Homepage_ and publish it
3. Change the root page to point to the Homepage:
	* Settings > Sites
	* Click on _localhost_
	* Change the root page selecting your Homepage
	* Save

Every page you create, of whatever type, should be a child page of Homepage.