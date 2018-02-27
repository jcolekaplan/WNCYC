import boto3
from boto3.dynamodb.conditions import Key, Attr

class dynamoTable(object):
    
    """Initialize table
       Can be buildings, machines, users
    """
    def __init__(self, tableType):
        allowedTableTypes = ['Buildings', 'Machines', 'Users']
        if tableType not in allowedTableTypes:
            raise ValueError('Invalid table type! Must be one of: {}'.format(allowedTableTypes))
        dynamodb = boto3.resource('dynamodb', region_name = 'us-east-2')
        self.table = dynamodb.Table(tableType)

    def putItem(self, Info):
        self.table.put_item(Item=vars(Info))
    
    def getItem(self, keyInfo, keyStr):
        getInfo = self.table.get_item(Key={keyStr: keyInfo})
        return getInfo
    
    def scanTable(self):
        return self.table.scan()
    
    def scanFilter(self, filterExpression):
        return self.table.scan(FilterExpression=filterExpression)