# INFO319
Twitter stream analysis for emergency management; before, during or after an emergency. 

### Installation

Get pip requirements through 
``pip3 install -r requirements.txt``

### Running the program
Running the program from bash requires 3 steps:

1. Start the api with: 
``python3 run.py`` The run.py file is located inside
the webApi/ folder.

2. Start twitter_streaming.py file by simply
running it through ``python3 twitter_streaming.py``

3. Start the frontend by going into the frontend/ 
directory and first use ``npm install``. Once the 
install has finished start it by using ``npm start``.
This will start a local development server. A production
build can be generated through ``npm run build``.