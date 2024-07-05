import sqlite3
from tabulate import tabulate

def connect_to_db():
    return sqlite3.connect('smart_garden.db')

def view_all_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM garden_data")
    rows = cursor.fetchall()
    headers = [description[0] for description in cursor.description]
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def view_latest_entries(conn, n=5):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM garden_data ORDER BY id DESC LIMIT ?", (n,))
    rows = cursor.fetchall()
    headers = [description[0] for description in cursor.description]
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def delete_entry(conn, entry_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM garden_data WHERE id = ?", (entry_id,))
    conn.commit()
    print(f"Entry with ID {entry_id} has been deleted.")

def delete_all_data(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM garden_data")
    conn.commit()
    print("All data has been deleted from the garden_data table.")

def main():
    conn = connect_to_db()
    while True:
        print("\n1. View all data")
        print("2. View latest 5 entries")
        print("3. Delete a specific entry")
        print("4. Delete all data")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            view_all_data(conn)
        elif choice == '2':
            view_latest_entries(conn)
        elif choice == '3':
            entry_id = input("Enter the ID of the entry to delete: ")
            delete_entry(conn, entry_id)
        elif choice == '4':
            confirm = input("Are you sure you want to delete all data? (y/n): ")
            if confirm.lower() == 'y':
                delete_all_data(conn)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

    conn.close()

if __name__ == "__main__":
    main()