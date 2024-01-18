val = 0

def increment():
    global val

    val += 1

def main():
    global val

    print(val)

    should = input("Increment? (y)es/(n)o").lower()
    
    if should == 'y':
        increment()
    
    print(val)
    
if __name__ == "__main__":
    main()
