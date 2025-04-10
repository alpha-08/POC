import termcolor
import pyfiglet
import re
from datetime import *


class Security:
    def __init__(self,user,passwd):
        self.user=user
        self.passwd=passwd
        
    def validateCreds(self):
        
        
        with open ('E:\\St.Thomas\\Study Data\\Semester1\\Python\\project finalterm\\creds.txt') as credFile:
            creds=credFile.read()
            credsplit=creds.split(',')
            userr,passwordd=credsplit
            credentials={}
            credentials[userr]=passwordd
                
        if ((self.user in credentials) and (self.passwd==credentials[userr])):

            return True
        else:
            with open('E:\\St.Thomas\\Study Data\\Semester1\\Python\\project finalterm\\user.login.txt', 'a') as UserLoginTry:
                
                UserLoginTry.write(f'{self.user},{self.passwd}\n')
            
            print('\nInvalid Credentials, Try Again\n')
            return False



class UserBlock(Security):
    def numOfAttempts(self):
        with open ('E:\\St.Thomas\\Study Data\\Semester1\\Python\\project finalterm\\user.login.txt') as loginAttempts:
            attempts=loginAttempts.read()
            usercount=sum(1 for match in re.finditer(self.user, attempts)) # Regex

            return usercount

class Item:
    
    def __init__(self,Item_UPC,Item_Description,Item_Unit_Price,Item_Max_Qty,Item_Order_Threshold,Item_Replenishment_Order_Qty,Item_On_Hand):
        self.Item_UPC=Item_UPC
        self.Item_Description=Item_Description
        self.Item_Max_Qty=Item_Max_Qty
        self.Item_Order_Threshold=Item_Order_Threshold
        self.Item_Replenishment_Order_Qty=Item_Replenishment_Order_Qty
        self.Item_On_Hand=Item_On_Hand
        self.Item_Unit_Price=Item_Unit_Price
         
    def getUPC(self):
        return self.Item_UPC
    def getDescription(self):
        return self.Item_Description
    def getMaxQuality(self):
        return self.Item_Max_Qty
    def getOrderThreshold(self):
        return self.Item_Order_Threshold
    def getReplenishmentOrder(self):
        return self.Item_Replenishment_Order_Qty
    def getItemOnHand(self):
        return self.Item_On_Hand
    def GetItemUnitPrice(self):
        return self.Item_Unit_Price
    
    def __repr__(self):
        return f"{self.Item_Description}"

class ItemCollection:
    def __init__(self):
        self.ItemsDict={}


    def addItem(self, upc, itemObj): 
        self.ItemsDict[upc]=itemObj
        
    def printAllKeys(self):
        print(self.ItemsDict.keys())
        
    def printAllValues(self):
        # print("Values:")
        for item in self.ItemsDict.values():
            print(item)
    
    def eachDictItem(self):
        for key, value in self.ItemsDict.items():
            print(f"{key}, {value}")


def ReadFile():
    
    collectionObj=ItemCollection()  # here we created an object of Class ItemCollection.
    
    with open('E:\\St.Thomas\\Study Data\\Semester1\\Python\\project finalterm\\RetailStoreItemData.txt') as file:
        dbdata=file.readlines()
        # return dbdata[0:1]
        for line in dbdata[1:]:
            temp=line.strip().split(',') 

            upc= temp[0]
            item_description=temp[1]

            max_qty=temp[2]
            item_threshold=temp[3]
            item_replenishment=[4]
            item_onhand=temp[5]
            item_price=temp[6]
            ItemObj=Item(upc,item_description,max_qty,item_threshold,item_replenishment,item_onhand,item_price) # here we created Class Item obj and passing three paramters
            collectionObj.addItem(upc, ItemObj)                   # here we are passing upc and three parameters of Class Item obj into the dictionary created in class addItem.
    return collectionObj



def main():
    
    count=1

    itemCollectionObj = ReadFile()  # Read the file and get the populated ItemCollection object
    cart={}
    while True:
        
        ascii_banner = pyfiglet.figlet_format("Welcome to POS System",font='mini')
        colored_banner = termcolor.colored(ascii_banner, color='white')
        print(colored_banner)
        
        user=input('Enter Username: ')
        passwd=input('Enter Password: ')
        
        obj_security=Security(user, passwd)
        # obj_security.validateCreds()
        
        user_block=UserBlock(user, passwd)
                
        if obj_security.validateCreds():
                    
            while True:
                
                cart={}
                print('\n---------Select Option-------\n\n1= New Sales\n2=Return Items\n3=Backroom Ops\n9=Exit Application\n')
                selection=input('Enter Selection: ')
                
                if selection=='1':
                    
                    while True:                        

                        upc=input('\nEnter UPC: ')
    
                        if upc in itemCollectionObj.ItemsDict.keys():

                            item=itemCollectionObj.ItemsDict[upc]
                            print('{} Description: {}'.format(upc,item.getDescription()))
    
                            qty=int(input("Enter Quantity: "))                 
                            price=qty*int(item.GetItemUnitPrice())
                            print('Price for {} {}: {}\n'.format(qty,item.getDescription(),price))
                            cart[qty]=int(price)
                            print('Item added to cart, \nDo you want to continue? select:y/n')

                            sellagain=input('choose: ')
                            sellAgain=sellagain.lower()
                            if sellAgain=='y':
                                continue
                            else:
                                
                                break
                        else:
                            itemCollectionObj.ItemsDict.setdefault(upc,'No Translation')
                            print('UPC Not Found')
                    counter=1
                    
                    for i in cart:
                        
                        print('{}. {} | Qty.{}: ${}'.format(counter,upc,i, cart[i]))
                        
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        
                        with open('E:\\St.Thomas\\Study Data\\Semester1\\Python\\project finalterm\\receipt\\{}.txt'.format(timestamp),'a') as file:
                            file.write('{}\nUPC:{} | Qty.{}: Bill: ${}\nTotal Bill: ${}'.format(date.today(),upc,i, cart[i],sum(cart.values())))
                        counter+=1
                        print('\n------------------\nTotal bill: ${}\n------------------'.format(sum(cart.values())))
                    
                        
                elif selection=='2':
                        print('\nReturn Items screen\n')
                    
                elif selection=='3':
                        print('\nshow backroom ops\n')
                    
                    
                elif selection=='9':
                
                    break
                    
                else:
                        
                        print('\nEnter valid option\n')
            
        else:
            count+=1
            if user_block.numOfAttempts() > 3:
                print('User Blocked, Please contact system admin')
                break

        
if __name__=='__main__':
    main()
    
    
