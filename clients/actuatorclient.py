import time
import requests # sende HTTP requests til API

import logging
log_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%H:%M:%S")

import common

LIGHTBULB_CLIENT_SLEEP_TIME = 4

class ActuatorClient:
    """
    Actuator client representing the physical light bulb in the house
    using the cloud service to set is state
    """

    def __init__(self, did):
        self.did = did
        self.state = common.ActuatorState('off')

    def get_state(self) -> str: # returnerer en string som representerer den nåværende tilstanden til aktuatoren

        """
        This method sends a GET request to the cloud service to
        read/obtain the current state of the light bulb actuator.
        """

        logging.info(f"Actuator Client {self.did} retrieving state")
        actuator_state = None

        url = f"http://localhost:8000/smarthouse/actuator/{self.did}/state"     # URL for GET request to retrieve actuator state
        response = requests.get(url)                                            # Retrives the response from the GET request

        if response.status_code == 200:
            actuator_state = response.json().get('state')
        else:
            logging.error(f"Failed to retrieve state for actuator {self.did}")

        return actuator_state


    def run(self): # kjører i en loop som regelmessig sender en forespørsel til skyen for å sette den nåværende tilstanden til lyspæren i samsvar med tilstanden i skyen
        """
        This method runs in a loop reguarly sending a request to the cloud service
        to set the current state of the light bulb in accordance with the state
        in the cloud service
        """

        while True:
            state = self.get_state()

            if state != self.state.state:           # Sjekker om den nye staten er forskjellig fra den nåværende staten
                logging.info(f"Actuator Client {self.did} changing state to {state}")
                self.state.state = state
            else:
                logging.info(f"Actuator Client {self.did} state is already {state}")

            time.sleep(LIGHTBULB_CLIENT_SLEEP_TIME)


if __name__ == '__main__': 

    actuator = ActuatorClient(common.LIGHT_BULB_ACTUATOR_DID) 
    actuator.run()