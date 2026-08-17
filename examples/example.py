################################################################################
###                                 Imports                                  ###
################################################################################
#Standard imports
import os
import sys

#Our imports
#EXAMPLE_DIR = os.path.abspath(os.path.dirname(__file__))
#PROJ_DIR = os.path.abspath(os.path.join(EXAMPLE_DIR, ".."))
#LIB_DIR = os.path.abspath(os.path.join(PROJ_DIR, "src", "dsppipeline"))
#sys.path.append(LIB_DIR)
from dsppipeline import Stage
from dsppipeline import Pipeline

################################################################################
###                              Example Stages                              ###
################################################################################
class Add_1_Stage(Stage):
	"""
	Expects a number in, adds 1 to that number, and outputs
	"""
	def process(self, data_in):
		return data_in + 1

class Mult_By_2_Stage(Stage):
	"""
	Expects a number in, multiplies it by 2, and outputs
	"""
	def process(self, data_in):
		return data_in * 2

################################################################################
###                             Example Pipeline                             ###
################################################################################
class Example_Pipeline(Pipeline):
	"""
	Expects a number in, adds 1, multiplies by 2, and then adds 1 again
	"""
	def __init__(self):
		stages = [
			Add_1_Stage(),
			Mult_By_2_Stage(),
			Add_1_Stage()
		]
		super().__init__(stages)

################################################################################
###                                  Main                                    ###
################################################################################
if __name__ == "__main__":
	#Create pipeline and run it
	pipeline = Example_Pipeline()
	outq = pipeline.get_output_q()
	pipeline.start()

	#Feed test data
	n = 10
	for ii in range(n):
		pipeline.put(ii)

	#Pull output data
	for ii in range(n):
		print("Output %d: %d" % (ii, outq.get()))

	#Shutdown
	pipeline.stop()

################################################################################
###                               End of File                                ###
################################################################################