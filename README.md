# INFO319
Twitter stream analysis for emergency management; before, during or after an emergency. 

### Installation

Get pip requirements through 
``pip3 install -r requirements.txt``

### Running the program
The program consists of several modules that communicates
with each other by passing data from one to the other.

1. Start the api with: 
``python3 run.py`` The run.py file is located inside
the webApi/ folder. This program is responsible for
sending the updated data to all connected clients
in real-time using web-sockets.

2. Start TweepyStreaming.py by simply
running it through ``python3 TweepyStreaming.py``
. This will await a connection before it begins to
stream data from twitter. When a connection is made,
from spark in this case, the programs starts running
and sends all incoming data to the connected socket.

3. Start SparkStreaming.py by setting up the system with
pyspark. The script is set up to be run using 
``spark-submit SparkStreaming.py``. This connects
to tweepy and receives the incoming data. The incoming
data is processed and words/hashtag counts are made for a 
certain short time period. When the data has been filtered
to only keep the most relevant information it is stored in
a database for bulk processing and sent through to the api to be passed to
clients. 

4. Start the frontend by going into the frontend/ 
directory and first use ``npm install``. Once the 
install has finished start it by using ``npm start``.
This will start a local development server. A production
build can be generated through ``npm run build``.