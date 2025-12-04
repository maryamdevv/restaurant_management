class Person:
    def __init__(self, name, national_id):
        self.name = name
        self._national_id = national_id.strip()
        
        self._is_active = True
        
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError ("Name can not be empty!")
        self._name = value.strip().title()
    
    @property
    def is_active(self):
        return self._is_active
    
    def is_active(self):
        if self._is_active:
            return f"{self.name} is active."
        return f"{self.name} is not active."
    
    def activate(self):
        if self._is_active:
            return f"{self.name} already is active!"
        self._is_active = True
        return f"{self.name} has been successfully activated."
    
    def deactivate(self):
        if not self._is_active:
            return f"{self.name} already is deactive!"
        self._is_active = False
        return f"{self.name} has been successfully deactivated."
    
    def __str__(self):
        status = "Active" if self._is_active else "Inactive"
        return f"{self.name} ({self._national_id}) | status: {status}"
    
    
class Freelancer(Person):
    def __init__(self, name, national_id, skills=None):
        super().__init__(name, national_id)
        self.skills = skills or []
        self._balance = 0
        self._jobs_done = 0
        self._rating = 0.0
        
    @property
    def skills(self):
        return self._skills
    @skills.setter
    def skills(self, value):
        if value is None:
            value = []
        if not isinstance(value, list):
            raise ValueError("Skills must be a list!")
        self._skills = [s.strip().title() for s in value if s.strip()]
        
    @property
    def balance(self):
        return self._balance
    @property
    def jobs_done(self):
        return self._jobs_done
    @property
    def rating(self):
        return self._rating
    
    def add_skill(self, skill):
        if not skill or not skill.strip():
            raise ValueError("Skill cannot be empty!")
        clean_skill = skill.strip().title()
        if clean_skill not in self._skills:
            self._skills.append(clean_skill)
            return f"Skill '{clean_skill}' added."
        return f"Skill '{clean_skill}' already exists."
    
    def complete_job(self, amount):
        if not isinstance(amount, (int, float)) or amount <=0:
            raise ValueError("Amount must be a positive number!")
        self._balance += amount
        self._jobs_done += 1
        return f"Job completed! +{amount:,} IRR | Total jobs: {self.jobs_done}"
        
    def __str__(self):
        skills_str = ", ".join(self.skills) if self.skills else "No skills"
        return (f"{super().__str__()} | Skills: [{skills_str}] "
                f"| Jobs: {self.jobs_done} | Balance: {self.balance:,} IRR")
        
    
class Client(Person):
    def __init__(self, name, national_id):
        super().__init__(name, national_id)
        self._balance = 0
        
    @property
    def balance(self):
        return self._balance
    
    def deposit(self, money):
        if not isinstance(money, (int, float)) or money <= 0:
            raise ValueError ("Money must be a positive number!")
        self._balance += money
        return f"{money:,} Rials added to balance. New balance: {self.balance:,} IRR"
    
    def __str__(self):
        return f"{super().__str__()} | balanc: {self.balance:,} IRR"
    
    
class Admin(Person):
    def __init__(self, name, national_id, access_level="full"):
        super().__init__(name, national_id)
        self.access_level = access_level

    def ban_user(self, person):
        if not isinstance(person, Person):
            return "Invalid user!"
        if person.is_active:
            person.deactivate()
            return f"{person.name} has been BANNED."
        return f"{person.name} is already banned."

    
    def show_stats(self, platform):
        total_users = len(platform.people)
        active_users = sum(1 for p in platform.people if p.is_active)
        freelancers = [p for p in platform.people if isinstance(p, Freelancer)]
        clients = [p for p in platform.people if isinstance(p, Client)]
        
        return f"""
=== PLATFORM STATS ===
Total Users: {total_users}
Active Users: {active_users}
Freelancers: {len(freelancers)}
Clients: {len(clients)}
Total Money in System: {sum(p.balance for p in platform.people if hasattr(p, 'balance')):,} IRR
        """.strip()
        
    
class FreelancePlatform:
    def __init__(self):
        self.people = []
        
    def add_person(self, person):
        if not isinstance(person, Person):
            raise TypeError("person must be of class Person!")
        self.people.append(person)
        return f"{person.name} was added to list."
    
    def find_by_national_id(self, n_id):
        for person in self.people:
            if person._national_id == n_id:
                return person
        return None
    
    def deposit_to_client(self, n_id, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive!")
        client = self.find_by_national_id(n_id)
        if client is None:
            return "Client not found!"
        if not isinstance(client, Client):
            return "This person is not a client!"
        client.deposit(amount)
        return f"Deposited {amount:,} IRR to {client.name}. New balance: {client.balance:,} IRR"
    
    def complete_job(self, freelancer_nid, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive!")
        freelancer = self.find_by_national_id(freelancer_nid)
        if freelancer is None:
            return "freelancer not found!"
        if not isinstance(freelancer, Freelancer):
            return "This person is not a freelancer!"
        result = freelancer.complete_job(amount)
        return result
        
        
    def show_active_people(self):
        active_person = []
        for person in self.people:
            if person.is_active() :
                active_person.append(person)
        if not active_person:
            return "No active person is in platform!"
        lines = ["-"*60]
        for i, p in enumerate(active_person, 1):
            lines.append(f"{i:2}. {p}")
        lines.append("-"*60)
        return "\n".join(lines)
    
    def ban_user(self, n_id):
        if not self.people:
            return "There is no one on the platform who wants to be banned!"
        person = self.find_by_national_id(n_id)
        if person is None:
            return "Person not found!!"
        return person.deactivate()
        

def main():
    platform = FreelancePlatform()
    
    while True:
        print("\n" + "="*50)
        print("   FREELANCE PLATFORM - MADE BY MARYAM   ")
        print("="*50)
        print("1. Freelance registration")
        print("2. Client registration")
        print("3. Deposit money to the client")
        print("4. Completion of work by freelancer")
        print("5. Show active people")
        print("6. Ban the user")
        print("7. Exit")
        print("="*50)
        
        choice = input("choose (1-7):").strip()
        
        if choice == "1":
            name = input("Name:").strip()
            n_id = input("National ID:").strip()
            skills_input = input("skills (Separate with commas):").strip()
            skills = []
            if skills_input:
                parts = skills_input.split(",")
                for part in parts:
                    clean = part.strip().title()
                    if clean:
                        skills.append(clean)
            freelancer = Freelancer(name, n_id, skills)
            print(platform.add_person(freelancer))
            
        elif choice == "2":
            name = input("Name:").strip()
            n_id = input("National_ID:").strip()
            client = Client(name, n_id)
            print(platform.add_person(client))
            
        elif choice == "3":
            try:
                n_id = input("National_ID:").strip()
                amount = int(input("Deposit amount:"))
                print(platform.deposit_to_client(n_id, amount))
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == "4":
            try:
                n_id = input("National_ID:").strip()
                amount = int(input("Amount of work done:"))
                print(platform.complete_job(n_id, amount))
            except ValueError as e:
                print(f"Error: {e}")
             
        elif choice == "5":
            print(platform.show_active_people())
            
        elif choice == "6":
            n_id = input("National_ID:").strip()
            print(platform.ban_user(n_id))
            
        elif choice == "7":
            print("\nYou are the best in world💙💙💙")
            break
        
        else:
            print("Enter only numbers 1 to 7!")
            
if __name__ == "__main__":
    main()