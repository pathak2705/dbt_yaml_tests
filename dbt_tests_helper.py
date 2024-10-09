#utility to create dbt tests based on table and column inputs

def dbt_test_creator(table_name: str, col_types: {}):
    """
    :param table_name: name of the main table
    :param col_types: a key:value pair containing details of columns and their types
    here's the list of types available for now -
    - of_type: dbt_expectations.expect_column_values_to_be_of_type
    - unique: dbt_expectations.expect_column_values_to_be_unique
    - not_null: dbt_expectations.expect_column_values_to_not_be_null
    - values_in_set: dbt_expectations.expect_column_values_to_be_in_set
    - regex: dbt_expectations.expect_column_values_to_match_regex
    - none: columns that do not require any dbt tests
    eg - {"of_type": ["col_1", "col_2"]} -> this means that col_1 and col_2 from main table will have dbt test clause for expect_column_values_to_be_of_type
    :return: structured dbt tests in yaml format
    """
    res = f"  - name: {table_name}\n    description: \n    columns:"

    #function to create inverse column:test dict for ease of use
    inverse_col_types = {}
    for key, value in col_types.items():
        for col in value:
            if col in inverse_col_types:
                inverse_col_types[col].append(key)
            else:
                inverse_col_types[col] = [key]

    for key, value in inverse_col_types.items():
        check = f"\n      - name: {key}\n        description:"
        if any(dbt_type in value for dbt_type in ["of_type", "unique", "not_null", "values_in_set", "regex"]):
            check+= "\n        tests:"
        for test_type in value:
            if test_type == "of_type":
                check+= "\n          - dbt_expectations.expect_column_values_to_be_of_type:\n              column_type:"
            elif test_type == "unique":
                check+= "\n          - dbt_expectations.expect_column_values_to_be_unique"
            elif test_type == "not_null":
                check+= "\n          - dbt_expectations.expect_column_values_to_not_be_null"
            elif test_type == "values_in_set":
                check+= "\n          - dbt_expectations.expect_column_values_to_be_in_set:\n              value_set:"
            elif test_type == "regex":
                check+= "\n          - dbt_expectations.expect_column_values_to_match_regex:\n              regex:"
            else:
                check+= ""
        res+= check
    print(res)

#input variables - change as per your requirements
table = "test" # name of your table
column_type_dict = {
            "none": ["col_1","col_2","col_3","col_4"],
            "of_type": ["col_8","col_7"],
            "regex":["col_7","col_8"],
            "unique":["col_7","col_8"],
            "not_null":["col_7","col_8","col_9"]
                    }

#function call
dbt_test_creator(table, column_type_dict)

