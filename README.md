# All About Countries by Burgers and Fries
This is a website all about countries! \
After learning about the countries, test your knowledge with our quiz! 


### Roster:
- Benjamin Avrahami: Frontend and Bootstrap Framework
- Ethan Chen: Backend Flask
- Peihua Huang: Database/API
- Jionghao Wu: Project Manager

<br>

### APIs required (no keys needed!!!):
- [REST Countries](https://docs.google.com/document/d/1aQRi7FIILs_x3RE5i65KHuuy49Rt05ZqERKqZjOGiJw/edit) - basic info about countries
- [Currency Exchange](https://docs.google.com/document/d/1yTckLoGBHA-C37hhukXOc76Jh_770L7m3Moj-wMFeUU/edit) - exchange rates between base country and other countries on record
- [Agify.io](https://docs.google.com/document/d/1_YHaU-HXpDXaBDa3xPbGl2P9yBmzjuxKakyp4LRwow4/edit) - number people and average age of a person with a given name in a given country


### How to run this project
1. To ensure that we're running on the same package versions, run it with a virtual environment with the following commands:
   ```
   python3 -m venv <name of vitrual environment>    # creates a virtual environment named <name of virtual environment>
   .<name of vitrual environment>/bin/activate      # activates the virtual environment
   ```
2. Clone and change into our repository:
   ```
   git clone https://github.com/jhwu03/Softdev-API.git
   cd Softdev-API/
   ```
3. Install all the needed packages using the following command in a terminal: <br>
   ```
   pip3 install -r doc/requirements.txt
   ```
4. Once all the packages are install, run the project:
   ```
   python3 app.py
   ```
   Once the Flask is running, open http://127.0.0.1:5000/ in the browser
5. If you are running a virtual environment, deactivate it by entering `deactivate` into the command line.
