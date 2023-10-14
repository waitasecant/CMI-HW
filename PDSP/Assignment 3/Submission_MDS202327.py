class BusBooking:

    def __init__(self):
        self.__count = 10000
        self.__wCount = 0  # Window seats filled
        self.__aCount = 0  # Aisle seats filled
        self.__seatDict = {}  # Seat:Booking Id
        self.__seatBooked = {}  # Seat:0/1
        self.__bookDict = {}  # Booking Id: (Name, Seat)
        self.__wList = []  # [Booking Id]
        self.__wlDict = {}  # Booking Id:WL Seat
        self.__makeDict(self.__seatDict)
        self.__makeDict(self.__seatBooked)

# ------------Helper Functions Start------------------
    def __makeDict(self, a):
        for i in ["W", "A"]:
            for j in range(20):
                a[f"{i}{j+1}"] = 0

    def __get_key(self, mydict, val):
        return list(mydict.keys())[list(mydict.values()).index(val)]

    def __sortDict(self, myDict):
        myKeys = list(myDict.keys())
        myKeys.sort()
        return {i: myDict[i] for i in myKeys}

    def __filterByPref(self, myDict, pref):
        newDict = {}
        for i in myDict:
            if i[0] == pref:
                newDict[i] = myDict[i]
        return newDict

    def __getLowestEmpty(self, pref):
        for i in self.__sortDict(self.__filterByPref(self.__seatBooked, pref)):
            if self.__seatBooked[i] == 0:
                return i
# ------------Helper Functions End------------------

# ------------Update Functions Start----------------
    def __addBookCount(self):
        self.__count = self.__count + 1
        return self.__count

    def __updateSeatBooking(self, pref):
        seat = self.__getLowestEmpty(pref)
        self.__seatBooked[seat] = 1
        return seat

    def __updateCount(self):
        tempw = self.__filterByPref(self.__seatBooked, "W")
        self.__wCount = sum(tempw.values())
        tempa = self.__filterByPref(self.__seatBooked, "A")
        self.__aCount = sum(tempa.values())

    def __updateBookDict(self, book_id):
        del self.__bookDict[book_id]
        for id in self.__wlDict:
            self.__bookDict[id] = (self.__bookDict[id][0], self.__wlDict[id])

    def __updateBookDictFill(self):
        for id in self.__wlDict:
            self.__bookDict[id] = (self.__bookDict[id][0], self.__wlDict[id])

    def __updatewlDict(self):
        self.__wlDict = {}
        for book_id in self.__wList:
            self.__wlDict[book_id] = f"WL-{self.__wList.index(book_id)+1}"
        return self.__wlDict
# ------------Update Functions End------------------

# ------------Main Functions Start------------------
    def book(self, name, pref):

        self.name = name
        self.pref = pref.lower()

        if self.pref in ["w", "window"]:
            self.pref = "w"
        elif self.pref in ["a", "aisle"]:
            self.pref = "a"
        else:
            self.pref = "no pref"

        if 0 in self.__seatBooked.values():
            if self.__wCount < 20 and self.__aCount < 20:

                if self.pref == "w":
                    book_id = eval(str(self.__addBookCount()))
                    seat = self.__updateSeatBooking("W")
                    self.__updateCount()
                    self.__seatDict[seat] = book_id
                    self.__bookDict[book_id] = (self.name, seat)
                    return (book_id, seat)

                elif self.pref == "a":
                    book_id = eval(str(self.__addBookCount()))
                    seat = self.__updateSeatBooking("A")
                    self.__updateCount()
                    self.__seatDict[seat] = book_id
                    self.__bookDict[book_id] = (self.name, seat)
                    return (book_id, seat)

                else:
                    if min(self.__wCount, self.__aCount) == self.__wCount:
                        book_id = eval(str(self.__addBookCount()))
                        seat = self.__updateSeatBooking("W")
                        self.__updateCount()
                        self.__seatDict[seat] = book_id
                        self.__bookDict[book_id] = (self.name, seat)
                        return (book_id, seat)

                    else:
                        book_id = eval(str(self.__addBookCount()))
                        seat = self.__updateSeatBooking("A")
                        self.__updateCount()
                        self.__seatDict[seat] = book_id
                        self.__bookDict[book_id] = (self.name, seat)
                        return (book_id, seat)

            elif self.__wCount == 20 and self.__aCount < 20:
                book_id = eval(str(self.__addBookCount()))
                seat = self.__updateSeatBooking("A")
                self.__updateCount()
                self.__seatDict[seat] = book_id
                self.__bookDict[book_id] = (self.name, seat)
                return (book_id, seat)

            elif self.__aCount == 20 and self.__wCount < 20:
                book_id = eval(str(self.__addBookCount()))
                seat = self.__updateSeatBooking("W")
                self.__updateCount()
                self.__seatDict[seat] = book_id
                self.__bookDict[book_id] = (self.name, seat)
                return (book_id, seat)

        else:
            book_id = eval(str(self.__addBookCount()))
            self.__wList.append(book_id)
            seat = f"WL-{self.__wList.index(book_id)+1}"
            self.__bookDict[book_id] = (self.name, seat)
            self.__wlDict[book_id] = seat
            return (book_id, self.__wlDict[book_id])

    def __fill(self):
        while 0 in self.__seatBooked.values() and self.__wList != []:
            first = self.__wList[0]
            seat = self.__get_key(self.__seatBooked, 0)
            self.__seatDict[seat] = first
            self.__bookDict[first] = (self.__bookDict[first][0], seat)
            self.__seatBooked[seat] = 1
            self.__wList.pop(0)
            self.__updatewlDict()
            self.__updateBookDictFill()

    def cancel(self, book_id):
        if book_id not in self.__bookDict:
            return False
        else:
            if book_id in self.__seatDict.values():
                seat = self.__get_key(self.__seatDict, book_id)
                self.__seatDict[seat] = 0
                self.__seatBooked[seat] = 0
                self.__updateBookDict(book_id)
                self.__updateCount()
            else:
                self.__wList.pop(self.__wList.index(book_id))
                self.__updatewlDict()
                self.__updateBookDict(book_id)
                self.__updateCount()
        self.__fill()
        return True

    def status(self, id):
        if id in self.__bookDict:
            return self.__bookDict[id]
        else:
            return False

    def __str__(self):
        selflist = []
        for id in self.__bookDict:
            selflist.append(
                (id, self.__bookDict[id][0], self.__bookDict[id][1]))
        return (str(selflist))
