from serial import Serial
import time

# ser = Serial('/dev/cu.usbmodem141401', 9600) # change port name accordingly
arduino = Serial(port='/dev/cu.usbmodem141401', baudrate=9600, timeout=.1)

instructions = []

# generate instructions
for i in range(1, 61):
    instr = {"x": i, "y": i, "x_rpm": i, "y_rpm": i}
    instructions.append(instr)

i = 0
while True:
    time.sleep(1)

    if i >= len(instructions):
        break

    instr = instructions[i]
    b = bytes(instr["x"], instr["y"], instr["x_rpm"], instr["y_rpm"], -1)
    arduino.write(b)

    s = f'{instr["x"]},{instr["y"]},{instr["x_rpm"]},{instr["y_rpm"]}'
    # arduino.write(f'{s}\n'.encode())
    print(f'Sent instruction: {instr}')
    res = arduino.read_until(b'\n').decode().strip()
    print(f'Successfully recieved instruction: {res}')
    if res == s:
        i+=1
    time.sleep(0.1)
