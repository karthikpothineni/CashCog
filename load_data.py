import requests
import ast
import sys
import psycopg2

connection = psycopg2.connect( host="localhost", user="postgres", password="", dbname="cash_cog" )
cursor = connection.cursor()
employee_insert_query = "INSERT INTO employee (uuid, first_name, last_name) VALUES (%s,%s,%s)"
expense_insert_query = "INSERT INTO expense (uuid, description, created_at, amount, currency, employee, is_approved) VALUES (%s,%s,%s,%s,%s,%s,%s)"
count = 0

def populateRecords(record):
    global count
    if 'employee' in record and isinstance(record['employee'],dict) and len(record['employee']) !=0:
        try:
            # Employee insertion
            employee_obj = record['employee']
            emp_record_to_insert = (employee_obj["uuid"], employee_obj["first_name"], employee_obj["last_name"])
            cursor.execute(employee_insert_query, emp_record_to_insert)
            connection.commit()
        except:
            connection.rollback()

        try:
            # Expense insertion
            record['employee'] = employee_obj['uuid']
            exp_record_to_insert = (record["uuid"], record["description"], record["created_at"], record["amount"], record["currency"], record["employee"], 'NA')
            cursor.execute(expense_insert_query, exp_record_to_insert)
            connection.commit()
            count=count+1
            print("Record inserted successfully. Count:",count)
        except Exception as error:
            print("Failed to insert expense record: ",error)
            connection.rollback()
    else:
        print("Employee record not found. Skipping insertion")


def main():
    print("Started loading data in to database")
    try:
        r = requests.get('https://cashcog.xcnt.io/stream', stream=True)
        for each_line in r.iter_lines():
            decoded_line = each_line.decode('utf-8')
            record = ast.literal_eval(decoded_line)
            populateRecords(record)
    except KeyboardInterrupt:
        cursor.close()
        connection.close()
        print("Closed database connection")
        print("Stopped loading")
        sys.exit()


if __name__ == '__main__':
    main()