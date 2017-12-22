from flask import *
import os
import signal
import mcp3008
import RPi.GPIO as GPIO
from relaytest import setpins, relayon

app = Flask(__name__)

def get_reading(numchip=2):
    reading_arr = [0]*numchip*8
    for i in range(0,numchip):
        for j in range(0,8):
            reading_arr[i*8+j] = mcp3008.readadc(j,i)
    return reading_arr

@app.route('/')
def index():
    reading_arr = get_reading(2) # Number of sensors = 2.
    return render_template('index.html', reading_arr=reading_arr)

@app.route('/moisture')
def process0():

    return index()

@app.route('/trigger1')
def process1():
    setpins()
    relayon()
    GPIO.cleanup()
    return index()

#    return render_template('trigger1.html')
    

@app.route('/trigger2')
def process2():
    setpins()
    relayon(1)
    GPIO.cleanup()
    
#    return render_template('trigger2.html')
    return index()

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
    
    
  
    
    
    

    

    
