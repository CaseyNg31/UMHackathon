import hashlib
import time
import json
import os

class Block:
    def __init__(self, index, donor, donation_type, amount, previous_hash, timestamp=None, hash_value=None):
        self.index = index
        self.timestamp = timestamp if timestamp else time.strftime('%Y-%m-%d %H:%M:%S')
        self.donor = donor
        self.donation_type = donation_type
        self.amount = amount
        self.previous_hash = previous_hash
        self.hash = hash_value if hash_value else self.calculate_hash()

    def calculate_hash(self):
        block_content = f"{self.index}{self.timestamp}{self.donor}{self.donation_type}{self.amount}{self.previous_hash}"
        return hashlib.sha256(block_content.encode()).hexdigest()

    def to_dict(self):
        return {
            "Index": self.index,
            "Timestamp": self.timestamp,
            "Donor": self.donor,
            "Type": self.donation_type,
            "Amount": self.amount,
            "Previous Hash": self.previous_hash,
            "Hash": self.hash
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            index=data["Index"],
            donor=data["Donor"],
            donation_type=data["Type"],
            amount=data["Amount"],
            previous_hash=data["Previous Hash"],
            timestamp=data["Timestamp"],
            hash_value=data["Hash"]
        )

    def __str__(self):
        return f"""
        Block #{self.index}
        Donor: {self.donor}
        Type: {self.donation_type}
        Amount: ${self.amount}
        Timestamp: {self.timestamp}
        Previous Hash: {self.previous_hash}
        Hash: {self.hash}
        """

class DonationLedger:
    def __init__(self):
        self.chain = []

        if os.path.exists("blockchain.json"):
            self.load_from_json()
        else:
            self.chain.append(self.create_genesis_block())

    def create_genesis_block(self):
        return Block(0, "Genesis", "N/A", 0, "0")

    def add_donation(self, donor, donation_type, amount):
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), donor, donation_type, amount, last_block.hash)
        self.chain.append(new_block)

    def print_ledger(self):
        for block in self.chain:
            print(block)

    def verify_chain(self):
        print("Verifying chain integrity...")
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.previous_hash != previous.hash or current.hash != current.calculate_hash():
                print(f"Chain broken at block {i}")
                return False
        print("✅ All blocks are valid and connected.")
        return True

    def save_to_json(self, filename="blockchain.json"):
        with open(filename, "w", encoding='utf-8') as f:
            json.dump([block.to_dict() for block in self.chain], f, indent=4)
        print(f"📁 Ledger saved to {filename}")

    def load_from_json(self, filename="blockchain.json"):
        with open(filename, "r", encoding='utf-8') as f:
            data = json.load(f)
            self.chain = [Block.from_dict(block_data) for block_data in data]
        print(f"📥 Loaded ledger from {filename}")

ledger = DonationLedger()

print("\n📥 Welcome to the Blockchain-style Charity Donation Ledger")
while True:
    donor = input("Enter donor name (or 'q' to quit): ")
    if donor.lower() == 'q':
        break
    donation_type = input("Enter donation type (Zakat / Sadaqah / Waqf): ").capitalize()
    try:
        amount = float(input("Enter donation amount: $"))
    except ValueError:
        print("Invalid amount. Try again.")
        continue

    ledger.add_donation(donor, donation_type, amount)
    print("Donation recorded!\n")

print("\n📄 Full Donation Ledger:")
ledger.print_ledger()
ledger.verify_chain()
ledger.save_to_json()
