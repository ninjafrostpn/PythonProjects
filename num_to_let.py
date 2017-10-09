__author__ = 'j00751'
letterlist = [chr(i) for i in range(ord("a"), ord("z") + 1)]
print(letterlist)
while True:
    numbers = input("Input a string of numbers\n>> ")
    if numbers == "kill":
        break
    else:
        numbers = numbers.split(" ")
    try:
        letters = ""
        oi = 0
        while oi < len(numbers):
            letters += letterlist[int(numbers[oi]) - 1]
            oi += 1
        print(letters)
    except:
        print("Invalid set")