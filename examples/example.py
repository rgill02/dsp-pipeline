################################################################################
###                                 Imports                                  ###
################################################################################
#Standard imports
import os
import sys
import time

#Our imports
from dsppipeline import Stage, Source, Sink
from dsppipeline import Pipeline

################################################################################
###                              Example Stages                              ###
################################################################################
class Example_Source(Source):
	"""
	Generates incremental numbers
	"""
	def __init__(self):
		super().__init__(10)
		self.count = 0

	def process(self, data_in=None):
		self.count += 1
		return self.count

class Add_Sub(Stage):
	"""
	Adds or subtracts a number from the incoming data
	"""
	def __init__(self, x):
		self.x = x
		super().__init__()

	def process(self, data_in):
		return data_in + self.x

class Example_Sink(Sink):
	"""
	Prints received numbers out to stdout
	"""
	def __init__(self, name):
		self.name = name
		super().__init__()

	def process(self, data_in=None):
		print("%s: " % self.name, data_in)

################################################################################
###                             Example Pipeline                             ###
################################################################################
class Example_Pipeline(Pipeline):
	"""
	Generates incremental numbers, multiplies by 2, and prints them to stdout
	"""
	def __init__(self):
		stages = [
			Example_Source(),
			[
				[Add_Sub(0.1), Example_Sink("Add")],
				[Add_Sub(-0.2), Example_Sink("Sub")]
			]
		]
		super().__init__(stages)

################################################################################
###                                  Main                                    ###
################################################################################
if __name__ == "__main__":
	#Create pipeline and run it
	pipeline = Example_Pipeline()
	pipeline.start()

	time.sleep(0.1)

	pipeline.stop()


################################################################################
###                               End of File                                ###
################################################################################