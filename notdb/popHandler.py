def popDN(d:dict, n:str, element_index:int=-1):
   ''' pop an element from a list using dot notation '''
   elements = n.split('.')
   thisValue = None

   if len(elements) == 1:
      return d[n].pop(element_index)

   for ele in elements:
      if thisValue == None:
         thisValue = d[ele]
      else:
         thisValue = thisValue[ele]

   return thisValue.pop(element_index)