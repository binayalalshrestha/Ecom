def together(*args, **kwargs):
    rollNumber = 0

    for rollNumber in args:
        print(f"Student is {kwargs['name']} with roll no {rollNumber} and address {kwargs['addr']}.")

together(1,name="abc",addr="def")
together(2,name="ghi",addr="jkl")
