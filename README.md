# Restaurant Seat Booking System

A GUI-based application for browsing restaurants, booking tables, and managing reservations. Built with Python and CSV file-based data storage.

---

## *Problem Statement*

Develop a Restaurant Seat Booking System with a graphical user interface (GUI) that allows users to:

- View and search restaurants
- Make and cancel table reservations
- Manage personal booking records

The system uses CSV files for persistent data storage.

---

## *System Requirements*

### *1. Data Storage*

The system utilizes three CSV files:

- restaurants.csv – Restaurant information and table configurations
- users.csv – Registered user details
- bookings.csv – Reservation records

---

### *2. Required Classes*

#### *2.1 Restaurant Class*

*Attributes:*

- restaurant_id (unique identifier)
- name
- cuisine_type
- rating (out of 5)
- location
- total_tables
- table_configuration (e.g., 2-seater, 4-seater)
- opening_hours
- closing_hours

*Methods:*

- Constructor to initialize restaurant data  
- get_available_tables(date, time, party_size)  
- display_restaurant_info()  
- check_valid_booking_time(time)  
- Method to export restaurant data to CSV format

---

#### *2.2 User Class*

*Attributes:*

- user_id (unique identifier)
- name
- email
- phone_number
- current_bookings (list of active bookings)

*Methods:*

- Constructor to initialize user data  
- make_reservation(restaurant_id, date, time, table_id, party_size)  
- cancel_reservation(booking_id)  
- view_booking_history()  
- Method to export user data to CSV format

---

## *3. GUI Requirements*

### *3.1 Main Window*

- Title: *"Restaurant Booking System"*
- Clean, professional layout
- Easy navigation between sections

---

### *3.2 Components*

#### *1. Restaurant Display Section*
- Scrollable list of all restaurants
- Filter by *cuisine type* and *rating*
- Search bar by restaurant name
- Detailed restaurant view on selection

#### *2. Booking Section*
- Date & time selector
- Party size input
- View and select available tables
- Booking confirmation form

#### *3. User Management Section*
- View current bookings
- Booking history
- Cancel booking interface

---

## *4. Functional Requirements*

### *4.1 Restaurant Display*
- Show restaurant details:  
  - Name, Cuisine, Rating, Location, Operating Hours, Available Tables
- Filter & sort features

### *4.2 Booking Process*

*Steps:*

1. Select date, time, and party size
2. View available tables
3. Select a table
4. Enter user details
5. Review & confirm reservation
6. Receive booking confirmation ID

---

### *4.3 Cancellation Process*

- View all current bookings
- Choose a booking to cancel
- Confirm cancellation
- Update table availability in the system

---

## *Technologies Used*

- Python 3.x
- Tkinter (GUI)
- CSV (Data storage)

---

## *License*

This project is licensed under the [MIT License](LICENSE).

---

## *Author*

Created by PRAJWALINDRA
