################################################################################
###                                 Imports                                  ###
################################################################################
#Standard imports
from abc import ABC, abstractmethod
import multiprocessing

################################################################################
###                                Pipeline                                  ###
################################################################################
class Pipeline(ABC):
	"""
	Represents a processing pipeline. A pipeline consists of one or more 
	Stages. It creates a queue at the input, output, and between all 
	processing stages, and handles passing data from queues to process 
	functions in the various stages.
	"""
	############################################################################
	def __init__(self, stages):
		"""
		Creates a new Pipeline

		Parameters
		----------
		stages : list
			List of Stages to run in order
		cb
		"""
		#Save args
		self.stages = stages

		#Create queues
		self.qs = []
		for ii in range(len(self.stages)):
			self.qs.append(multiprocessing.Queue())
		self.qs.append(multiprocessing.Queue())

		#Create variable to store processes
		self.procs = []

	############################################################################
	def get_output_q(self):
		"""
		Getter for the output queue

		Returns
		-------
		outq : multiprocessing.Queue:
			Output queue
		"""
		return self.qs[-1]

	############################################################################
	def start(self):
		"""
		Starts all of the stages of the pipeline and starts passing data 
		through them via the input queue
		"""
		#Create processes
		for ii in range(len(self.stages)):
			stage = self.stages[ii]
			pargs = (self.qs[ii], self.qs[ii+1])
			new_proc = multiprocessing.Process(target=stage.run, args=pargs)
			self.procs.append(new_proc)

		#Start processes
		for p in self.procs:
			p.start()

	############################################################################
	def put(self, data_in):
		"""
		Adds data to the input queue. Is blocking

		Parameters
		----------
		data_in : object
			Data to add to the input queue
		"""
		self.qs[0].put(data_in)

	############################################################################
	def stop(self):
		"""
		Starts a clean shutdown sequence by adding "None" to the input
		"""
		#Send shutdown message
		self.qs[0].put(None)

		#Join all processes
		for p in self.procs:
			p.join()

################################################################################
###                               End of File                                ###
################################################################################