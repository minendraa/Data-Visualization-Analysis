import os
import datetime

class ParkingSystem:
    def __init__(self,log_file="parking.log",capacity=10):
        self.log_file=log_file
        self.capacity=capacity
        self.parked_vehicles=set()

        if not os.path.exists(self.log_file):
            with open(self.log_file,'w')as file:
                file.write("Parking log initialized\n")

    def get_parked_count(self):
        return len(self.parked_vehicles)
    
    def store_logs(self,vehicle_number,level="Entry"):
        timestamp=datetime.datetime.now().strftime("%Y-%M-%d %H:%M:%S")
        entry=f"[{timestamp}][{level}]{vehicle_number.strip()}\n"

        with open(self.log_file,'a') as file:
            file.write(entry)

        print(f"Log recorded: {entry}",end='')

    def park_vehicle(self,vehicle_number):
        if self.get_parked_count()>=self.capacity:
            print("Parking Full!!")
            return
        
        if vehicle_number in self.parked_vehicles:
            print("Vehicle is already parked..")
            return
    
        self.parked_vehicles.add(vehicle_number)
        self.store_logs(vehicle_number, "Entry")

    def exit_vehicle(self,vehicle_number):
        if vehicle_number not in self.parked_vehicles:
            print("Vehicle is not currently parked.")
            return
        
        self.parked_vehicles.remove(vehicle_number)
        self.store_logs(vehicle_number,"Exit")

    def view_logs(self):
        if os.path.exists(self.log_file):
            with open(self.log_file,'r')as file:
                print("\n---Parking Log Records---")
                print(file.read())

        else:
            print("File does not exist...")

    def filter_logs(self,keyword):
        if os.path.exists(self.log_file):
            with open(self.log_file,'r')as file:
                lines=file.readlines()

            filtered = [line for line in lines if keyword in line]

            print(f"\n---Filtered Data for {keyword}---")
            for line in filtered:
                print(line,end='')

        else:
            print("Lof file not found")


if __name__ == "__main__":
    system = ParkingSystem(capacity=5)

    while True:
        print("\n--- Parking System Menu ---")
        print("1. Park Vehicle")
        print("2. Unpark Vehicle")
        print("3. View Logs")
        print("4. Filter Logs")
        print("5. Exit")

        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            vehicle = input("Enter vehicle number: ").strip().upper()
            system.park_vehicle(vehicle)

        elif choice == "2":
            vehicle = input("Enter vehicle number: ").strip().upper()
            system.exit_vehicle(vehicle)

        elif choice == "3":
            system.view_logs()

        elif choice == "4":
            keyword = input("Enter keyword (e.g., vehicle number or CHECK--IN--): ").strip()
            system.filter_logs(keyword)

        elif choice == "5":
            print("Exiting Parking System...")
            break

        else:
            print("Invalid choice. Try again.")
