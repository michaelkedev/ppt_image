import time
while True:
    print("c")
    try:
        print("a")
    except Exception as e:
        print("b")
        pass
    time.sleep(1)