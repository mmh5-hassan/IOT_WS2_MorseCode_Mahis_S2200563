from microbit import *
import radio
radio.on()

#Morse code to character mapping
morse_map = {
    ".-"   : "A",
    "-..." : "B",
    "-.-." : "C",
    "-.."  : "D",
    "."    : "E",
    "..-." : "F",
    "--."  : "G",
    "...." : "H",
    ".."   : "I",
    ".---" : "J",
    "-.-"  : "K",
    ".-.." : "L",
    "--"   : "M",
    "-."   : "N",
    "---"  : "O",
    ".--." : "P",
    "--.-" : "Q",
    ".-."  : "R",
    "..."  : "S",
    "-"    : "T",
    "..-"  : "U",
    "...-" : "V",
    ".--"  : "W",
    "-..-" : "X",
    "-.--" : "Y",
    "--.." : "Z",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",
    "-----": "0"
}


dotInterval = 230
dashInterval = 470

letterThreshold = 1000

buffer = ''

started_time = running_time()

#Function to decode a Morse code
def decode(buffer):
    return morse_map.get(buffer, '?')


while True:
    #Calculate the time waiting for a signal
    waiting = running_time() - started_time
    signal = radio.receive()

    #sorting to "." or "-" based on A press time
    if button_a.was_pressed():
        key_downtime = running_time()
        
        while button_a.is_pressed():
            pass

        duration = running_time() - key_downtime
        if duration <= dotInterval:
            display.show(Image('00000:'
                               '00000:'
                               '00900:'
                               '00000:'
                               '00000'))
            radio.send('.')
            sleep(50)
            display.clear()
        elif duration >= dotInterval:
            display.show(Image('00000:'
                               '00000:'
                               '09990:'
                               '00000:'
                               '00000'))
            radio.send('-')
            sleep(50)
            display.clear()
        
    # listening to morse code signals
    if signal:
        if signal == '.':
            buffer += '.'
            display.show(Image('00000:'
                               '00000:'
                               '00900:'
                               '00000:'
                               '00000'))
            sleep(dotInterval)
            display.clear()
        elif signal == '-':
            buffer += '-'
            display.show(Image('00000:'
                               '00000:'
                               '09990:'
                               '00000:'
                               '00000'))
            sleep(dashInterval)
            display.clear()

            
        #waiting time reset as signal received
        started_time = running_time()

        
    #Check to see if waiting time has exceeded the threshold for a letter
    elif len(buffer) > 0 and waiting > letterThreshold:
        character = decode(buffer)
        buffer = ''
        display.scroll(character)
