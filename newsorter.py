def sorter(queue):
	c = len(queue) - 1
	while c > 0:
		if c-1 == 0:
			if(queue[c].totalBurst == queue[c].remainingBurst and queue[c-1].totalBurst == queue[c-1].remainingBurst):
				if(queue[c].burstTime < queue[c-1].burstTime):
					temp = queue[c]
					queue[c] = queue[c-1]
					queue[c-1] = temp
					c -= 1
			else:
				break
		elif(queue[c].burstTime < queue[c-1].burstTime):
			temp = queue[c]
			queue[c] = queue[c-1]
			queue[c-1] = temp
			c -= 1
		else:
			break
	return queue