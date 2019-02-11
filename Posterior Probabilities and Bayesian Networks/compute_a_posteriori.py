
from sys import argv
argumentLength= len(argv)
if argumentLength > 1:
	observations = argv[1]
else:
	observations = ""


outFile = open("result.txt", 'w+')
outFile.write("\nObservation Sequence of Q: %s\n" % observations)
outFile.write("Length of the Q: %i\n" % len(observations))

observations = observations.upper()

observations = " " + observations + "C"
print("Observations recorded:"+observations)



# Computing prior probabilities of the bags
#h1 (prior: 10%): This type of bag contains 100% cherry candies.
#h2 (prior: 20%): This type of bag contains 75% cherry candies and 25% lime candies.
#h3 (prior: 40%): This type of bag contains 50% cherry candies and 50% lime candies.
#h4 (prior: 20%): This type of bag contains 25% cherry candies and 75% lime candies.
#h5 (prior: 10%): This type of bag contains 100% lime candies.

probabilityHypoBags = [{ 'h1':0.1, 'h2':0.2, 'h3':0.4, 'h4':0.2, 'h5':0.1 }]
priorProbability = { 'C|h1':1, 'L|h1':0, 'C|h2':0.75, 'L|h2':0.25, 'C|h3':0.5, 'L|h3':0.5, 'C|h4':0.25, 'L|h4':0.75, 'C|h5':0, 'L|h5':1 
}

probabilityQueries = []

probability= 0

for i in range(1, 6):
	tempProbability= (priorProbability[observations[1] + '|h' + str(i)] * probabilityHypoBags[0]['h' + str(i)])
	probability= probability+ tempProbability


probabilityQueries.append({ observations[1]:probability})
obsLength = len(observations)

for i in range(1, obsLength - 1):
	outFile.write("\nAfter Observation %i = %s:\n" % (i, observations[i]))
	
	if len(probabilityHypoBags) - 1 < i:
		probabilityHypoBags.append({})
	
	if len(probabilityQueries) - 1 < i:
		probabilityQueries.append({})
	
	
	tempProbability= 0

	for j in range(1, 6):
		probabilityHypoBags[i]['h' + str(j)] = priorProbability[observations[i] + '|h' + str(j)] * probabilityHypoBags[i - 1]['h' + str(j)] / probabilityQueries[i - 1][observations[i]]		
		tempProbability= tempProbability+ priorProbability[observations[i + 1] + '|h' + str(j)] * probabilityHypoBags[i]['h' + str(j)]		
		probabilityQueries[i][observations[i + 1]] = tempProbability


        for k in range(1, 6):
	        outFile.write("P(h%d|Q) = %.5f\n" % (k, probabilityHypoBags[-1]["h" + str(k)]))
        

        if observations[i] == "C" and observations[i + 1] == "L":
            pOfNextObs = probabilityQueries[i][observations[i + 1]]
            outFile.write("\nProbability that the next candy we pick will be C, given Q: %.5f\n" % (1.000 - pOfNextObs))
            outFile.write("Probability that the next candy we pick will be L, given Q: %.5f\n" % (pOfNextObs))
        

        elif observations[i] == "L" and observations[i + 1] == "C":
            pOfNextObs = probabilityQueries[i][observations[i + 1]]
            outFile.write("\nProbability that the next candy we pick will be C, given Q: %.5f\n" % pOfNextObs)
            outFile.write("Probability that the next candy we pick will be L, given Q: %.5f\n" % (1.000 - pOfNextObs))
       

        elif observations[i] == observations[i + 1] == "C":
            if probabilityQueries[i][observations[i]] > probabilityQueries[i][observations[i + 1]]:
                pOfNextObs = probabilityQueries[i][observations[i]]
            else:
                pOfNextObs = probabilityQueries[i][observations[i + 1]]
            
            outFile.write("\nProbability that the next candy we pick will be C, given Q: %.5f\n" % pOfNextObs)
            outFile.write("Probability that the next candy we pick will be L, given Q: %.5f\n" % (1.000 - pOfNextObs))
       

        elif observations[i] == observations[i + 1] == "L":
            if probabilityQueries[i][observations[i]] > probabilityQueries[i][observations[i + 1]]:
                pOfNextObs = probabilityQueries[i][observations[i]]
            else:
                pOfNextObs = probabilityQueries[i][observations[i + 1]]
          
            outFile.write("\nProbability that the next candy we pick will be C, given Q: %.5f\n" % (1.000 - pOfNextObs))
            outFile.write("Probability that the next candy we pick will be L, given Q: %.5f\n" % pOfNextObs)




outFile = open("result.txt", "r")
outputFileContents = outFile.read()
print(outputFileContents)
outFile.close()
