char = int(input())



if ((char < 10 and (char % 10 == 1)) or
        ((11 < char < 100 and (char % 10 == 1)) or
         ((char > 100 and (char % 100 in [1, 21, 31, 41, 51, 61, 71, 81, 91]))))):
    print(char, 'программист')


elif ((char < 10 and (char % 10 in [2, 3, 4])) or

      (20 < char < 100 and ((char % 10 in [2, 3, 4]))) or

      (char > 100 and (char % 100 in [2, 3, 4, 22, 23, 24, 32, 33, 34, 42, 43, 44, 62, 63, 64, 82, 83, 84])) or

      (char % 100 in [52, 53, 54]) or

      (char % 100 in [72, 73, 74]) or

      (char % 100 in [92, 93, 94])):

    print(char,'программиста')

else:
    print(char,'программистов')

