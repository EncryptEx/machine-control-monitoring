import re

def parse_response(response):
    print(response)
    response = response.strip()
    if "[" not in response:
        return response, None, None
    
    i = len(response)-1
    while (response[i] != "["): 
        i -= 1

    user_response = response[:i-1]
    s = response[i:]

    match = re.match(r"\[(\d+)\](?:\s*(\w))?", s)
    print("user response:")
    print(user_response)
    if match:
        number = int(match.group(1))  
        parameter = match.group(2) if match.group(2) else None
        print(number)
        return user_response, number, parameter

    return user_response, None, None

def parse_info_sensors(data):
    
    parsed_data = {
        "Motor Status": f"{'Running' if data['isServoRunning'] else 'Not Running'}",
        "Real Velocity (m/s)": round(data['realVelocity'], 2),
        "Practical Velocity (m/s)": round(data['practicVelocity'], 2),
        "Total number of boxes passed": data['totalBoxesCount'],
        "Speed": round(data['absoluteServoVelocity'], 2),
        "Servo Direction": "f Forward" if data['isForward'] == 'f' else "b Backward",
        "Voltage (V)": round(data['voltage'], 2),
        "Current (mA)": round(data['current'], 2),
        "Power (mW)": round(data['power'], 2),
    }
    print(parsed_data)
    return parsed_data

