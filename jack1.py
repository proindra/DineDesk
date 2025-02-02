import csv
import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class Restaurant:
    def __init__(self, restaurant_id, name, cuisine_type, rating, location, total_tables, table_configuration, opening_hours, closing_hours):
        self.restaurant_id = restaurant_id
        self.name = name
        self.cuisine_type = cuisine_type
        self.rating = rating
        self.location = location
        self.total_tables = total_tables
        self.table_configuration = table_configuration
        self.opening_hours = opening_hours
        self.closing_hours = closing_hours

    def get_available_tables(self, date, time, party_size):
        with open('bookings.csv', 'r') as file:
            reader = csv.DictReader(file)
            booked_tables = [row['table_id'] for row in reader if row['restaurant_id'] == self.restaurant_id and row['date'] == date and row['time'] == time]
        available_tables = []
        for table_type, count in self.table_configuration.items():
            if int(table_type.split('-')[0]) >= party_size:
                for i in range(count):
                    table_id = f"{table_type}-{i+1}"
                    if table_id not in booked_tables:
                        available_tables.append(table_id)
        return available_tables

    def display_restaurant_info(self):
        return (f"Name: {self.name}\nCuisine: {self.cuisine_type}\nRating: {self.rating}/5\n"
                f"Location: {self.location}\nOperating Hours: {self.opening_hours} - {self.closing_hours}\n")

    def check_valid_booking_time(self, time):
        opening = datetime.strptime(self.opening_hours, "%H:%M").time()
        closing = datetime.strptime(self.closing_hours, "%H:%M").time()
        booking_time = datetime.strptime(time, "%H:%M").time()
        return opening <= booking_time <= closing
class User:
    def __init__(self, user_id, name, email, phone_number, current_bookings):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.current_bookings = json.loads(current_bookings)

    def make_reservation(self, restaurant_id, date, time, table_id, party_size):
        with open('bookings.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([f"B-{datetime.now().timestamp()}", self.user_id, restaurant_id, table_id, date, time, party_size])
        self.current_bookings.append({
            "restaurant_id": restaurant_id,
            "date": date,
            "time": time,
            "table_id": table_id,
            "party_size": party_size
        })
        messagebox.showinfo("Success", "Reservation made successfully!")

    def cancel_reservation(self, booking_id):
        rows = []
        booking_found = False
        with open('bookings.csv', 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                if row[0] != booking_id:
                    rows.append(row)
                else:
                    booking_found = True

        if not booking_found:
            messagebox.showerror("Error", "Booking ID not found!")
            return

        with open('bookings.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)

        self.current_bookings = [booking for booking in self.current_bookings if booking["table_id"] != booking_id]
        messagebox.showinfo("Success", "Reservation canceled successfully!")

    def view_booking_history(self):
        return self.current_bookings

class BookingDialog(tk.Toplevel):
    def __init__(self, parent, restaurant):
        super().__init__(parent)
        self.title("Confirm Booking")
        self.restaurant = restaurant
        self.result = None
        self.parent = parent  
        
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=20, pady=20)
        
        ttk.Label(main_frame, text="Enter Your Details", font=('Arial', 12, 'bold')).pack(pady=10)
        
        ttk.Label(main_frame, text="Name:").pack()
        self.name_entry = ttk.Entry(main_frame, width=30)
        self.name_entry.pack(pady=5)
        
        ttk.Label(main_frame, text="Email:").pack()
        self.email_entry = ttk.Entry(main_frame, width=30)
        self.email_entry.pack(pady=5)
        
        ttk.Label(main_frame, text="Phone:").pack()
        self.phone_entry = ttk.Entry(main_frame, width=30)
        self.phone_entry.pack(pady=5)
        
        ttk.Button(main_frame, text="Confirm Booking", 
                  command=self.confirm_booking).pack(pady=20)

    def confirm_booking(self):    
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()

        date = self.parent.date_entry.get()
        time = self.parent.time_entry.get()
        party_size = self.parent.party_size_entry.get()
        table_id = self.parent.table_id_entry.get()

        if not all([name, email, phone, date, time, party_size, table_id]):
            messagebox.showerror("Error", "Please fill in all fields")
            return

        booking_id = f"B-{datetime.now().timestamp()}"
        summary = f"""
        Booking Details:
        ---------------
        Name: {name}
        Email: {email}
        Phone: {phone}
        Restaurant: {self.restaurant.name}
        Date: {date}
        Time: {time}
        Party Size: {party_size}
        Table: {table_id}
        Booking ID: {booking_id}
        """
        
        if messagebox.askyesno("Confirm Booking", f"{summary}\n\nConfirm this booking?"):
            self.result = {
                "booking_id": booking_id,
                "restaurant_id": self.restaurant.restaurant_id,
                "user_name": name,
                "user_email": email,
                "user_phone": phone,
                "date": date,
                "time": time,
                "party_size": party_size,
                "table_id": table_id
            }
            self.destroy()
class RestaurantBookingSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Restaurant Booking System")
        self.geometry("800x600")
        self.restaurants = []  
        self.current_user = None  
        self.initialize_ui()
        self.login_prompt()  

    def initialize_ui(self):
        self.tabs = ttk.Notebook(self)
        
        self.restaurant_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.restaurant_tab, text="Restaurants")
        self.initialize_restaurant_tab()

        self.booking_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.booking_tab, text="Book a Table")
        self.initialize_booking_tab()

        self.user_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.user_tab, text="User Management")
        self.initialize_user_tab()

        self.tabs.pack(expand=1, fill="both")

    def initialize_restaurant_tab(self):
        search_frame = ttk.Frame(self.restaurant_tab)
        search_frame.pack(fill="x")
        ttk.Label(search_frame, text="Search:").pack(side="left", padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_restaurants).pack(side="left", padx=5)

        filter_frame = ttk.Frame(self.restaurant_tab)
        filter_frame.pack(fill="x", pady=10)
        
        ttk.Label(filter_frame, text="Cuisine:").pack(side="left", padx=5)
        self.cuisine_var = tk.StringVar(value="All")
        self.cuisine_filter = ttk.Combobox(filter_frame, textvariable=self.cuisine_var, state='readonly')
        self.cuisine_filter.pack(side="left", padx=5)
        
        ttk.Label(filter_frame, text="Min Rating:").pack(side="left", padx=5)
        self.rating_var = tk.StringVar(value="All")
        self.rating_filter = ttk.Combobox(filter_frame, textvariable=self.rating_var, 
                                        values=["All", "4.5+", "4.0+", "3.5+", "3.0+"], 
                                        state='readonly')
        self.rating_filter.pack(side="left", padx=5)
        
        ttk.Button(filter_frame, text="Apply Filter", 
                   command=self.apply_filters).pack(side="left", padx=5)
        
        ttk.Label(self.restaurant_tab, text="Restaurants:").pack(pady=5)
        self.restaurant_list = ttk.Treeview(self.restaurant_tab, 
                                          columns=("Name", "Cuisine", "Rating", "Location"), 
                                          show="headings")
        self.restaurant_list.heading("Name", text="Name")
        self.restaurant_list.heading("Cuisine", text="Cuisine")
        self.restaurant_list.heading("Rating", text="Rating")
        self.restaurant_list.heading("Location", text="Location")
        self.restaurant_list.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.load_restaurants()

    def initialize_booking_tab(self):
        ttk.Label(self.booking_tab, text="Make a Reservation").pack()
        ttk.Label(self.booking_tab, text="Date (YYYY-MM-DD):").pack()
        self.date_entry = ttk.Entry(self.booking_tab)
        self.date_entry.pack()
        ttk.Label(self.booking_tab, text="Time (HH:MM):").pack()
        self.time_entry = ttk.Entry(self.booking_tab)
        self.time_entry.pack()
        ttk.Label(self.booking_tab, text="Party Size:").pack()
        self.party_size_entry = ttk.Entry(self.booking_tab)
        self.party_size_entry.pack()
        self.table_id_entry = ttk.Entry(self.booking_tab)
        ttk.Label(self.booking_tab, text="Table ID:").pack()
        self.table_id_entry.pack()
        ttk.Button(self.booking_tab, text="Check Availability", command=self.check_availability).pack()
        ttk.Button(self.booking_tab, text="Confirm Booking", command=self.make_reservation).pack()

    def initialize_user_tab(self):
        ttk.Label(self.user_tab, text="User Management").pack()
        ttk.Button(self.user_tab, text="View Booking History", command=self.view_booking_history).pack()
        ttk.Button(self.user_tab, text="Cancel Reservation", command=self.cancel_reservation).pack()

    def load_restaurants(self):
        try:
            with open('restaurants.csv', 'r') as file:
                reader = csv.DictReader(file)
                
                cuisines = set()
                
                for row in reader:
                    cuisines.add(row['cuisine_type'])
                    table_config = json.loads(row['table_configuration'].replace("'", '"'))
                    self.restaurants.append(Restaurant(
                        restaurant_id=row['restaurant_id'],
                        name=row['name'],
                        cuisine_type=row['cuisine_type'],
                        rating=float(row['rating']),
                        location=row['location'],
                        total_tables=int(row['total_tables']),
                        table_configuration=table_config,
                        opening_hours=row['opening_hours'],
                        closing_hours=row['closing_hours']
                    ))
                    self.restaurant_list.insert("", "end", 
                        values=(row['name'], row['cuisine_type'], 
                               row['rating'], row['location']))
                
                cuisine_options = ["All"] + sorted(list(cuisines))
                self.cuisine_filter['values'] = cuisine_options
                
        except FileNotFoundError:
            messagebox.showerror("Error", "restaurants.csv not found!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_restaurants(self):
        search_query = self.search_entry.get().lower()
        for item in self.restaurant_list.get_children():
            self.restaurant_list.delete(item)

        for restaurant in self.restaurants:
            if search_query in restaurant.name.lower() or search_query in restaurant.cuisine_type.lower() or search_query in restaurant.location.lower():
                self.restaurant_list.insert("", "end", values=(restaurant.name, restaurant.cuisine_type, restaurant.rating, restaurant.location))

    def check_availability(self):
        date = self.date_entry.get()
        time = self.time_entry.get()
        try:
            party_size = int(self.party_size_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Party size must be a valid number!")
            return

        available_restaurants = []
        for restaurant in self.restaurants:
            if restaurant.check_valid_booking_time(time):
                available_tables = restaurant.get_available_tables(date, time, party_size)
                if available_tables:
                    available_restaurants.append((restaurant.name, available_tables))

        if available_restaurants:
            availability_info = "\n".join([f"{name}: {', '.join(tables)}" for name, tables in available_restaurants])
            messagebox.showinfo("Availability", availability_info)
        else:
            messagebox.showinfo("Availability", "No tables available for the given date and time.")

    def make_reservation(self):
        if not self.current_user:
            messagebox.showerror("Error", "Please login first!")
            return
        if not all([self.date_entry.get(), self.time_entry.get(), 
                    self.party_size_entry.get(), self.table_id_entry.get()]):
            messagebox.showerror("Error", "Please fill in all booking details first")
            return
            
        selected_item = self.restaurant_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a restaurant")
            return
        
        restaurant_data = self.restaurant_list.item(selected_item)['values']
        selected_restaurant = None
        
        for restaurant in self.restaurants:
            if restaurant.name == restaurant_data[0]:
                selected_restaurant = restaurant
                break
        
        if selected_restaurant:
            dialog = BookingDialog(self, selected_restaurant)
            self.wait_window(dialog)
            
            if dialog.result:
                with open('bookings.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        dialog.result["booking_id"],
                        self.current_user.user_id,
                        dialog.result["restaurant_id"],
                        dialog.result["table_id"],
                        dialog.result["date"],
                        dialog.result["time"],
                        dialog.result["party_size"]
                    ])
                
                self.current_user.current_bookings.append({
                    "booking_id": dialog.result["booking_id"],
                    "restaurant_id": dialog.result["restaurant_id"],
                    "date": dialog.result["date"],
                    "time": dialog.result["time"],
                    "table_id": dialog.result["table_id"]
                })
                
                messagebox.showinfo("Success", 
                                  f"Booking confirmed!\nYour booking ID is: {dialog.result['booking_id']}")

    def view_booking_history(self):
        if not self.current_user:
            messagebox.showerror("Error", "Please login first!")
            return
            
        bookings = []
        try:
            with open('bookings.csv', 'r') as file:
                reader = csv.DictReader(file)
                bookings = [row for row in reader if row.get('user_id') == self.current_user.user_id]
                
            if bookings:
                history_info = "\n".join([
                    f"Booking ID: {b['booking_id']}\n"
                    f"Restaurant: {b['restaurant_id']}\n"
                    f"Date: {b['date']}\n"
                    f"Time: {b['time']}\n"
                    f"Table: {b['table_id']}\n"
                    f"-------------------" for b in bookings
                ])
                messagebox.showinfo("Booking History", history_info)
            else:
                messagebox.showinfo("Booking History", "No bookings found.")
        except FileNotFoundError:
            messagebox.showerror("Error", "No booking records found.")

    def cancel_reservation(self):
        booking_id = simpledialog.askstring("Cancel Booking", "Enter your booking ID:")
        if not booking_id:
            return

        try:
            rows = []
            booking_found = False
            with open('bookings.csv', 'r') as file:
                reader = csv.reader(file)
                headers = next(reader)
                for row in reader:
                    if row[0] != booking_id:
                        rows.append(row)
                    else:
                        booking_found = True

            if not booking_found:
                messagebox.showerror("Error", "Booking ID not found!")
                return

            with open('bookings.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(rows)

            messagebox.showinfo("Success", "Reservation canceled successfully!")
        except FileNotFoundError:
            messagebox.showerror("Error", "No booking records found.")

    def login_prompt(self):
        user_id = simpledialog.askstring("Login", "Enter your User ID:")
        if user_id:
            self.load_user(user_id)
        else:
            messagebox.showerror("Error", "Login required!")
            self.destroy()

    def load_user(self, user_id):
        try:
            with open('users.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['user_id'] == user_id:
                        self.current_user = User(
                            row['user_id'],
                            row['name'],
                            row['email'],
                            row['phone_number'],
                            row['current_bookings']
                        )
                        messagebox.showinfo("Success", f"Welcome {self.current_user.name}!")
                        return
                messagebox.showerror("Error", "User not found!")
                self.destroy()
        except FileNotFoundError:
            messagebox.showerror("Error", "users.csv not found!")
            self.destroy()

    def apply_filters(self):
        for item in self.restaurant_list.get_children():
            self.restaurant_list.delete(item)
        
        cuisine_filter = self.cuisine_var.get()
        rating_filter = self.rating_var.get()
        min_rating = 0.0
        if rating_filter != "All":
            min_rating = float(rating_filter.replace("+", ""))
        for restaurant in self.restaurants:
            if (cuisine_filter == "All" or restaurant.cuisine_type == cuisine_filter) and \
               (rating_filter == "All" or restaurant.rating >= min_rating):
                self.restaurant_list.insert("", "end", 
                    values=(restaurant.name, restaurant.cuisine_type, 
                           restaurant.rating, restaurant.location))

if __name__ == "__main__":
    app = RestaurantBookingSystem()
    app.mainloop()
