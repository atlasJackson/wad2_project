# **WAD2 Project:** Football Fives Finder

### Developed by:
> Gordon Daffurn 0801676d@student.gla.ac.uk
Hangil Ko 2286274k@student.gla.ac.uk
Nicola Mössner 2268685m@student.gla.ac.uk

#### Project URLs
* Github URL: https://github.com/atlasJackson/wad2_project
* PythonAnywhere URL: http://f5f.pythonanywhere.com/
---
#### IMPORTANT INFORMATION

1. Requirements file is included. Create a new virtual environment with mkvirtualenv, then install requirements from the given file with

```sh
$ pip install -r requirements.txt
```
2. **Google Maps Javascript API key**

Before running the app, you require an API key to generate a map for the fives/\<game> and fives/about_us pages.
In the project configuration directory (the wad2_project directory nested inside the wad2_project directory), is the file context_processors.py. Within this file is one method: api_key_processor. This passes the api key to the context for every template - line 8 assigns the api key from the settings file to the variable api_key. You must include the file api_google.txt, which solely contains your API key, inside this directory. To obtain an api key, follow the link below:
https://developers.google.com/maps/documentation/javascript/get-api-key

3. **Unit Tests**

The unit tests have been split into separate files, located in wad_project/fives/tests. To run coverage, use the following command:
```sh
$ coverage run manage.py test fives.tests
```

---
#### Description
Our goal for this app was to create a web application that allowed users - from every background with a varierty of needs - to find or create five-a-side games of football.

1. Everyone who visits the site can view the list of games available.
2. The list of games can be filtered or sorted by game type, minimum number of free spaces, maximum price, location, host's username, and date. It can also be filtered by duration of game, and sorted by starting time.
3. Users are required to register and login to:
    * Create their own game.
    * Join a game (with available spaces).
    * View other users' accounts.
4. Players can rate other participants from a game after the game has finished. This can only be done once, in order to improve the integrity of users' ratings.
5. Users who host their own game are responsible for overseeing it. This includes removing players (for any reason they deem necessary), and booking the pitch (if required). More information is available on the homepage once users have logged in.
---
#### External Sources
* Django (1.11.7):
    * https://docs.djangoproject.com/en/2.0/releases/1.11.7/
* JQuery (& Plugins):
    * https://jquery.com/ 
    * https://mottie.github.io/tablesorter/docs/
    * https://jqueryvalidation.org/
* Bootstrap:
    * https://getbootstrap.com/ 
* Geopy (1.11.0):
    * https://geopy.readthedocs.io/en/1.11.0/ 
* Coverage (4.5.1):
    * https://coverage.readthedocs.io/en/coverage-4.5.1/
* Google Maps Javascript API: 
    * https://developers.google.com/maps/documentation/javascript/tutorial

