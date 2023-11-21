class Node:
    def __init__(self, initVal=None):
        self.value = initVal
        if self.value != None:
            self.tag = "L"
            self.left = None
            self.right = None
        else:
            self.value = None
            self.tag = None
            self.left = None
            self.right = None
        return

    def inorder(self):
        if self.tag == None:
            return []
        if self.tag == "L":
            return [(self.tag, self.value)]
        else:
            return self.left.inorder()+ [(self.tag, self.value)] + self.right.inorder()

    def collect(self):
        if self.tag == "L":
            return [self.value]
        else:
            return self.left.collect() + [self.value] + self.right.collect()

    def __str__(self):
        return str(self.inorder())

    def find(self, v):
        if self.tag == "L":
            return False
        if self.value == v:
            return True
        if v < self.value:
            return self.left.find(v)
        if v > self.value:
            return self.right.find(v)


    def find_tag(self, v):
        if self.tag == "L":
            if self.value == v:
                return self.tag
            else:
                return False
        if self.value == v:
            return self.tag
        if v < self.value:
            return self.left.find_tag(v)
        if v > self.value:
            return self.right.find_tag(v)
        

    def insert(self, v):
        if self.value == None:
            self.value = v
            self.tag = "L"
            return
            
        if self.value == v:
            return
            
        if v < self.value:
            if self.tag == "L":
                self.left = Node(v)
                self.right = Node(self.value)
                self.tag = "I"
            else:
                self.tag = "I"
                self.left.insert(v)
            return
            
        if v > self.value:
            if self.tag == "L":
                self.right = Node(v)
                self.left = Node(self.value)
                self.value = v
                self.tag = "I"
            else:
                self.tag = "I"
                self.right.insert(v)
            return


    def delete(self,v):    
            
        if self.find_tag(v)=="I":
            if self.value == None:
                return
            if v < self.value:
                self.left.delete(v)
            if v > self.value:
                self.right.delete(v)
            if v == self.value:
                if self.value != self.right.value:
                    self.value = self.right.value
                    self.right = self.right.right
                else:
                    self.value = min(self.collect())
                    self.left = None
                    self.right = None
                    self.tag = "L"

        elif self.find_tag(v)=="L":
            temp = self
            temp_left = temp.left

            if temp.value == None:
                return
            
            if temp.value == v:
                temp.value = None
                temp.tag = None
                return

            while temp_left.value!= v:
                temp = temp_left
                temp_left = temp_left.left

            temp.value = temp.right.value
            temp.tag = temp.right.tag
            temp.left = temp.right.left
            temp.right = temp.right.right
        else:
            return
