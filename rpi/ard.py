class ArdState:
    def __init__(self, b0, b1, b2, b3, dst, state, txt):
        self.button0 = b0 > 50
        self.button1 = b1 > 50
        self.button2 = b2 > 50
        self.button3 = b3 > 50
        self.distance = dst;
        self.state = state;
        self.txt = txt;

    def __str__(self):
        return self.txt

def try_to_read_arduino_state(txt):
    if txt == "":
        return None
    numbers = txt.split(',')
    if len(numbers) != 6:
        return None
    try:
        b0 = int(numbers[0])
        b1 = int(numbers[1])
        b2 = int(numbers[2])
        b3 = int(numbers[3])
        dst = float(numbers[4])
        state = int(numbers[5])
        return ArdState(b0, b1, b2, b3, dst, state, txt)
    except:
        return None
    return None
