#determining protein class (3rd element) by clusters of native sequences (block ID)
#protein class is 1 if homologous to the native sequence, 0 if non-homologous(decoys)

import sys

#Highest unit, made up of examples
class Block:
  def __init__(self, block_id):
    self.id = block_id
    self.examples = []
    
  def addExample(self, example):
    self.examples.append(example)
  
#Secondary unit, belongs to parent block, contains feature data  
class Example:
  def __init__(self, parent_block, example_id, protein_class, features):
    self.parent = parent_block
    self.id = example_id
    self.protein_class = protein_class
    self.features = features #Array of feature data

def load_kdd(filename):
  with open(filename, 'r') as kdd_set:
    for line in kdd_set:
      values = line.split()
      
      block_id = values[0]        #First value is Block ID, multiple lines per Block ID
      example_id = values[1]      #Second value is Example ID, unique per line
      protein_class = values[2]   #Third value is Protein Class (the desired answer)
      feature_values = values[3:] #Remaining 74 values are feature values/data
      
      if block_id not in blocks:
        blocks[block_id] = Block(block_id)

      blocks[block_id].addExample(Example(block_id,example_id,protein_class,feature_values))
	  
def create_coreset(m):
	print("create coreset here")
	
def export_coreset():
	new_line = '' #prevents a newline being printed at the beginning
	export_file = open("export.dat", "w+")
	print("Exporting lightweight coreset...")
	for block in blocks:
		for example in blocks[block].examples:
			export_file.write(new_line+example.parent+'\t'+example.id+'\t'+example.protein_class)
			for value in example.features:
				export_file.write('\t'+value)
			new_line = '\n' #every line after the first has a newline printed
	export_file.close()

blocks = {} 

#parameter checking and assignment
if len(sys.argv) != 2:
	print("Incorrect number of parameters.")
	print("usage: python coresets.py m")
	exit()
else:
	m = sys.argv[1]
	
load_kdd('test_file.dat') #using subset of first 5 lines
export_coreset()