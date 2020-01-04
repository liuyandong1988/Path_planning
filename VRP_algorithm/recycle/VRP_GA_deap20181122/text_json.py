#!/usr/bin/env python2
import os
import fnmatch
from json import dump

# BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
BASE_DIR = os.path.abspath('.')

def makeDirsForFile(pathname):
    try:
        os.makedirs(os.path.dirname(pathname))
    except:
        pass


def textTojson(customize=False):
    def __distance(customer1, customer2):
        return ((customer1['coordinates']['x'] - customer2['coordinates']['x'])**2 + (customer1['coordinates']['y'] - customer2['coordinates']['y'])**2)**0.5
    if customize:
        textDataDir = os.path.join(BASE_DIR, 'data', 'text_customize')
        jsonDataDir = os.path.join(BASE_DIR, 'data', 'json_customize')
    else:
        textDataDir = os.path.join(BASE_DIR, 'data', 'text')
        jsonDataDir = os.path.join(BASE_DIR, 'data', 'json')
    for textFile in map(lambda textFilename: os.path.join(textDataDir, textFilename), fnmatch.filter(os.listdir(textDataDir), '*.vrp')):
        jsonData = {}
        print textFile
        with open(textFile) as f:
            for lineNum, line in enumerate(f, start=1):
                if lineNum in [2, 3, 4, 5, 7]:
                    pass
                elif lineNum == 1:
                    # <Instance name>
                    jsonData['instance_name'] = line.strip().split()[2]
                    jsonData['max_vehicle_number'] = int(line.strip().split()[2][-1])
                    print jsonData['instance_name'] , jsonData['max_vehicle_number'] 
                elif lineNum == 6:
                    # <Vehicle capacity>
                    jsonData['vehicle_capacity'] = float(line.strip().split()[2])
#                     print jsonData['vehicle_capacity'] 
                elif lineNum == 8:
                    # Custom number = 0, deport
                    # <Custom number>, <X coordinate>, <Y coordinate>
                    values = line.strip().split()
                    jsonData['deport'] = {
                        'coordinates': {
                            'x': float(values[1]),
                            'y': float(values[2]),
                        }
                    } 
#                     print jsonData['deport']
#                     raw_input('prompt')
                elif lineNum in [num for num in xrange(9,40)]:
                    # <Custom number>, <X coordinate>, <Y coordinate>, <Demand>
                    values = line.strip().split()
                    jsonData['customer_%s' % (int(values[0])-1)] = {
                        'coordinates': {
                            'x': float(values[1]),
                            'y': float(values[2]),
                        }
                    }
                elif lineNum == 41:
                    # Custom number = 0, deport
                    # <Demand> 
                    values = line.strip().split()
                    jsonData['deport']['demand'] = float(values[1])
                
                elif lineNum in [num for num in xrange(42,73)]:
                    # <Custom number>, <X coordinate>, <Y coordinate>, <Demand>
                    values = line.strip().split()
                    jsonData['customer_%s' % (int(values[0])-1)]['demand'] = float(values[1])
                else:
                    pass
                             
#         print jsonData['customer_31'] 
#         raw_input('prompt')
                    
        
        customers = ['deport'] + ['customer_%d' % x for x in xrange(1, 32)]
#         print customers
#         raw_input('prompt')
        jsonData['distance_matrix'] = [[__distance(jsonData[customer1], jsonData[customer2]) for customer1 in customers] for customer2 in customers]
        jsonData['all_coordination'] = [(jsonData[customer]['coordinates']['x'], jsonData[customer]['coordinates']['y'] ) for customer in customers]
        jsonFilename = '%s.json' % jsonData['instance_name']
        jsonPathname = os.path.join(jsonDataDir, jsonFilename)
        print('Write to file: %s' % jsonPathname)
        makeDirsForFile( pathname = jsonPathname)
        with open(jsonPathname, 'w') as f:
            dump(jsonData, f, sort_keys=True, indent=4, separators=(',', ': ')) # transform the dic to str put in json

if __name__ == '__main__':
    textTojson()
    
