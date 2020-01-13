import json
store = input("Enter number of lines and queries: ").split()
lines = int(store[0])
queries = int(store[1])
Json = ''
print("Enter JSON file:")
for l in range(lines):
    Json += input()
Json_text = json.loads(Json)
print("Enter Queries:")
Query = []
NQ = []
for i in range(queries):
    Query.append(input())
    if '.' in Query[i]:
        NQ.append((Query[i].split('.'))[1])
        Query[i] = (Query[i].split('.'))[0]
    if Query[i] in Json_text and type(Json_text.get(Query[i])) != dict:
        print(Json_text.get(Query[i]))
    elif Query[i] in Json_text:
        if NQ[0] in Json_text.get(Query[i]):
            print((Json_text.get(Query[i])).get(NQ[0]))
            NQ = []
        else:print("Null")
    else: print("Null")