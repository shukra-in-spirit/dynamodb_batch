from rich.console import Console
from rich.prompt import Prompt
from sts_internal.identity import sts_internal
from rich_internal.tui import rich_tui
from dynamodb_internal.core_methods import dynamodb_core
import inquirer
import click
import os
import ast
from commands_internal.commands import commands


def main():
    # Create a Console instance
    console = Console(color_system="auto")

    # Define the prompts for the two input fields
    prompt2 = Prompt.ask("Please provide the role arn",
                         default="arn:aws:iam::717154137320:role/redstone-gl-vas-read-only")
    # Print the given arn
    role_arn_string = rich_tui.create_print_string(
        [("\n\n", ""), ("The role provided is: ", "cyan"), (prompt2, "italic bold green"), ("\n", ""), ("assuming role, please wait.", "")])
    console.print(role_arn_string)

    # take the user prompt and then assumes the role
    # it gets the credentials returned from the sts_internal
    # this credential will be used later to create the clients
    identity = sts_internal(prompt2)
    credentials = identity.assume_role()
    get_role_identity = identity.get_identity_info(credentials)

    # clear screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # Print the assume role success
    assume_role_success_string = rich_tui.create_print_string(
        [("Successfully", "green bold"), (" started session!\n", ""), ("for role: ", ""),
         (get_role_identity['Arn'], "bold"), ("\n\n", ""), ("Getting the list of tables.", "")])
    console.print(assume_role_success_string)

    # Get the list of tables for the role
    dyanamodb_client = dynamodb_core(credentials)
    table_names = dyanamodb_client.get_table_names_as_list()

    # Prompt the user to select the table
    select_table_prompt_string = rich_tui.create_print_string(
        [("Please select the table name: ", ""), ("\n", "")])
    console.print(select_table_prompt_string)
    question = [
        inquirer.List('selected_table',
                      message="Selected Table --> ",
                      choices=table_names,
                      ),
    ]
    answer = inquirer.prompt(question)
    selected_table = answer['selected_table']
    # clear screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # print the selected table
    selected_table_string = rich_tui.create_print_string(
        [("your selected table is: ", ""), (selected_table, "cyan")])
    console.print(selected_table_string)

    # start command info
    start_command_screen = rich_tui.create_print_string(
        [("\nYou can now run your ", ""), ("dynamodb table - ", "red bold"), (selected_table, "green italic"), (" commands.", "")])
    console.print(start_command_screen)

    command = ""
    # start the command sequence
    while command != "exit":
        # ask the user for input command
        command = Prompt.ask("##dynamodb##>")

        # check if the command supplied is for exiting the tool or not
        # in case it is then perform a graceful exit
        if command == "exit":
            # print to console for exit and then end the program
            exit_command_string = rich_tui.create_print_string(
                [("Thank you ", "green bold"), ("for using ", ""), ("dynamodb cheat!", "blue italic")])
            console.print(exit_command_string)
            exit
        else:
            # a command has been supplied, the first step would be to decompose the command
            command_operation, command_operand, filters_list = decompose_command(
                command)
            # create an instance of the internal command control package
            commands_control = commands(
                dynamodb_client=dyanamodb_client, table_name=selected_table)
            # call the execute command from the command control package to start execution
            output_string = commands_control.execute_command(
                command_operation=command_operation, command_operand=command_operand, command_filters=filters_list, console=console)
            # printing the output of execution
            console.print(output_string)
            console.print("\n")

# decomposing means to break down to its smallest parts
# in the decompose command method we are splitting the command
# and returning currently four components
# operation or the first word
# operand or the second word
# a list of the filters that was being passed
# (TODO) a list of the set value or key that was being passed


def decompose_command(command):
    # uses the split to break into everything with spaces
    command_word_list = command.split()
    # sets operation
    command_operation = command_word_list[0]
    # sets operand
    command_operand = command_word_list[1]
    # if only filter is used then puts the value for filter
    if (len(command_word_list) > 2) and ((command_word_list[2] == '-w') or (command_word_list[2] == "--where")):
        # removes the first three elements of the list
        command_where_argument_list = command_word_list[3:]

        command_where_string = ' '.join(map(str, command_where_argument_list))
        filters_list = ast.literal_eval(command_where_string)
        return command_operation, command_operand, filters_list
    # if pnly set is used then puts the value for set
    elif (len(command_word_list) > 2) and ((command_word_list[2] == '-s') or (command_word_list[2] == "--set")):
        # removes the first three elements of the list
        # command_where_argument_list = command_word_list[3:]

        # command_where_string = ' '.join(map(str, command_where_argument_list))
        # filters_list = ast.literal_eval(command_where_string)
        return command_operation, command_operand, "set"
    else:
        return command_operation, command_operand, ""


# Using the special variable
# __name__
if __name__ == "__main__":
    main()
