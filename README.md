# All About Countries by Burgers and Fries

### Roster:
- Benjamin Avrahami: Frontend and Bootstrap Framework
- Ethan Chen: Backend Flask/API
- Peihua Huang: Database
- Jionghao Wu: Project Manager

<br>

### APIs required:
- REST Countries - basic info about countries
- Currency Exchange - exchange rates between base country and other countries on record
- Open Trivia - list of trivia questions (may be implemented if time allows)
- Maps Static - customized image from google maps
- UNdata - information on growth, pollution, and health indicators that the UN uses
- Agify.io - number people and average age of a person with a given name in a given country


### How to run this project
1. Clone and change into our repository:
   ```
   git clone https://github.com/jhwu03/Softdev-API.git
   cd Softdev-API/
   ```
2. Install all the needed packages using the following command in a terminal: <br>
   ```
   pip3 install -r doc/requirements.txt
   ```
3. If pip command is restricted, run it with a virtual environment with the following commands:
   ```
   python3 -m venv <name of vitrual environment>    # creates a virtual environment named <name of virtual environment>
   .<name of vitrual environment>/bin/activate      # activates the virtual environment
   pip3 install -r doc/requirements.txt             # installs all the packages needed
   ```
4. Once all the packages are install, run the project:
   ```
   python3 app.py
   ```
   Once the Flask is running, open http://127.0.0.1:5000/ in the browser
5. If you are running a virtual environment, deactivate it by entering `deactivate` into the command line.
