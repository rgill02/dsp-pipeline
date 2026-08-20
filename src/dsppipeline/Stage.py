################################################################################
###                                 Imports                                  ###
################################################################################
#Standard imports
from abc import ABC, abstractmethod
import time
import multiprocessing

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
		#Keep track of how many data chunks we have processed and how long it 
		#took
		self.num_proc = 0
		self.duration = 0

		#Queue to get input data from
		self.inq = multiprocessing.Queue()

		#Queues to put data in
		self.outqs = []

	############################################################################
	def get_inq(self):
		"""
		Getter for the input queue

		Returns
		-------
		inq : multiprocessing.Queue
			Input queue
		"""
		return self.inq

	############################################################################
	def add_outq(self, outq):
		"""
		Adds another output queue to the list

		Parameters
		----------
		outq : multiprocessing.Queue
			Output queue to add to list of output queues
		"""
		self.outqs.append(outq)

	############################################################################
	@abstractmethod
	def process(self, data_in=None):
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
	def cleanup(self):
		"""
		To be overridden to perform any needed cleanup
		"""
		pass

	############################################################################
	def die(self):
		"""
		Call the cleanup method and do our own cleanup and die
		"""
		for outq in self.outqs:
			outq.put(None)

		proc_time = self.avg_proc_time()
		if proc_time is not None:
			print("%s Average Proc Time: %.3f ms" % (self.__class__.__name__, proc_time / 1e-3))

		self.inq.close()

		self.cleanup()

	############################################################################
	def run(self):
		"""
		This method is called by the code running the pipeline. It pulls data 
		from the input queue, passes it to the process function, and stores the 
		result in the output queues. Queues are blocking. It does this in a 
		loop. Once "None" is received the loop breaks and this stage shuts down.

		Returns
		-------
		avg_proc_time : float
			Average time to run the process function in seconds
		"""
		while True:
			#Pull data from input queue
			data_in = self.inq.get()
			if data_in is None:
				break

			#Process the data
			start_time = time.monotonic()
			data_out = self.process(data_in)
			end_time = time.monotonic()
			self.duration += end_time - start_time

			#Increment count
			self.num_proc += 1

			#Store the output in the output queue
			for outq in self.outqs:
				outq.put(data_out)

		self.die()

	############################################################################
	def avg_proc_time(self):
		"""
		Gets the average time to run the process method

		Returns
		-------
		avg_time : float
			Average process time in seconds
		"""
		if self.num_proc == 0:
			return None
		return self.duration / self.num_proc

################################################################################
###                             Pipeline Source                              ###
################################################################################
class Source(Stage):
	"""
	Specific type of stage that is at the beginning of a pipeline and is a 
	source of data. This might be some sort of file reader, subscriber client, 
	etc.
	"""
	############################################################################
	def __init__(self, max_q):
		"""
		Creates a new Source

		Parameters
		----------
		max_q : int
			Maximum watermark for output queue
		"""
		self.max_q = int(max_q)
		super().__init__()

	############################################################################
	def run(self):
		"""
		This method pulls the data from its source and puts it in its output 
		queues.
		"""
		while True:
			#Pull data from source
			start_time = time.monotonic()
			data_out = self.process()
			end_time = time.monotonic()
			self.duration += end_time - start_time

			#Increment count
			self.num_proc += 1

			#Store the output in the output queue
			for outq in self.outqs:
				while outq.qsize() >= self.max_q:
					time.sleep(0.1)
				outq.put(data_out)

			if self.inq.qsize() > 0 or data_out is None:
				break

		self.die()		

	############################################################################
	def send_stop(self):
		"""
		Triggers message to send "None" to all output queues and then shuts 
		down loop
		"""
		self.inq.put(None)

################################################################################
###                             Pipeline Source                              ###
################################################################################
class Sink(Stage):
	"""
	Specific type of stage that is at the end of a pipeline and is a 
	sink of data. This might be some sort of file writer, plotter, etc.
	"""
	############################################################################
	def run(self):
		"""
		This method is called by the code running the pipeline. It pulls data 
		from the input queue, passes it to the process function. It does this 
		in a loop. Once "None" is received the loop breaks and this stage shuts 
		down.
		"""
		while True:
			#Pull data from input queue
			data_in = self.inq.get()
			if data_in is None:
				break

			#Process the data
			start_time = time.monotonic()
			data_out = self.process(data_in)
			end_time = time.monotonic()
			self.duration += end_time - start_time

			#Increment count
			self.num_proc += 1

		self.die()

################################################################################
###                               End of File                                ###
################################################################################