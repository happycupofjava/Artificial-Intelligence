from sys import argv

given = False
event = []
observations = []
for i in range(1,len(argv)):
	
    if argv[i] == "given":
        given = True
        continue
    event.append(argv[i])

    if given:
        observations.append(argv[i])
#print("Observations entered"+str(event))

class BayesianNodes(object):
    def prob(self, B, E, A, J, M):
        probability = (self.probabilityValues("B",B,None,None) * self.probabilityValues("E",E,None,None) * self.probabilityValues("A|B,E",A,B,E) * self.probabilityValues("J|A",J,A,None) * self.probabilityValues("M|A",M,A,None))
        return probability

    def probabilityValues(self,event,value1,value2,value3):
        if event == "B":
            if value1:
                return 0.001
            else:
                return 0.999

        if event == "E":
            if value1:
                return 0.002
            else:
                return 0.998

        if event == "A|B,E":
            if value2 and value3:
                var = 0.95
            if value2 and not value3:
                var = 0.94
            if not value2 and value3:
                var = 0.29
            if not value2 and not value3:
                var = 0.001
            if value1:
                return var
            else:
                return (1-var)

        if event == "J|A":
            if value2:
                var = 0.9
            else:
                var = 0.05
            if value1:
                return var
            else:
                return (1-var)

        if event == "M|A":
            if value2:
                var = 0.7
            else:
                var = 0.01
            if value1:
                return var
            else:
                return (1-var)

    def calculate(self, variables):
        if not None in variables:
            return self.prob(variables[0],variables[1],variables[2],variables[3],variables[4])
        else:
            index_none = variables.index(None)
            nextEvent = list(variables)
            nextEvent[index_none] = True
            value1 = self.calculate(nextEvent)
            nextEvent[index_none] = False
            value2 = self.calculate(nextEvent)
            return value1 + value2

    def ProbValues(self,variables):
        probability = []
        if "Bt" in variables:
            probability.append(True)
        elif "Bf" in variables:
            probability.append(False)
        else:
            probability.append(None)
        if "Et" in variables:
            probability.append(True)
        elif "Ef" in variables:
            probability.append(False)
        else:
            probability.append(None)
        if "At" in variables:
            probability.append(True)
        elif "Af" in variables:
            probability.append(False)
        else:
            probability.append(None)
        if "Jt" in variables:
            probability.append(True)
        elif "Jf" in variables:
            probability.append(False)
        else:
            probability.append(None)
        if "Mt" in variables:
            probability.append(True)
        elif "Mf" in variables:
            probability.append(False)
        else:
            probability.append(None)

        return probability

bayesNetwork = BayesianNodes()

if event:
    num = bayesNetwork.calculate(bayesNetwork.ProbValues(event))
    if observations:
        observation_value = bayesNetwork.calculate(bayesNetwork.ProbValues(observations))
    else:
        observation_value = 1
    print("Probability for "+str(event)+"= %.9f" % (num/observation_value))

else:
    print("Incorrect input!")