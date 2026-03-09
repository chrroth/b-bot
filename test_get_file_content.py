from functions.get_file_content import get_file_content

def main():

    print("Result for lorem.txt:")
    result = get_file_content("calculator", "lorem.txt")

    print(len(result))
    lines_list = result.splitlines()
    last_line = lines_list[-1]
    print(last_line)

    print("Result for main.py:")
    print(get_file_content("calculator", "main.py"))

    print("Result for pkg/calculator.py:")
    print(get_file_content("calculator", "pkg/calculator.py"))

    print("Result for /bin/cat:")
    print(get_file_content("calculator", "/bin/cat"))

    print("Result for pkg/does_not_exist.py:")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))
    

if __name__ == "__main__":
    main()

