#determining protein class (3rd element) by clusters of native sequences (block ID)
#protein class is 1 if homologous to the native sequence, 0 if non-homologous(decoys)

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
      print(len(blocks[block_id].examples)) #Test print

blocks = {}      
load_kdd('test_file.dat') #using subset of first 5 lines