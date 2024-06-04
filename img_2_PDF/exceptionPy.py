a=10
b=0
c=0

while (True):
    try:
        print("inside first try")
        print (a/b)
        print(a/c)
        try:
            print ("This is inner try block")
            print(a/c)
        except Exception:
            print ("General exception")
        finally:
            print ("inside inner finally block")
        
    except ZeroDivisionError:
        print ("Division by 0")
        break
    else:
        print ("This is other else block")
        print(a/c)
    finally:
        print ("inside outer finally block")
