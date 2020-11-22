
#function to check if the symbol already exists or not

def notExists(symbol,paramter,_boolean):
	mil_gaya = 0
	symbolFileReading = open("SYMTAB.txt","r")

	for lines in symbolFileReading:
		line = lines
		line = line[:-1]
		splitline = line.split('\t')



		if (splitline[0] == symbol):
			mil_gaya +=1
			break


	if (mil_gaya >0):
	
	
		_boolean = False
		return int(_boolean)
	else:
		#return 1;
		return int(_boolean)

	symbolFileReading.close()



#returns the number of bytes in decimal format
def cal_bytes(mnemonic,operand):

	found=0
	noOfBytes=-1

	if(mnemonic=="RESW" or mnemonic=="RESB" or mnemonic=="WORD" or mnemonic=="BYTE"):
		found=1
		if(mnemonic=="RESW"):
			operand = int(operand)
			noOfBytes = operand*3
		elif(mnemonic=="RESB"):
			operand = int(operand)
			noOfBytes = operand
		elif(mnemonic=="WORD"):
			noOfBytes = 3
		elif(mnemonic=="BYTE"):
			length=len(operand)-3
			if(operand[0]=='X'):
				if(length%2==0): noOfBytes=length/2
				else: noOfBytes = (length/2)+1
			elif(operand[0]=='C'):
				noOfBytes=length
	
	
	if(found==0):
		opcode = open("OPCODE.txt","r")		#opcode file              

		for opLine in opcode:
			op= opLine.split('\t')
		
			if(mnemonic==op[0]):
				found=1
				noOfBytes=op[1]
				break
				
		opcode.close()
		
	if(found==0):
		noOfBytes=-1
	
	noOfBytes = int(noOfBytes)
	return noOfBytes

#this function will return the opcode of the operand

def returnOpcode(shortForm,paramter):
	alpha  = paramter
	mil_gaya = 0
	opCodeFile = open("OPCODE.txt","r") #opening the opcode file


	for lines in opCodeFile:
		line = lines
		line = line[:-1]
		op = line.split("\t")



		if (shortForm == op[0]):
			opcode = op[2]
			mil_gaya+=1
			break





	if (mil_gaya==1):
		return opcode
	else:
		return alpha




#this function will return the ascii code of the character under the scrutiny of our eyes.

def returnASCII(paramter,character):
	mil_gaya = 0
	alpha  = paramter
	asciiFileOpen = open("ASCII.txt","r")

	for lines in asciiFileOpen:
		line = lines
		line = line[:-1]
		lineSplit = line.split('\t')



		if(lineSplit[1] == str(character)):
			mil_gaya += -1
			asciiCode = lineSplit[0]
			break



	if (mil_gaya <0):
		return asciiCode
	else:
		return alpha



#this function will return the address of the label

def returnAddress(paramter,label):
	symbolFileReading = open("SYMTAB.txt","r") # to read the address. of the label
	mil_gaya = 0
	alpha = paramter


	for lines in symbolFileReading:
		line = lines
		line = line[:-1]
		splitline = line.split("\t")


		if(splitline[0] == label):
			mil_gaya+=1

			
			tAdd = splitline[1]



			break
	symbolFileReading.close()


	if(mil_gaya>0):
		return tAdd
	else:
		return alpha




#*********************************************************************************#
							#INITIATING EXECUTION
#*********************************************************************************#

FileName=input("File name: ")


assemF=open(FileName,"r")
#assembly code file
addF=open("aCODE.txt","w") 
#file that stores addresses in assembly code
labelF = open("SYMTAB.txt","w")
#file that stores labels in the assembly code

begin = assemF.readline();			
#assumption: first line of the code is the start statement

 
while(begin[0]=='.'):
	begin = assemF.readline();

begin = begin[:-1]

Line1 = begin.split('\t')
#print (Line1)

addHex = Line1[2]	#value of address in hex #addf
add = int(addHex,16)	#converted the value in decimal
addHD= addHex		#duplicate containing hex value #add1
#


"""we are converting the first address into decimal and after adding the right number of bytes
we will convert it back to hexadecimal"""

print("\n")
for i in assemF:
	line = i
	line = line[:-1]
	
	line1 = line.split('\t')

	if(line[0]!='.'):
		if(line1[1]=="END"):
			break
	
		nBytes=0
		if(len(line1)==3):
			nBytes = cal_bytes(line1[1],line1[2])		#returns no of bytes in decimal  #harshal
		else:
			nBytes = cal_bytes(line1[1],0)
		
	
		if(nBytes==-1):
			error= "Error: Invalid mnemonic " + line1[1]
			print(error)
			input()
			exit(0)


		# ENTRY INTO SYMTAB  #harshal
		if(line1[0]!=''):
			u=True					#if label is not empty
			if(notExists(line1[0],-1,u)):		#checks if the label is already present or not  #harshal
				sym = line1[0] + "\t" + addHD    #store the zeroth element and the second element in the sym tab or else report the error
				



				#print(symbol)
				labelF.write(sym)
				labelF.write("\n")
				labelF.flush()
			else:
				error= "Error: " + line1[0] + " - Multiple declaration "
				print(error)
				input()
				exit(0)



		#WRITING INSTRUCTIONS ALONG WITH ASSIGNED ADDRESSES	
		lineWrite= addHD + "\t" + line		#check if \n is a part of line	#Add1 is hex
		#print(writeLine)					#PRINTS ON-SCREEN
		addF.write(lineWrite)				#writes into file  #harshal
		addF.write("\n")
		addF.flush()
			
		#CALCULATION OF NEXT ADDRESS
		add = add + nBytes				#performs decimal addition
		addHD="{0:b}".format(add)    #str(format(add,'04x'))	#converts to hex before storing 4x
		length = 4-len(addHD)
		addHD = "0"*length + addHD


labelF.close()
assemF.close()
addF.close()

#temporary file with appropriate addresses and SYMTAB have been created
#***********************************************************************#


assemFI = open("aCODE.txt","r")	#assembly code file with addresses  #harsal
obcd = open("objCODE.txt","w")	#to store the assembly file with object code  #harshal
ob = open("sic.o","w")				#to store only the object code  #harshal


assemFI.seek(0)


for i in assemFI: 
	line = i
	line = line[:-1]
	line2 = line.split('\t')

	address=line2[0]
	label = line2[1]
	sym = line2[2]
	u=0
	if(len(line2)==4):
		operand = line2[3]
	else:
		u=1
	int1=0
	int2=1
	int3=2

	if(sym!="RESW"	and	sym!="RESB"):
		if(sym=="BYTE"):					#OBJECT CODING for sym: BYTE
			array = operand.split('\'')
			if(array[0]=="X"):
				objLine = array[1]

			elif(array[0]=="C"):
				list1 = list(array[1])			
				objLine = ""
				

				
				for char in list1:
					asciic= returnASCII(-1,char)
					if (asciic==-1):
						print("Error: Invalid character in BYTE")
						input()
						exit(0)
					objLine =  asciic +asciic

						

					

		elif(sym=="WORD"):		
								#OBJECT CODING for sym: WORD
			"""operand = int(operand)
			objLine = "{0:b}".format(operand)#str(format(operand,'#010b'))[2:]		#6		
			length = 4-len(objLine)"""
			
			objLine=" "
		elif(sym=="RSUB"):					#OBJECT CODING for sym: RSUB
			opcode = returnOpcode(sym,-1)
			if(opcode==-1):
				print("Error: Opcode for RSUB could not be found")
				input()
				exit(0)

			else:
				int2=3
				objLine = opcode + "0000"



		else:									#OBJECT CODING for all other mnemonics
			opcode = returnOpcode(sym,-1)
			if(opcode==-1):
				error="Error: Opcode for " + sym + " not found"
				print(error)
				input()
				exit(0)
			
			opsplit = operand.split(',')
			length = len(opsplit)
			
			dirAdd =returnAddress(-1,opsplit[0]) 
			if(dirAdd==-1):
				error="Error: Directed address of " + opsplit[0] + " not found"
				print(error)
				input()
				exit(0)


			if(length==2 and opsplit[1]=="X"):
				string=dirAdd
				a = string[:1]
				b = string[1:]
				
				a = int(a)
				a = a + 8
				a = "{0:b}".format(a)#str(format(a,'#010b'))[2:]
				length = 4-len(a)
			
				a="0"*length + a
				
				
				dirAdd = a+b					 
			
			objLine = opcode + " "+  dirAdd  

		if(sym=="RSUB"):
			write = line[0:4] + "\t\t"+ objLine	

		elif (sym=="WORD"):
			write=" "

		else:
			write = line[0:4] + "\t" + objLine	


		obcd.write(write)				#object code along with instructions
		obcd.write("\n")
		ob.write(objLine)						#only object code file
		ob.write("\n")	
	
	else:
		print("")
		"""x = line.find("\t")  
		y = line[0:x+1]
		alpha = line
		alpha = alpha[::-1]

		beta = alpha.find("\t")
		gamma = alpha[0:beta+1]


		obcd.write(line)
		obcd.write("\n")"""


assemFI.close()
obcd.close()
ob.close()


"""we have written the onj code in apt files now"""
#***************************************************************************#

objCode = open("objCODE.txt","r")

for i in objCode:
	line = i[:-1]
	print(line)

#output file with apt addresses and codes generated
#*****************************************************************************#
get = input()



				
