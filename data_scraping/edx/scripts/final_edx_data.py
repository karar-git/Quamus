import json
def shape(lst):
    if not isinstance(lst, list):
        return [] 
    return [len(lst)] + shape(lst[0])
def main():

    fields = ["courses","degree_programs","programs","executive_education"]
    data = []
    for i,field in enumerate(fields):
        with open(f'edx_{field}.json', 'r') as file:
            data.append(json.load(file))
    
if __name__ == '__main__':
    main()
