
def file_reader(file_name):
    x = []
    try:
        # Open the file in read mode
        with open(file_name, 'r') as file:
            # Read and print each line
            for line in file:
                x.append(line.strip())  

    except FileNotFoundError:
        print(f"File not found: {file_name}")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    return x
