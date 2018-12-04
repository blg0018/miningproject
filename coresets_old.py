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
    print("Reading in dataset...")
    for line in kdd_set:
      values = line.split()
      
      #string values are converted into proper types and inserted
      block_id = int(values[0])        #First value is Block ID, multiple lines per Block ID
      example_id = int(values[1])      #Second value is Example ID, unique per line
      protein_class = int(values[2])   #Third value is Protein Class (the desired answer)
      feature_values = values[3:]        #Remaining 74 values are feature values/data
      for i in range(len(feature_values)):
        feature_values[i] = float(feature_values[i])
      
      if block_id not in blocks:
        blocks[block_id] = Block(block_id)

      blocks[block_id].addExample(Example(block_id,example_id,protein_class,feature_values))
  print("Reading complete.\n")    

def create_coreset(m):
  print("Creating lightweight coreset...")
  print("---Finding the mean of the data...")
  #-------------------------------------
  #1. Find mu = mean of data points X
  #-------------------------------------
  mean = []
  total_number = 0
  
  for block in blocks:
    for example in blocks[block].examples:
      #if mean is empty, create initial values
      if total_number == 0:
        for i in range(len(example.features)):
          mean.append(float(0))
      
      #add up example values to mean array
      for i in range(len(example.features)):
        mean[i] += example.features[i]
      
      total_number += 1
  #Once mean array is populated, calculate means
  for i in range(len(mean)):
    mean[i] /= total_number

  #-------------------------------------
  #2. Create summation of distances d(x,mean)^2 array
  #-------------------------------------
  print("---Finding differences squared sum between the mean and data values...")
  distances_sum = [] #each value represents the summation of differences between the mean and each value in the dataset squared
  initialized = 0
  
  #Sum up differences for each example, square it, and add to array
  for block in blocks:
    for example in blocks[block].examples:  
      #Initialize distances_sum array
      if initialized == 0:
        for i in range(len(example.features)):
          distances_sum.append(float(0))
        initialized = 1
        
      #Add new distance^2 to array's existing value
      for i in range(len(example.features)):
        distances_sum[i] += abs((mean[i]-example.features[i])**2)
  
  #-------------------------------------
  #3. Create q(x) probability for each example in dataset
  #-------------------------------------
  print("---Creating q(x) probability array...")
  print("Coreset creation complete.\n")
  
def export_coreset():
  new_line = '' #prevents a newline being printed at the beginning
  export_file = open("export.dat", "w+")
  print("Exporting lightweight coreset...")
  for block in blocks:
    for example in blocks[block].examples:
      export_file.write(new_line+str(example.parent)+'\t'+str(example.id)+'\t'+str(example.protein_class))
      for value in example.features:
        export_file.write('\t'+str(value))
      new_line = '\n' #every line after the first has a newline printed
  export_file.close()
  print("Export complete.")

blocks = {} 

#parameter checking and assignment
if len(sys.argv) != 3:
  print("Incorrect number of parameters.")
  print("usage: python coresets.py dataset_filename m")
  exit()
else:
  m = sys.argv[2]
  filename = sys.argv[1]
	
load_kdd(filename)  
create_coreset(m)
export_coreset()
