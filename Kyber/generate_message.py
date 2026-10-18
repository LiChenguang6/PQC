import random
def generate_message(seed,filename,N):
    random.seed(seed)
    numbers=[]
    for i in range(N):
        m = random.randint(0,1)
        numbers.append(m)

    file = open(filename,"w")

    for num in numbers:
        file.write(str(num)+" ")
    file.close()
    return numbers
