#1
from typing import Dict, List, Callable, Optional, Any
from dataclasses import dataclass, field
from enum import Enum, auto
from datetime import datetime
import re
import json


class AgentState(Enum):
	IDLE = auto()
	PLANNING = auto()
	THINKING = auto()
	ACTING = auto()
	OBSERVING = auto()
	REFLECTING = auto() 
	CRITIQUING = auto()
	FINISHED = auto()
	FAILED = auto()

#2

@dataclass
class MemoryEntry:
	role: str
	content: str
	timestamp: str = field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))

class AgentMemory:
	def __init__(self):
		self.short_term: List[MemoryEntry] = []
		self.episodic: List[str] = []   #High-level past successes/failures
		self.long term: Dict[str, str] = {} #Simple key-value knowledge that grows
		self.current_plan: List[str] = []
		self.tool_cache: Dict [str, str] = {} #Cache tool results

def add(self, role: str, content: str):
	self.short_term.append(MemoryEntry(role=role, content=content))

def get_context(self, last_n: int 15) -> str:
	recent = self.short_term[-last_n:]
	return "\n".join(f"[{e.timestamp}] {e.role.upper()}: {e.content}" for e in recent)

def remember_fact(self, key: str, value: str):
	self.long_term[key.lower()] = value

def recall(self, key: str) -> Optional[str]:
	return self.long_term.get(key.lower())

def add_episode(self, summary: str):
	self.episodic.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} | {summary}")

def cache_tool(self, tool_name: str, inp: str, result: str):
	self.tool_cache[f" {tool_name}::{inp.lower().strip()}"] = result	

def get_cached(self, tool_name: str, inp: str) -> Optional [str]:
	return self.tool_cache.get(f"{tool_name}::{inp.lower().strip()}")	

#3. tools

def calculator_tool (expression: str) -> str:
	try:
		allowed set("0123456789+-*/().%")
		if not all(c in allowed for c in expression):
			return "Error: Invalid characters"
		return f"Result = {eval (expression)}"
	except Exception as e:
		return f"Calculation error: {e}"

def weather_tool(city: str) -> str:
	data = {
	"mumbai": "32°C, humid, partly cloudy (Humidity 78%)",
	"delhi": "38°C, hot and dry",
	"bangalore": "26°C, pleasant with light rain",
	"chennai": "34°C, very humid",
	"hyderabad": "33°C, clear skies",
	"pune": "29°C, cloudy",
	"kolkata": "33°C, overcast",
	}
	return data.get(city.lower().strip(), f"No data for '{city}'. Try: Mumbai, Delhi, Bangalore, Chennai, Hyderabad, Pune, Kolkata")

def time_tool(_: str = "") -> str:
	return datetime.now().strftime("Current time: %A, %d %B %Y | %I: %M:%S %p")

def search_tool (query: str) -> str:
	knowledge = {
	"python inventor": "Guido van Rossum created Python (first released 1991).",
	"react pattern": "ReAct = Reason Act. The agent interleaves thinking and tool use.",
	"capital of india": "New Delhi is the capital of India.",
	"largest planet": "Jupiter is the largest planet in our solar system.",
	"langchain": "LangChain is a framework for building LLM applications and agents.",
	"crewai": "CrewAI helps you build multi-agent teams that collaborate.",
	"ai agent formula": "AI Agent = LLM (Brain) + Memory + Tools + Planning + Action Loop",
	"reflexion": "Reflexion is a technique where the agent critiques its own previous attempts and improves.",
	}

	q = query.lower()
	for k, v in knowledge.items():
		if k in q:
			return v
		return f"No precise match found for '(query) in knowledge base."
	except Exception as e:
		return f"Code error: {e}"

def file_tool(command: str) -> str:
	cmd = command.lower().strip()
	if cmd == "list":
		return "Files: note.txt | todo.md | research.md | agent_memory.json"
	if "notes" in cmd:
		return "notes.txt 'Focus on Tools + Memory + Planning. Start simple, then add complexity.'"
	if "todo" in cmd:
		return "todo.md 1. Finish agent loop 2. Add reflection 3. Try multi-agent next"
	if "research" in cmd:
		return "research.md 'ReAct is still the most practical starting pattern in 2025-26."
	return "Supported: list | read notes | read todo | read research"

TOOLS: Dict[str, Callable] = {
    "calculator": calculator_tool
    "weather": weather tool,
    "time": time_tool,
    "search": search_tool,
    "code": code_tool
    "file": file_tool,
}

#4 brain

class Brain:
	def create_plan(self, goal: str) -> List[str]:
		g = goal.lower()
		plan = []

		if "weather" in g:
			plan.append("Identify the city and call weather tool")
		if any(wing for win ["calculate", "math", "compute", "+", "*", "/"]):
			plan.append("Extract expression and use calculator")
		if any(wing for win ["time", "date", "today"]):
			plan.append("Call time tool")
		if any(wing for win ["file", "notes", "todo", "research"]):
			plan.append("Use file tool to read the requested document")
		if any(wing for win ["who", "what", "capital", "invented", "largest", "formula", "react", "langchain"]): 
			plan.append("Search knowledge base for the fact")

		if not plan:
			plan ["Understand goal", "Choose appropriate tool(s)", "Execute and collect results"]

		plan.append("Synthesize all information into a clear final answer")
		return plan

	def think(self, goal: str, context: str, last_obs: str, remaining_plan: List[str]) -> str:
		"""Returns Thought + Action in ReAct style, aware of the plan"""
        g = goal.lower()

    #---Reflection trigger---#
    if last obs and ("error" in last_obs.lower() or "no data" in last_obs.lower() or "no precise" in last_obs.lower()):
    	return (
    		"Thought: Previous action did not give useful information."
    		"I should try a different tool or rephrase the query.\n"
    		"Action: search\n"
    		f"Action Input: {goal}"
    	)
    	#Follow the plan when possible
    	if remaining plan:
    		next_step = remaining_plan[@].lower()

    		if "weather" in next_step:
    			cities ["mumbai", "delhi", "bangalore", "chennai", "hyderabad", "pune", "kolkata"] 
    			city = next((c.title() for c in cities if c in g), "Mumbai") 
    			return f"Thought: Following plan - get weather.\nAction: weather \nAction Input: {city}"

    		if "calculator" in next_step or "expression" in next_step:
    			match = re.search(r" [\d\+\-\*/\(\)\.\s]+", goal) 
    			expr = match.group().strip() if match else "2+2"
    			return f"Thought: Following plan perform calculation.\nAction: calculator\nAction Input: {expr}"

    		if "time" in next_step:
    			return "Thought: Following plan get current time.\nAction: time\nAction Input: "

    		if "file" in next_step:
    			if "todo" in g:
    				return "Thought: Following plan read todo. AnAction:file\nAction Input: read todo"
    			if "research" in g:
    				return "Thought: Following plan read research notes. InAction: file\nAction Input: read research"
    			if "notes" in g:
    				return "Thought: Following plan read notes.\nAction: file\nAction Input: read notes"
    			return "Thought: Following plan list files.\nAction: file\nAction Input: list"

    	if "search" in next_step or "knowledge" in next_step:
    		return f"Thought: Following plan search for information.\nAction: search\nAction Input: {goal}"

    	#Fallback tool selection
    	if any(w in g for w in ["calculate", "+", "/"]):
    		match = re.search(r"[\d\+\-\*/\(\)\.\s%]+", goal)
    		expr = match.group().strip() if match else "2+2"
    		return f"Thought: I need to calculate.\nAction: calculator\nAction Input: {expr}"

    	if "weather" in g:
    		return "Thought: Weather requested.\nAction: weather\nAction Input: Mumbai"

    	if any(w in g for win ["time", "date"]):
    		return "Thought: Time requested.\nAction: time\nAction Input:"

    	return f"Thought: I will search for relevant knowledge.\n Action: search \nAction Input: {goal}"

    def reflect(self, goal:str, observations: List[str], plan: List[str])  -> str:
    	if not observations:
    		return "Reflection: No observations yet. I should start executing the plan"
    	last = observation[-1].lower()
    	if "error" in last or "no data" in last:
    		return "Reflection: Last tool call failex. I will adjust the plan and try an alternate approach."
    	return "Reflecton: Progress looks good. I can continue or move toward the final answer"

    def critique(self, goal: str, observations: List[str]) -> str:
    	if len(observation) == 0:
    		return "Critique: Insufficient information gathered."
    	return "Critique: The collected observations appear relevant and sufficient to answer the user."

    def final_answer(self, goal: str, observations: List[str]) -> str:
    	unique_obs = []
    	for o in observations:
    		if o not in unique_obs:
    			unique_obs.append(o)
    	combined = "\n• ".join(unique_obs)
    	return f"Answer to: \"{goal}\"\n• {combined}"

# =======================================================================
# 5. THE AGENT (More complex orchestration)
# =======================================================================

class ComplexAIAgent:
    def __init__(self, max_steps: int = 10):
        self.memory = AgentMemory()
        self.brain = Brain()
        self.max_steps = max_steps
        self.state = AgentState.IDLE
        self.observations: List[str] = []
        self.trajectory: List[str] = []

    def _log(self, msg: str):
    	print(msg)
    	self.trajectory.append(msg)

    def _parse_react(self, text: str) -> tuple[Optional[str], str]:
    	action, action_input = None,
    	for line in text.splitlines():
    		line = line.strip()
    		if line.lower().startswith("action:"):
    			action = line.split(":", 1)[1].strip().lower()
    		elif line.lower().startswith("action input:"):
    			action_input = line.split(":", 1)[1].strip()
    	return action, action_input

    def run(self, user goal: str) -> str:
    	self.state = AgentState.PLANNING
    	self.observations = []
    	self.trajectory = []
    	self.memory.short_term.clear()
    	self.memory.add("user", user_goal)

    	self. log("\n" +"-"*72)
    	self.log(f"🎯 GOAL: {user_goal}") 
    	self. log("-"*72)

    	#--------------PLANNING-----------
    	plan = self.brain.create_plan(user_goal)
    	self.memory.current_plan plan.copy()
    	self._log("\n INITIAL PLAN:")
    	for i, step in enumerate (plan, 1):
    		self. log(f"  {i}. {step}")

    	remaining_plan plan.copy()
    	last_obs = ""

    	for step_num in range(1, self.max_steps + 1):
    		self._log(f"\n Step {step_num}/{self.max_steps} ")

    		#THINKING
    		self.state = AgentState.THINKING
    		context = self.memory.get_context()
    		thought = self.brain.think(user_goal, context, last_obs, remaining_plan)
    		self. log(f" {thought}")
    		self.memory.add("thought", thought)

    		action, action_input = self._parse_react(thought)

    		if not action or action not in TOOlS:
    			self.state = AgentState.REFLECTING
    			reflection = self.brain.reflect(user_goal, self,observations, remaining_plan)
    			self.log(f" {reflection}")
    			self.memory.add("reflection", reflection)
    			continue
    		#Check cache first
    		cached self.memory.get_cache(action, action_input)
    		if cached:
    			result= f"[CACHED] {cached}"
    			self._log(f" Using cached result for {action}")
    		else:
    			#ACTING
    			self.state = Agent5tate.ACTING
    			self._log(f"Action: {action}(\"{action_input}\")")
    			self.memory.add("action", f"{action}({action_input})")

    			try:
    				result = TOOLS[action](action_input)
    				self.memory.cache_tool(action, action_input, result)
    			except Exception as e:
    				result = f"Tool exceptions {e}"


    				if useful and (not remaining plan or step_num > 3):
    				#CRITIC step
    				self.state = AgentState.CRITIQUING
    				critique = self.brain.critique(user_goal, self.observations)
    				self._log(f" Critic: {critique}")

    				if "insufficient" not in critique.lower():
    					final = self.brain.final_answer (user_goal, self.observations)
    					self.state = AgentState.FINISHED
    					self._log(f"\n FINAL ANSWER: \n{final}")
    					self.memory.add_episode(f"Success: {user_goal[:50]}")
    					#Store a fact in long-term memory
    					self.memory.remember_fact(user_goal[:40], final [:120])
    					return final

    				#REFLECT after every few steps
    				if step_num % 2 == 0:
    					self.state AgentState.REFLECTING
    					reflection = self.brain.reflect(user_goal, self.observations, remaining_plan)
    					self._log(f" {reflection}")
    					self.memory.add("reflection", reflection)

    			#Max steps
    			self.state = AgentState.FAILED
    			self. log("\n A Max steps reached {safety limit}.")
    			final = self.brain.final answer (user_goal, self.observations)
    			self. log(f"\n BEST-EFFORT ANSWER:\n[final}")
    			self.memory.add episode(f" Partial: {user_goal[:50]}")
    			return final

 #==============================================   			
 #6. DEMO
 #==============================================   	

def main():
print("""
              CodeBloomAPP More Complex Al Agent State Machine Dynamic Planning Reflexion
              Critic Cache

""")
    agent = ComplexATAgent(max_steps=8)

    print("Example goals you can try:")
    print("What is the weather in Bangalore and also calculate 18 7?")
    print("Tell me the current time and who invented Python")
    print("• Read the todo list and the research notes")
    print("What is the Al agent formula?")
    print("Calculate (2515) 3 and then tell me the capital of India")
    print("\nType 'quit' to exit | 'memory' to see long-term memory\n")

    while True:
    	user = input("Your Goal ").strip()
    	if user.lower() in ["quit", "exit", "q"]:

    		print("Goodbyel Keep going deeper into agents")
    			break

    	if user.lower() == "memory":
    		print("\nLong-term memory:")
    		for k, v in agent.memory.long_torm.items():
    			print (f" {k} {v[:80]}...")
    			print("\n Episodic memory:")
    		for e in agent..memory.episodic[-5:]:
    			print(f" {e}")
    		continue
    	if not user:
    		continue

    		agent.run(user)
    		print("\n"+""*72)

if __name__ == "__main__":
	main()