class Loginstate(object): 
    userID:int
    

    def search(self):
        global userID
        return userID

    def update(self, id):
        global userID
        userID=id
        print(userID)
        print("record")

    