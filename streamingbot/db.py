"""
DynamoDB handler
"""
from typing import Any, Optional

import simplejson as json

from boto3 import resource
from boto3.dynamodb.conditions import Key  #pylint: disable=unused-import


class DynamoDBHandler:
    """ DynamoDB handler """
    def __init__(self, table_name: str) -> None:
        self.table = resource('dynamodb').Table(table_name)

    def get_item(self, attr_name: Any, attr_value: Any) -> Optional[dict]:
        """
        Return rows having indexed attribute name with value (None if none)
        """
        resp = self.table.get_item(
            Key={attr_name: attr_value}
        )
        return json.loads(json.dumps(resp.get('Item')))

    def put_item(self, **kwargs: Any) -> Any:
        """ Add a new entry into the table """
        return self.table.put_item(Item=kwargs)

    def delete_item(self, attr_name: Any, attr_value: Any) -> Any:
        """ Delete entry having primary key attribute name with value """
        return self.table.delete_item(
            Key={attr_name: attr_value}
        )

    def scan(self) -> Optional[dict]:
        """ Return all rows in the table """
        resp = self.table.scan()
        return json.loads(json.dumps(resp.get('Items')))
