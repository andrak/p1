import sys
from collections import deque

class Process:
	def __init__(self, inputList):
		self.name = inputList[0]
		self.arrivalTime = inputList[1]
		self.burstTime = inputList[2]
		self.numBurst = inputList[3]
		self.ioTime = inputList[4]
		self.ioFree = 0
		self.totalBurst = self.burstTime * self.numBurst
		self.remainingBurst = self.burstTime * self.numBurst
def qPrint(queue, string):
	out = "[Q"
	if len(queue) == 0 or string == 'doIt':
		out+= " empty]"
	elif(string == ''):
		for i in queue:
			out += " " + i.name
		out+= "]"
	else:
		for i in queue:
			if i.name != string:
				out += " " + i.name
		out += "]"
	return out

def sortInput(fileInput):
	output = {}
	for i in fileInput:
		if i.arrivalTime in output:
			output[i.arrivalTime].append(i)
		else:
			output[i.arrivalTime] = [i]
	return (output, sorted(output))

def RR(fileInput):
	sort = sortInput(fileInput)
	formattedDict = sort[0]
	orderList = sort[1]
	currentProcess = None
	queue = deque()
	blocked = deque()
	count = 0
	processCount = 0
	cT = 0
	cTBool = 0
	print("time {}ms: Simulator started for RR {}".format(count, qPrint(queue,'')))

	while(1):
		if count in orderList:
			for i in formattedDict[count]:
				queue.append(i)
				if(currentProcess):
					print("time {}ms: Process {} arrived {}".format(count, i.name, qPrint(queue,currentProcess.name)))
				else:
					print("time {}ms: Process {} arrived {}".format(count, i.name, qPrint(queue,'')))
		if(len(queue) > 0):
			currentProcess = queue[0]
			left = currentProcess.remainingBurst % currentProcess.burstTime
			if((currentProcess.numBurst-1) > -1 
				and currentProcess.remainingBurst >= left):
				if(cT == 4):
					if not cTBool:
						temp = queue.popleft()
						if len(queue) == 0:
							print("time {}ms: Process {} started using the CPU {}"
								.format(count, currentProcess.name, qPrint(queue,'doIt')))
							queue.appendleft(temp)
						else:
							queue.appendleft(temp)
							print("time {}ms: Process {} started using the CPU {}"
								.format(count, currentProcess.name, qPrint(queue,currentProcess.name)))
					if(currentProcess.remainingBurst == 0):
						cT = -4
						cTBool = 0
						processCount = 0
						print("time {}ms: Process {} terminated {}"
							.format(count, currentProcess.name, qPrint(queue, currentProcess.name)))				
						queue.popleft()
					elif(processCount > 0 and left == 0):
						cT = -4
						cTBool = 0
						processCount = 0
						blocked.append(queue.popleft())	
						currentProcess.numBurst -= 1
						print("time {}ms: Process {} completed a CPU burst; {} to go {}"
							.format(count, currentProcess.name, currentProcess.numBurst, qPrint(queue,'')))
						currentProcess.ioFree = count + currentProcess.ioTime
						print("time {}ms: Process {} blocked on I/O until time {}ms {}"
							.format(count, currentProcess.name, currentProcess.ioFree, qPrint(queue,'')))
					elif processCount < 84:
						currentProcess.remainingBurst -=1
						processCount += 1
						cTBool = 1
					elif(processCount == 84):
						cT = -4
						cTBool = 0
						processCount = 0
						temp = queue.popleft()
						if( len(queue) > 0):
							queue.append(temp)
							print("time {}ms: Time slice expired; process {} preempted with {}ms to go {}"
									.format(count, currentProcess.name, left, qPrint(queue,'')))
						else:
							print("time {}ms: Time slice expired; no preemption because ready queue is empty {}"
									.format(count, qPrint(queue,'doIt')))
							queue.append(temp)
							cTBool = 1
							cT = 4
							processCount = 0
						
		count+=1
		if not cTBool:
			cT += 1
		for i in blocked:
			if(count == i.ioFree):
				blocked.remove(i)
				queue.append(i)
				print("time {}ms: Process {} completed I/O {}"
					.format(count, i.name, qPrint(queue,currentProcess.name)))
				break
		if(count > 1450):
			break

def main(argv):
	file = open(argv[0])

	'''Block of code to make input usable'''
	formattedInput = []
	for line in file:
		if(line[0] == "#"):
			continue
		temp = line.replace("\n","")
		temp = temp.split("|")
		for i in temp:
			try:
				temp[temp.index(i)] = int(i)
			except ValueError:
				continue
		formattedInput.append(Process(temp))
	RR(formattedInput)

if __name__ == "__main__":
	main(sys.argv[1:])