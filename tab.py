'''
Created on 14.7.2023
@author: jalma
'''

from member import Member
from actions import Transaction, Operation
from datetime import datetime
import os

TAB_PATH = "tabs" #Directory for saving tab files
VERSION = "0.8"

class Tab():
    
    def __init__(self, read=False, name="", file="", path=""):
        self.version = VERSION
        self.members = []
        self.mem_count = 0
        self.transactions = []
        self.tr_count = 0
        self.operations = []
        self.op_count = 0
        self.parent = None
        self.children = []
        self.ch_count = 0
        self.string = ""
        self.name=name
        self.total_spending = 0
        self.directory = os.getcwd()
        if read:
            if file:
                self.read_from_file(os.path.join(os.path.join(self.directory, TAB_PATH), file))
            elif path:
                self.read_from_file(path)

            
    def read_from_file(self, path):
        #Reads an existing tab from a .txt file specified by path.
        with open(path, "r") as file:
            textIn = file.read().splitlines()
        if not textIn[0].startswith("Tabz"):
            return
        
        ver = float(textIn[0].split()[2])
        
        size = len(textIn)
        i=0
        
        tab = self
        parent = self
        
        while i<size:
            row = textIn[i]
            if row.startswith("Name: "):
                name = row[6:]
                if not self.name:
                    self.change_name(name)
                else:
                    for child in parent.children:
                        if child.name == name:
                            tab = child
                            break
                    if parent == tab:
                        return
                    
            elif row.startswith("Actions:"):
                i+=1
                
                while textIn[i] and i<size:
                    line = textIn[i].split()
                    timestamp = "{} {}".format(line[0], line[1])
                    if line[2] == "A:":
                        if not tab.parent:
                            tab.add_member(line[3], timestamp)
                    elif line[2] == "P:":
                        tab.add_purchase(self.find_member_id(line[3]), int(float(line[5])*100), timestamp)
                    elif line[2] == "T:":
                        tab.add_transfer(self.find_member_id(line[3]), self.find_member_id(line[5]), int(float(line[7])*100), timestamp)
                    elif line[2] == "B:":
                        tab.balance()
                    elif line[2] == "Z":
                        tab.zero_out()
                    elif line[2] == "R:":
                        tab.remove_member(self.find_member_id(line[3]))
                    elif line[2] == "E:":
                        names = line[5].split(",")
                        m_ids = [self.find_member_id(name) for name in names]
                        parent.exclude_members(m_ids, line[3])
                    else:
                        break
                    i+=1
            
            i+=1
            
        '''    
        try:
            while i<size and textIn[i][:4] != "Name":
                i +=1
            
            self.change_name(textIn[i][6:])
                
        except(IndexError):
            i=0
            
        while i<size and textIn[i] != "Actions:":
            i+=1
        i+=1
        while i < size:
            line = textIn[i].split()
            if len(line)>3:
                timestamp = "{} {}".format(line[0], line[1])
                if line[2] == "A:":
                    self.add_member(line[3], timestamp)
                elif line[2] == "P:":
                    self.add_purchase(self.find_member_id(line[3]), float(line[5]), timestamp)
                elif line[2] == "T:":
                    self.add_transfer(self.find_member_id(line[3]), self.find_member_id(line[5]), float(line[7]), timestamp)
                elif line[2] == "B:":
                    self.balance()
                elif line[2] == "Z":
                    self.zero_out()
                elif line[2] == "R:":
                    self.remove_member(self.find_member_id(line[3]))
                elif line[2] == "E":
                    names = line[5].split(",")
                    m_ids = [self.find_member_id(name) for name in names]
                    self.exclude_members(m_ids, line[3])
            else:
                break
            i+=1
            '''
            
            
            
    def parse_text(self, text):
        pass
        
        
        
    def write_to_file(self):
        if self.parent != None:
            self.parent.write_to_file()
        else:
            try:
                os.chdir(os.path.join(self.directory, TAB_PATH))
            except FileNotFoundError:
                self.create_directory(TAB_PATH)
                os.chdir(self.directory + TAB_PATH)
                
            with open("{}.txt".format(self.name), "w") as file:
                file.write(str(self))
            os.chdir(self.directory)
    
    
        
    def create_directory(self, dirpath):
        os.mkdir(os.path.join(self.directory, dirpath))
    
    
    
    def get_time(self):
        #Returns local time in format yyyy-mm-dd hh:mm
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    
    
    def find_member_id(self, name):
        #Finds the id of a member by name
        for member in self.members:
            if member.name == name:
                return member.id
            
            
            
    def find_member(self, m_id):
        for member in self.members:
            if member.id == m_id:
                return member
    
    
    
    def add_member(self, name, time="", m_id=-1):
        #Adds a new member to the tab.
        name= name.replace(" ", "_")
        if m_id < 0:
            m_id = self.mem_count
        self.members.append(Member(name, m_id))
        self.mem_count += 1
        self.op_count += 1
        if not time:
            time = self.get_time()
        self.string += "{} A: {}\n".format(time, name)
        self.operations.append(Operation("A", time, name))
    
    
    
    def remove_member(self, index):
        #Removes a member from the tab.
        member = self.members[index]
        time = self.get_time()
        self.string += "{} R: {}\n".format(time, self.members[index].name)
        self.total_spending -= member.spending
        self.operations.append(Operation("R", time, member.name))
        self.members.pop(index)
        self.mem_count -= 1
        self.op_count += 1
        for i in range(index, self.mem_count):
            self.members[i].id -= 1


    
    def add_transaction(self, payer_id, amount, recipient_id=-1, time=""):
        if not time:
            time = self.get_time()
        transaction = Transaction(payer_id, amount, self.tr_count, recipient_id, time)
        self.tr_count += 1
        return transaction  
        
    
    
    def add_purchase(self, payer_id, amount, time=""):
        #Adds a purchase for a member.
        purchase = self.add_transaction(payer_id, amount, time=time)
        self.transactions.append(purchase)
        payer = self.find_member(payer_id)
        payer.add_spending(amount)
        self.total_spending += amount
        self.string += "{} P: {} | {}\n".format(purchase.timestamp, payer.name, str(amount/100))
    
    
    
    def add_transfer(self, payer_id, recipient_id, amount, time=""):
        #Adds a peer actions from a member to another.
        payer = self.find_member(payer_id)
        recipient = self.find_member(recipient_id)
        transfer = self.add_transaction(payer_id, amount, recipient_id, time=time)
        self.transactions.append(transfer)
        payer.add_spending(amount)
        recipient.add_spending(-amount)
        self.string += "{} T: {} -> {} | {}\n".format(transfer.timestamp, payer.name, recipient.name, str(amount/100))
        #self.string += transfer.timestamp + " T: " + payer.name + " -> " + recipient.name + " | " + str(amount) + "\n"
    
    
    
    def find_tabs(self):
        return [file for file in os.listdir(self.directory + TAB_PATH) if file.endswith(".txt")]
        
    
    
    '''def create_child(self, e=[], i=[]):
        child = Tab(read=False, "{}_{}".format(self.name, self.ch_count))
        self.ch_count += 1
        if e:
            for mem in self.members:
                pass
        elif i:
            pass
        
        self.children.append(child)'''
    
    
    
    def exclude_members(self, m_ids, name=""):
        #Excludes members from future payments.
        new_members = [x for x in self.members if x.id not in m_ids]
        
        if self.parent != None:
            parent = self.parent
        else:
            parent = self
            
        #tab = next((child for child in parent.children if child.members == new_members), None)
        
        if not name:
            name = "Sub_{}".format(parent.ch_count)
        subtab = Tab(name = name)
        parent.ch_count += 1
        for mem in new_members:
            subtab.add_member(mem.name, m_id = mem.id)
        subtab.parent = parent
        parent.children.append(subtab)
        time = self.get_time()
        names = [mem.name for mem in parent.members if mem.id in m_ids]
        exclusion = Operation("E", time, exclusions = names)
        parent.operations.append(exclusion)
        parent.string += "{} E: {} | {}\n".format(time, subtab.name, ",".join(names))

        return subtab
    
    
    
    def include_member(self, members):
        #Adds previously exlcuded members back into the tab.
        pass
    
    
    
    def remove_transaction(self, transaction):
        #Removes specified actions from the tab.
        pass



    def balance(self):
        #Sets all members' spending to the average
        average = self.total_spending // self.mem_count
        for member in self.members:
            member.set_spending(average)
        time = self.get_time()
        self.operations.append(Operation("B", time, amount=average))
        self.string += "{} B: {}\n".format(time, average/100)
        self.op_count += 1
            
        
        
    def zero_out(self):
        for mem in self.members:
            mem.zero_spending()
        time = self.get_time()
        self.operations.appent(Operation("Z", time))
        self.string += "{} Z".format(time)
    
    
    
    def get_required_transfers(self, include_children=True):
        #Gives the required money transfers in order to balance spending.
        average = self.total_spending // self.mem_count
        above = []
        below = []
        transfers = []
        
        #Separates members according to spending (higher or lower). Average spending members do not require transfers in or out.
        for i in self.members:
            if i.spending > average:
                above.append({"id": i.id, "name": i.name, "spending": i.spending})
            elif i.spending < average:
                below.append({"id": i.id, "name": i.name, "spending": i.spending})
        
        def sortSpending(memb):
            return memb["spending"]
        
        #highest spender first
        above.sort(reverse=True, key=sortSpending)
        
        #lowest spender first
        below.sort(key=sortSpending)
        
        k,l = 0,0
        
        #Creates required transfers.
        while k < len(above) and l < len(below):
            higher = above[k]
            lower = below[l]
            higher_diff = higher["spending"]-average
            lower_diff = average-lower["spending"]
            if higher_diff > lower_diff:
                transfers.append(Transaction(lower["id"], lower_diff, recipient=higher["id"]))
                higher["spending"] -= lower_diff
                lower["spending"] += lower_diff
                l += 1
            elif above[k]["spending"]-average < average-below[l]["spending"]:
                transfers.append(Transaction(lower["id"], higher_diff, recipient=higher["id"]))
                higher["spending"] -= higher_diff
                lower["spending"] += higher_diff
                k+=1
            else:
                transfers.append(Transaction(lower["id"], higher_diff, recipient=higher["id"]))
                higher["spending"] -= higher_diff
                lower["spending"] += higher_diff
                k += 1
                l += 1
                
                
        def check_for_overlaps(transfers, ch_tr):
            for tr in transfers:
                if ch_tr.matches(tr):
                    tr.amount += ch_tr.amount
                    return True
                elif ch_tr.is_opposite(tr):
                    tr.amount -= ch_tr.amount
                    if tr.amount == 0:
                        transfers.remove(tr)
                    elif tr.amount < 0:
                        tr.reverse()
                    return True
            return False
                
        
        if include_children:
            ch_transfers = []
            
            for child in self.children:
                ch_transfers = child.get_required_transfers()
                ch_transfers = [ch_tr for ch_tr in ch_transfers if not check_for_overlaps(transfers, ch_tr)]
                transfers += ch_transfers
                            
        return transfers
    
    
    
    def change_name(self, name):
        self.name = str(name)
        
    
    
    def transactions_to_string(self):
        string = ""
        
        for tr in self.transactions:
            time, payer_id, recipient_id, amount = tr.get_info()
            string += "{} {}".format(time, self.find_member(payer_id).name)
            if recipient_id >= 0:
                string += " -> {}".format(self.find_member(recipient_id).name)
            string  += " | {}\n".format(str(amount/100))
            
        return string
    
    
    
    def operations_to_string(self):
        string = ""
        
        for op in self.operations:
            string += "{}\n".format(str(op).replace("A:", "Added:").replace("B:", "Balanced:").replace("E:", "Excluded:")) 
        return string
    
    
    
    def actions_to_string(self):
        return self.string.replace("A:", "Added:").replace("B:", "Balanced:").replace("P: ", "").replace("T: ", "").replace("R:", "Removed")
       
    
    
    def members_to_string(self):
        string = ""
        for member in self.members:
            m_id, name, spending = member.get_info()
            string += "{} {} {}\n".format(m_id, name, spending)   
        return string
        
    
    
    def __str__(self):
        string = ""
        if self.parent == None:
            string = "Tabz version " + self.version + "\n\n"
            
        string += "Name: " + self.name +"\n\n"
            
        string += "Members<"
        for i in range(0, self.mem_count):
            string += self.members[i].name
            if i != self.mem_count - 1:
                string += ", "
        string += ">\n\n"
            
        string += "Actions:\n{}\n".format(self.string)
            
        string += "Required transfers:\n"
        
        for i in self.get_required_transfers():
            string += "{}\n".format(str(i))
            
            
        for child in self.children:
            string += "\n{}".format(str(child))
        '''    
        for count, child in enum(self.children):
            string += "Child#{} {}\n".format(count, child.name)
            string += "Members<"
            for i in range(0, child.mem_count):
                string += self.members[i].name
                if i != self.mem_count - 1:
                    string += ", "
            string += ">\n\n"'''
            
        return string