# sample command:
# operation operand --where [ 'key', 'type', 'condition', 'value' ]
# operation = get | add | update | delete
# operand = key | value | count
# get count
# add key, delete key, update key
# update value
from rich_internal.tui import rich_tui
from rich.prompt import Prompt


class commands:
    def __init__(self, dynamodb_client, table_name) -> None:
        self.dd_client = dynamodb_client
        self.table_name = table_name
        pass

    def execute_command(self, command_operation, command_operand, command_filters, console):
        if command_operation.lower() == "get":
            if command_operand.lower() == "count":
                if command_filters == "":
                    count = self.get_table_count()
                    output_string = rich_tui.create_print_string(
                        [("The total count of items for table ", ""), (self.table_name, "cyan italic"), (" is: ", ""), (str(count), "green bold")])
                    return output_string, False
                elif command_filters == "set":
                    choice = Prompt.ask("Is it stable?", default="n",
                                        choices=["y", "n"])
                    if (choice == "y"):
                        return "hell yes! :)"
                    else:
                        return "aww... :/"
                else:
                    count = self.get_table_count_with_where(command_filters)
                    if (len(command_filters) == 3):
                        output_string = rich_tui.create_print_string(
                            [("The total count of items for table ", ""), (self.table_name, "cyan italic"), (" with filters:\n", ""),
                             ("key name \'" + command_filters[0] + "\' with value of type " +
                              command_filters[1] + " " + command_filters[2], "yellow"),
                             ("\nis: ", ""), (str(count), "green bold")])
                    elif (len(command_filters) == 4):
                        output_string = rich_tui.create_print_string(
                            [("The total count of items for table ", ""), (self.table_name, "cyan italic"), (" with filters:\n", ""),
                             ("key name \'" + command_filters[0] + "\' with value of type " + command_filters[1] +
                              " where value " + command_filters[2] + " " + command_filters[3], "yellow"),
                             ("\nis: ", ""), (str(count), "green bold")])
                    elif (len(command_filters) == 5):
                        output_string = rich_tui.create_print_string(
                            [("The total count of items for table ", ""), (self.table_name, "cyan italic"), (" with filters:\n", ""),
                             ("key name \'" + command_filters[0] + "\' of type " + command_filters[1] +
                              " where value " + command_filters[2] + " " + command_filters[3] + " and " + command_filters[4], "yellow"),
                             ("\nis: ", ""), (str(count), "green bold")])
                    else:
                        output_string = rich_tui.create_print_string(
                            [("error: ", "red"), ("filter length of ", ""), (str(len(command_filters)), "red bold"),
                             (" is not correct!", ""), ("\nplease correct filter to length of", ""), (" 3, 4 or 5.", "green bold")])
                    return output_string

    def get_table_count(self):
        return self.dd_client.get_count(self.table_name)

    def get_table_count_with_where(self, filters):
        filter_expression, expression_attribute_names, expression_attribute_values = self.decompose_filter(
            filters)
        if (filter_expression == "") & (expression_attribute_names == "") & (expression_attribute_values == ""):
            return 'error in where'
        return self.dd_client.get_count_with_filter(self.table_name, filter_expression, expression_attribute_names, expression_attribute_values)

    def decompose_filter(self, filters):
        attribute_conditions = filters[2]
        if (attribute_conditions == '=') or (attribute_conditions == 'equal_to'):
            filter_expression = "#attr = :val"
            expression_attribute_names = {"#attr": filters[0]}
            expression_attribute_values = {":val": {filters[1]: filters[3]}}
        elif (attribute_conditions == 'not_equal_to') or (attribute_conditions == '!='):
            filter_expression = "#attr != :val"
            expression_attribute_names = {"#attr": filters[0]}
            expression_attribute_values = {":val": {filters[1]: filters[3]}}
        elif (attribute_conditions == 'less_than_or_equal_to') or (attribute_conditions == '<=') or (attribute_conditions == '=<'):
            filter_expression = "#attr <= :val"
            expression_attribute_names = {"#attr": filters[0]}
            expression_attribute_values = {":val": {filters[1]: filters[3]}}
        elif (attribute_conditions == 'less_than') or (attribute_conditions == '<'):
            filter_expression = "#attr < :val"
            expression_attribute_names = {"#attr": filters[0]}
            expression_attribute_values = {":val": {filters[1]: filters[3]}}
        elif (attribute_conditions == 'greater_than_or_equal_to') or (attribute_conditions == '>=') or (attribute_conditions == '=>'):
            filter_expression = "#attr >= :val"
            expression_attribute_names = {"#attr": filters[0]}
            expression_attribute_values = {":val": {filters[1]: filters[3]}}
        elif (attribute_conditions == 'greater_than') or (attribute_conditions == '>'):
            filter_expression = "#attr > :val"
            expression_attribute_names = {"#attr": filters[0]}
            expression_attribute_values = {":val": {filters[1]: filters[3]}}
        elif attribute_conditions == 'contains':
            filter_expression = "contains(#attr, :val)"
            expression_attribute_names = {"#attr": filters[0]}
            expression_attribute_values = {":val": {filters[1]: filters[3]}}
        elif attribute_conditions == 'not_contains':
            filter_expression = "not contains(#attr, :val)"
            expression_attribute_names = {"#attr": filters[0]}
            expression_attribute_values = {":val": {filters[1]: filters[3]}}
        elif attribute_conditions == 'between':
            filter_expression = "#attr between :val1 and :val2"
            expression_attribute_names = {"#attr": filters[0]}
            expression_attribute_values = {
                ":val1": {filters[1]: filters[3]}, ":val2": {filters[1]: filters[4]}}
        elif attribute_conditions == 'exists':
            filter_expression = "attribute_exists(#attr)"
            expression_attribute_names = {"#attr": filters[0]}
            expression_attribute_values = ""
        elif attribute_conditions == 'not_exists':
            filter_expression = "attribute_not_exists(#attr)"
            expression_attribute_names = {"#attr": filters[0]}
            expression_attribute_values = ""
        elif attribute_conditions == 'begins_with':
            filter_expression = "begins_with(#attr, :val)"
            expression_attribute_names = {"#attr": filters[0]}
            expression_attribute_values = {":val": {filters[1]: filters[3]}}
        else:
            print("error in specifying the condition in where statement")
            return "", "", ""
        return filter_expression, expression_attribute_names, expression_attribute_values
