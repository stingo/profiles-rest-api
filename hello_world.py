todos = []
while True:
    
    todo = input("Enter to do: ")
    if todo.lower() == 'exit':
        break
    todos.append(todo)
   
    print("Your to-do list:\n" + "\n".join(todos))
