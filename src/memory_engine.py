import json
from pathlib import Path


class MemoryEngine:

    def __init__(self):

        self.memory_file = Path("memory.json")

        if not self.memory_file.exists():

            self.memory_file.write_text(
                json.dumps({}, indent=4)
            )

    def load_memory(self):

        with open(self.memory_file, "r") as file:

            return json.load(file)

    def save_memory(self, memory):

        with open(self.memory_file, "w") as file:

            json.dump(memory, file, indent=4)

    def remember_user(
        self,
        user_id,
        profile,
    ):

        memory = self.load_memory()

        memory[user_id] = profile

        self.save_memory(memory)

    def recall_user(
        self,
        user_id,
    ):

        memory = self.load_memory()

        return memory.get(user_id)

    def update_field(
        self,
        user_id,
        key,
        value,
    ):

        memory = self.load_memory()

        if user_id not in memory:

            memory[user_id] = {}

        memory[user_id][key] = value

        self.save_memory(memory)