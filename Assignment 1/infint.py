import sys

'''This part of the code was gathered by an image in the class groupme. I could not find a way to parse the command line arguments myself
so I used the image provided by another student as inspiration to solve this problem. The rest of my code after the Temp_string declaration is 
source code from myself. '''

command_arguments=str(sys.argv)
Input_file_name=command_arguments[command_arguments.index("=")+1:command_arguments.index("txt")+3]

#print("Command arguments: " + command_arguments)
#print("Input file name: "+ Input_file_name)

Temp_string=""


#From this point onward, the rest of the code is my own

#function to take in input from a given input file
def FileHandler(fileName):
    global Temp_string
    try:
        with open(fileName,"r",encoding="utf8") as inputFile:
            
            Temp_string=inputFile.read().split()

    except:
        print("File not found.")
    return Temp_string


#function to convert an integer list into a string: used for converting the integer list created by the operation function to be printed to output
def convert(list):
    res=int("".join(map(str,list)))#use the join function to concatenate the given list into a single string
    return res


#WORKING FUNCTION: this function parses a given string expression and creates an evaluatable stack for use to evaluate the prefix notation.
def parseExpression(expression, stack, index, multiDigit):
  temp = expression[index] #stores single char of expression based on given index value
  if(temp == 'a' or temp == 'm'): #stores letter 'a' and 'm' into a stack
    stack.append(temp)
  if(temp.isdigit()): #checks if char is a digit
    if(expression[index+1].isdigit() or expression[index+1] == ',' or expression[index+1] == ')'): #checks next value if it is a digit or comma or closed bracket and if it is, store it into the stack (used for multidigit numbers)
      multiDigit.append(temp) #new stack to store the multidigit, it is currently stored as single digits until later concantenation
      return parseExpression(expression, stack, index+1, multiDigit) #recursively loops back until the whole number is stored into a list
    else:
      stack.append(temp) #If it is just a single digit, then it will be added to the stack 
  if multiDigit: stack.append("".join(a for a in multiDigit)) #If mulitiDigit stack is not empty, concantenate all the elements to form the multidigit
  multiDigit = [] # resets stack so that it can be used later for more multidigit numbers(if any)
  if(temp == ')'): #stores closed parenthesis into the first stack
    stack.append(temp)
  if(index == len(expression)-1): #recursive end call, this signals to exit the recursive function
    return stack #returns the newly created stack with specifed inputs we made earlier
  return parseExpression(expression, stack, index+1, multiDigit) #recursive call to loop through each character of the expression by incrementing index value by 1


#WORKING FUNCTION: this function will evaluate the stacks and perform the approprate mathematical function calls. 
def evaluateExpressionStack(current_stack_value,stack,extracted_number_1,extracted_number_2):
    eval_stack=[]#this stack will be used to hold a ')' character in case there is no digit that follows this function
    number_1=''#this variable will hold the first operand for the operation 
    number_2=''#this variable will hold the second operand for the operation
    result_number=""#after performing an operation, compute the result and push it into the number stack
    error_string="invalid expression"#string to be return in the case that the expression is not valid
    #print("Reversing stack for evaluation")
    while stack:
        #parses the stack, popping each element and checking for the key symbols and digits
        current_stack_value=stack.pop()
        if len(stack)==0 and current_stack_value.isdigit():#if we pop out a value then check if the list is empty, we check to see if it is a digit. If the value is a digit, place it in the stack and return
            eval_stack.append(current_stack_value)
        else:
            #print("Current stack value: "+ str(current_stack_value))
            eval_stack.append(current_stack_value)
            #print("Evaluation stack: "+ str(eval_stack))
        if current_stack_value=="a":
            eval_stack.pop()#pops the current operator out
            add_checker_1=eval_stack.pop()
            if add_checker_1.isdigit():
                 number_1=add_checker_1#assigns the number on the top of the stack to number 1
            else:
                return error_string
            add_checker_2=eval_stack.pop()
            if add_checker_2.isdigit():
                number_2=add_checker_2#assigns the next number on the top of the stack as number 2
            else:
                return error_string
            eval_stack.pop()#pop out the ')' character that should be in the stack 
            result_number=add(number_1,number_2)
            eval_stack.append(result_number)
        elif current_stack_value=="m":
            eval_stack.pop()#pops the current operator out
            mult_checker_1=eval_stack.pop()
            if mult_checker_1.isdigit():
                number_1=mult_checker_1#assigns the number on the top of the stack to number 1
            else:
                return error_string
            mult_checker_2=eval_stack.pop()
            if mult_checker_2.isdigit():
                number_2=mult_checker_2#assigns the next number on the top of the stack to number 2
            else:
                return error_string
            eval_stack.pop()#gets rid of the ')' character which should be the next thing in the stack
            result_number=multiply(number_1,number_2)
            eval_stack.append(result_number)
    #print("Finished with calculations")
    final_answer=convert(eval_stack)
    #print("Final value= "+str(final_answer))
    return str(final_answer)


'''For my multiplication function, I followed a similar structure as my addition. I take an iterative approach by passing the two numbers as strings. I then convert the two strings into list values
That will store the numbers by element. The nodes in the list only hold one digit as I did not see a need to allow for node size manipulation necessary since the professor removed
the requirement to accept the 'digitsPerNode' input.'''
def multiply(string_1,string_2):
    #these lists will hold the values given by the parsed strings
    int_mult_list_1=[]
    int_mult_list_2=[]


    #this string will be returned if an error were to occur during runtime
    Error_string="invalid expression"
    

    #this value will institute the product of two values to be placed in the product list
    product=0

    #This value is going to store the carry over if the product of two elements is greater than 10
    carry=0

    #this list will hold the final product value of the given two lists
    prod_list=[]

    #these two values will maybe be used during a later parse of the two multiplication lists
    mult_list_1_size=0
    mult_list_2_size=0

    #counter for list size
    counter=0


    #these values will hold the given list numbers that will be multiplied together later
    list_of_values=[]

    #error checking the strings to make sure they are not empty. If they are not then we are to append the values from the argument strings and place them into the arrays
    if string_1=="":
        return Error_string
    else:
        for i in string_1:
            int_mult_list_1.append(int(i))
    #print("list 1= "+ str(int_mult_list_1))
    
    if string_2=="":
        return Error_string
    else:
        for j in string_2:
            int_mult_list_2.append(int(j))
    #print("list 2= "+str(int_mult_list_2))
    
    int_mult_list_1.reverse()
    int_mult_list_2.reverse()

    #print("list 1 reversed= "+str(int_mult_list_1))
    #print("list 2 reversed= "+str(int_mult_list_2))

    mult_list_1_size=len(int_mult_list_1)
    mult_list_2_size=len(int_mult_list_2)

    if len(int_mult_list_1)>40:
        print("Error: the length of number 1 is too large")
        return 0
    elif len(int_mult_list_2)>40:
        print("Error: the length of number 2 is too large")
        return 0
    
    #now begins the multiplication aspect of this function
    if mult_list_1_size>=mult_list_2_size:
        #print("printing out product values to test......")
        for i in range(mult_list_2_size):#The smaller value will be parsed in the outer loop
            for j in range(mult_list_1_size):#The larger value will be parsed first in the inner loop
                product=int_mult_list_2[i]*int_mult_list_1[j]+carry#perform the multiplication of the two elements
                #print(product)
                if product >= 10:
                    carry=product//10
                    remainder=product%10
                    #print("current carry value= "+str(carry))
                    #print("remainder value= "+ str(remainder))
                    prod_list.append(remainder)

                else:
                    prod_list.append(product)
                    carry=0
                product=0
            if carry!=0:
                prod_list.append(carry)
                carry=0
            prod_list.reverse()
            list_of_values.append(prod_list)
            prod_list=[] 
            counter+=1
            for i in range(counter):
                prod_list.append(0)
        for i in range(len(list_of_values)):
            list_of_values[i]=convert(list_of_values[i])
        #print("list of values:" +str(list_of_values))
    else:
        #print("printing out product values to test......")
        for i in range(mult_list_1_size):
            for j in range(mult_list_2_size):
                product=int_mult_list_1[i]*int_mult_list_2[j]+carry
                #print(product)
                if product >= 10:
                    carry=product//10
                    remainder=product%10
                    #print("current carry value= "+str(carry))
                    #print("remainder value= "+ str(remainder))
                    prod_list.append(remainder)

                else:
                    prod_list.append(product)
                    carry=0
                product=0
            if carry!=0:
                prod_list.append(carry)
                carry=0
            prod_list.reverse()
            list_of_values.append(prod_list)
            prod_list=[] 
            counter+=1
            for i in range(counter):
                prod_list.append(0)
        for i in range(len(list_of_values)):
            list_of_values[i]=convert(list_of_values[i])
        #print("list of values:" +str(list_of_values))
    
    final_result=0
    for i in range(len(list_of_values)):
        final_result+=int(list_of_values[i])
    #print("Final result= "+str(final_result))
    return str(final_result)
         


'''For my addition function, I have decided to use an iterative approach where I will take in the two values and place them into strings.
   I will then convert my strings into lists which I can then use to add values by node to acquire the solution. Each node holds one digit and I should be able to accomidate the 
   requirement that The node cannot exceed 40 digits.
'''
def add(string_1,string_2):
    #these two lists will hold the original value
    int_list_1=[]
    int_list_2=[]

    #this string will be returned in order to accomidate for any errors that are to be displayed in console
    Error_string="error"

    sum = 0
    #this list is going to hold the sum of both lists
    sum_list=[]

    #this is going to be used to determine the biggest list given and will be used later
    max_list_size=0
    list_1_size=0
    list_2_size=0

    #this carry value will be used if the sum of two indexes is 10 or greater
    carry=0

    #this value will hold the remainder of the modulus of a value to append to the sum list later
    remainder=0

    #here we are going to take the string of values and convert them into integer values that will be stored in the two lists
    if string_1=="":
        return Error_string
    else:
        for i in string_1:
            int_list_1.append(int(i))

    if string_2=="":
        return Error_string
    else:
        for j in string_2:
            int_list_2.append(int(j))

    #print("List #1 = "+ str(int_list_1))
    #print("List #2 = "+ str(int_list_2))
    #reverse the lists for the purpose of addition
    int_list_1.reverse()
    int_list_2.reverse()
    #print("Reversed list #1 = "+ str(int_list_1))
    #print("Reversed list #2 = "+ str(int_list_2))

    #we will keep hold of the list sizes in order to determine a maximum size sequence for my addition method later
    list_1_size=len(int_list_1)
    list_2_size=len(int_list_2)

    #we need to perform a check to see if the criteria for number length is accurate
    if len(int_list_1)>40:
        print("Error: the length of number 1 is too large")
        return 0
    elif len(int_list_2)>40:
        print("Error: the length of number 2 is too large")
        return 0


    #here the max list size will be determined to accomidate for when the two values are not the same length
    if len(int_list_1)>=len(int_list_2):
        max_list_size=len(int_list_1)
    else:
        max_list_size=len(int_list_2)

    #print("Maximum list size= "+ str(max_list_size))

    #this will be used to set the leading zeros to simplify addition
    if list_1_size > list_2_size:
        for i in range(list_1_size-list_2_size):
            int_list_2.append(0)
        #print("Old integer reversed List #1= "+str(int_list_1))
        #print("New integer reversed List #2= "+str(int_list_2))
    else:
        for j in range(list_2_size-list_1_size):
            int_list_1.append(0)
        #print("Old integer reversed List #2= "+str(int_list_2))
        #print("New integer reversed List #1= "+str(int_list_1))
    
    for x in range(max_list_size):
        sum=int_list_1[x]+int_list_2[x]+carry
        #print("current carry: "+ str(carry))
        #print(str(int_list_1[x])+"+"+str(int_list_2[x])+"+"+str(carry))
        if sum>=10:
            carry=sum//10
            remainder=sum%10
            sum_list.append(remainder)
        else:
            sum_list.append(sum)
            carry=0
        sum=0
    if carry>0:
        sum_list.append(carry)
    sum_list.reverse()
    answer=convert(sum_list)
    #print("answer gotten from addition function "+str(answer))
    

    
    return str(answer)

#====================================================BEGIN DRIVER CODE SEQUENCE==================================================================
#--------------------------------------------HW0 SOLUTION SET BEGINNING-----------------------------------------------------------------------

#gather the lists as a string first to convert later. NOTE: these values were only used for testing purposed and have since been disregarded
string_list_1="123456"
string_list_2="2593"



'''Opened_file=FileHandler(Input_file_name)
#print("Arguments: "+ str(Opened_file))
First_Number_List=[]
Second_Number_List=[]
for i in range(len(Opened_file)):
    Open_Bracket_index=Opened_file[i].find('(')
    Comma_index=Opened_file[i].find(',')
    Close_bracket_index=Opened_file[i].find(')')
    First_Number_List.append(Opened_file[i][Open_Bracket_index+1:Comma_index])
    Second_Number_List.append(Opened_file[i][Comma_index+1:Close_bracket_index])'''

#print(First_Number_List[2])
#print(Second_Number_List[0])
#print("Argument 1: "+ Opened_file[0])
'''Result_list=[]

for i in range(len(Opened_file)):
    Result_list=add(First_Number_List[i],Second_Number_List[i])
    Result_list="".join(map(str,Result_list))
    print(Opened_file[i]+"="+Result_list)'''
#--------------------------------------HW0 solution SET ENDING-------------------------------------------------------------------------------------------


#--------------------------------------HW1 SOLUTION SET BEGINNING-------------------------------------------------------------------------------------------


list_of_stacks=[]
myStack=[]
multiDigitNumber=[]
Result_list=[]
current_stack_value=""
number_1=""
number_2=""


File_hw1=FileHandler(Input_file_name)
#print("Arguments:" + str(File_hw1))
#print(str(File_hw1))
#createStack(File_hw1[0],myStack,0)
for i in range(len(File_hw1)):
    parseExpression(File_hw1[i],myStack,0,multiDigitNumber)
    list_of_stacks.append(myStack)
    #print("evaluated stack: "+ str(myStack))
    #print("Now evaluating operation stack.........")
    x=evaluateExpressionStack(current_stack_value,list_of_stacks[i],number_1,number_2)
    Result_list.append(x)
    print(File_hw1[i]+"="+Result_list[i])


#multiply(string_list_1,string_list_2)


#--------------------------------------------------HW1 SOLUTION SET ENDING------------------------------------------------------------------


#print("Program has finished")


#=================================================END DRIVER CODE SEQUENCE===============================================================================================
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++HW0 commentary++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''In the final iteration of the program, I have commented out several print statements throughout. These were for the sake of my own visualization
when I was testing various aspects of my code. I apoligize for the unprofessionalism and lack of organization in my code.'''

'''My code runs simply by inputing the command line inputs as stated in the hw instructions. The program will read in the desired input file and perform
the desired operation. It will then display the output in the console without writing it to a corresponding output file as that was not needed
in the instructions.'''
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++HW1 commentary+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''Similar to hw0, the code runs by inputting the command line as formatted in the hw1.pdf. The program is able to interpret the input file name from the given input
and will extract the strings from the inputfile. It will then run through the sequence of functions I have created and will evaluate each expression and display the output to the console.'''
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++