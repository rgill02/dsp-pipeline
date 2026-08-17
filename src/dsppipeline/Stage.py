################################################################################
###                                 Imports                                  ###
################################################################################
#Standard imports
from abc import ABC, abstractmethod

################################################################################
###                              Pipeline Stage                              ###
################################################################################
class Stage(ABC):
	"""
	Represents a stage of a processing pipeline. Each stage contains a function 
	called "process" that takes in data, processes, and outputs said data. All 
	other information the stage needs to work should come into the constructor
	"""
	############################################################################
	def __init__(self):
		"""
		Creates a new Stage
		"""
		#Keep track of how many data chunks we have processed
		self.num_proc = 0

	############################################################################
	@abstractmethod
	def process(self, data_in):
		"""
		Abstract method that child must implement. Takes in data, processes it, 
		and returns processed data

		Parameters
		----------
		data_in : object
			Data to be processed

		Returns
		-------
		data_out : object
			Processed data
		"""
		raise NotImplementedError("This method must be overridden")

	############################################################################
	def run(self, inq, outq):
		"""
		This method is called by the code running the pipeline. It pulls data 
		from the input queue, passes it to the process function, and stores the 
		result in the output queue. Queues are blocking. It does this in a 
		loop. Once "None" is received the loop breaks and this stage shuts down.

		Parameters
		----------
		inq : multiprocessing.Queue
			Input queue to pull data from
		outq : multiprocessing.Queue
			Output queue to pull data from
		"""
		while True:
			#Pull data from input queue
			data_in = inq.get()
			if data_in is None:
				outq.put(None)
				break

			#Process the data
			data_out = self.process(data_in)

			#Store the output in the output queue
			outq.put(data_out)

			#Increment count
			self.num_proc += 1

################################################################################
###                               End of File                                ###
################################################################################