from classes.ReadFile import RF


def main():
    rf = RF("./Statements")
    df = rf.read(template="./template.json")
    print(df)


if __name__ == "__main__":
    main()
