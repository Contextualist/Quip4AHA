import quip

class QuipClient4AHA(QuipClient)
    AHABC_ID = "PCeAOAQx6sO"
    
    KEYWORD=("Good Morning AHA", 
             "Now for this week in history", 
             "In World News", 
             "Now for the fun facts", 
             "In AHA News"), 
    B_WEIGHT=(1.00, 1.30, 1.50, 1.20, 1.00), 
    HOST=["Edward", "Katherine", "Sissy", "Harry"], 
    PN_PER_B=(1, 1, 2, 1, 3)): 

    
    def __init__(self):
        QuipClient.__init__(self, 
            access_token="Wk9EQU1BcDZFS04=|1483091850|CF037JVoITJPnAET8aHWnZwEZACvrIm7jtkRIQCaX3g=")
    
    def get_folder_AHABC(self):
        QuipClient.get_folder(self, id=AHABC_ID)
