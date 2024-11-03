from datetime import datetime

class Indices:
    def __init__(self, name):
        self.index_name = name

    def test(self):
        print(f"Hello, {self.index_name}!")

def main():
    current_dateTime = datetime.now()

    log_all_data_to_db
    log_specific_indices

    user = Indices("GPU")
    user.test()

if __name__ == "__main__":
    main()
