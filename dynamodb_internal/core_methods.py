class dynamodb_core:
    def __init__(self, creds) -> None:
        self.client = creds.client('dynamodb', 'us-west-2')
        pass

    def get_table_names_as_list(self):
        response = self.client.list_tables()
        return response['TableNames']
    # def update_key(self, modify_command):

    def get_count(self, table_name):
        response = self.client.scan(
            TableName=table_name,
            Select='COUNT'  # This instructs DynamoDB to return only the count, not the items
        )
        count = response['Count']
        while 'LastEvaluatedKey' in response:
            response = self.client.scan(
                TableName=table_name,
                Select='COUNT',
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            count = count + response['Count']
        return count

    def get_count_with_filter(self, table_name, filter_expression, expression_attribute_names, expression_attribute_values):
        if expression_attribute_values == "":
            response = self.client.scan(
                TableName=table_name,
                Select='COUNT',
                FilterExpression=filter_expression,
                ExpressionAttributeNames=expression_attribute_names)
            count = response['Count']
            while 'LastEvaluatedKey' in response:
                response = self.client.scan(
                    TableName=table_name,
                    Select='COUNT',
                    FilterExpression=filter_expression,
                    ExpressionAttributeNames=expression_attribute_names,
                    ExclusiveStartKey=response['LastEvaluatedKey']
                )
                count = count + response['Count']
            return count
        else:
            response = self.client.scan(
                TableName=table_name,
                Select='COUNT',
                FilterExpression=filter_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values)
            count = response['Count']
            while 'LastEvaluatedKey' in response:
                response = self.client.scan(
                    TableName=table_name,
                    Select='COUNT',
                    FilterExpression=filter_expression,
                    ExpressionAttributeNames=expression_attribute_names,
                    ExpressionAttributeValues=expression_attribute_values,
                    ExclusiveStartKey=response['LastEvaluatedKey']
                )
                count = count + response['Count']
            return count
