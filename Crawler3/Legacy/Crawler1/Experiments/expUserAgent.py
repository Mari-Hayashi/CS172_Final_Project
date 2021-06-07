import user_agents
import re
import sys

def extractWords(text):
    split_text = test.split("/")
    words = " ".join(re.findall(r"[a-zA-Z]+", split_text))
    return words    

def readAgents(filename):
    with open(filename) as user_file:
        agents = [agent.strip() for agent in user_file.read().split("\n") if agent.strip() != ""]
    print(len(agents))
    return agents

def saveAgents(filename, agents):
    with open(filename, "w") as user_file:
        for agent in agents:    
            user_file.write(agent + "\n")

def countAgents(filename, agents):
    counter = dict()
    for agent in agents:
        name = str(user_agents.parse(agent))
        if name in counter:
            counter[name] += 1
        else:
            counter[name] = 1

    sorted_agents = sorted(counter.items(), key=lambda x:x[1], reverse=True)
    with open(filename, "w") as count_file:
        for i in sorted_agents:
            count_file.write(f"{i} - {counter[i]}\n") 
        
    


if __name__ == "__main__":
    agents = readAgents(sys.argv[1])
    countAgents(sys.argv[2], agents) 
