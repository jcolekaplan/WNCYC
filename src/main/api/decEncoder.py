"""Workaround for formatting issue
   Source: http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.04.html
"""
import decimal
import json

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
