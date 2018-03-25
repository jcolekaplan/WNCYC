import boto3
from boto3.dynamodb.conditions import Key, Attr

class DynamoTable(object):
    
    """Initialize table
       Can be buildings, machines, users
    """
    def __init__(self, tableType):
        allowedTableTypes = ['Buildings', 'Machines', 'Users']
        if tableType not in allowedTableTypes:
            raise ValueError('Invalid table type! Must be one of: {}'.format(allowedTableTypes))
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table(tableType)

    def put(self, Info):
        self.table.put_item(Item=vars(Info))
    
    def get(self, **kwargs):
        
        if len(kwargs) != 1:
            raise ValueError('No key found or too many given')
        
        else:
            keyStr = list(kwargs.keys())[0]
            keyInfo = kwargs.get(keyStr)
            getInfo = self.table.get_item(Key={keyStr: keyInfo})
            return getInfo
    
    def scan(self):
        return self.table.scan()
    
    def scanf(self, filterExpression):
        return self.table.scan(FilterExpression=filterExpression)