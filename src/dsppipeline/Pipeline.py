################################################################################
###                                 Imports                                  ###
################################################################################
#Standard imports
from abc import ABC, abstractmethod
import multiprocessing

#Our imports
from . import Stage, Source, Sink

################################################################################
###                            Helper Functions                              ###
################################################################################
def create_pipeline(stages):
	"""
	Takes in a list of stages and creates the processes that 
	represent a pipeline. Takes in a list of stages where the initial Source 
	should be excluded. Works recursively. If a stage is the wrong type for its 
	placement then it throws a TypeError. Last stage of every branch must be a 
	Sink or another branch

	Parameters
	----------
	stages : list
		Nested list of stages

	Returns
	-------
	procs : list
		List of multiprocessing.Process objects representing a process for each 
		stage
	inq : list
		List of input multiprocessing.Queues to this branch/pipeline
	"""
	#Variables to hold outputs
	procs = []
	first_is_branch = False
	first_qs = None

	#Loop through list
	n = len(stages)
	for ii in range(n):
		cur_stage = stages[ii]

		#Check if we are looking at a branch or a stage
		if isinstance(cur_stage, tuple) or isinstance(cur_stage, list):
			#We are looking at a branch so ensure its the last element in this 
			#list
			if ii != (n - 1):
				raise TypeError("Branch must be last element in list")
			#Process every line in branch
			qs = []
			for jj in range(len(cur_stage)):
				new_procs, new_qs = create_pipeline(cur_stage[jj])
				procs.extend(new_procs)
				qs.extend(new_qs)
			if ii == 0:
				first_is_branch = True
				first_qs = qs
			else:
				for jj in range(len(qs)):
					stages[ii - 1].add_outq(qs[jj])
		else:
			#We are looking at a stage so ensure its a stage and not a Source
			if not isinstance(cur_stage, Stage) \
			   or isinstance(cur_stage, Source):
				raise TypeError("Expected list of Stages (no Sources)")
			#Ensure last stage is a Sink
			if ii == (n - 1) and not isinstance(cur_stage, Sink):
				raise TypeError("Last stage must be a Sink")

			#Create process
			new_proc = multiprocessing.Process(target=cur_stage.run)
			procs.append(new_proc)
			if ii != 0:
				#Point output of previous stage here
				stages[ii - 1].add_outq(cur_stage.get_inq())

	return procs, first_qs if first_is_branch else [stages[0].get_inq()]

################################################################################
###                                Pipeline                                  ###
################################################################################
class Pipeline(ABC):
	"""
	Represents a processing pipeline. A pipeline consists of a Source, and then 
	one or more Stages and Sinks. The data is loaded from the Source, passed 
	through to all the stages via queues, and then passed to the Sink(s). All 
	of the stages are run in separate processes. Can also handle branching.
	"""
	############################################################################
	def __init__(self, stages):
		"""
		Creates a new Pipeline

		Parameters
		----------
		stages : list
			List of Stages to run in order. The very first stage in this list 
			must be a Source. There can only be one source in this list. The 
			next stages can be a regular Stage or a tuple of lists to create a 
			branch. Each branch is a list of stages. The last stage of every 
			branch must be a Sink.
		"""
		#Save args
		self.stages = stages

		#Check that the first stage is a source
		if not isinstance(stages[0], Source):
			raise TypeError("First stage must be a 'Source'")

		#Create pipeline with processes
		self.procs = [multiprocessing.Process(target=stages[0].run)]
		new_procs, inqs = create_pipeline(stages[1:])
		self.procs.extend(new_procs)
		for ii in range(len(inqs)):
			stages[0].add_outq(inqs[ii])

	############################################################################
	def start(self):
		"""
		Starts all of the stages of the pipeline and starts passing data 
		through them
		"""
		#Start processes
		for p in self.procs:
			p.start()

	############################################################################
	def stop(self):
		"""
		Starts a clean shutdown sequence by adding "None" to the input
		"""
		#Send shutdown message
		self.stages[0].send_stop()

		#Join all processes
		self.wait()

	############################################################################
	def wait(self):
		for p in self.procs:
			p.join()

################################################################################
###                               End of File                                ###
################################################################################