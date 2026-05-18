import json
from datetime import datetime

class Task:
    def __init__(self, title: str, description: str = ""):
        self.id          = datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.title       = title
        self.description = description
        self.status      = "todo"
        self.created_at  = datetime.now().strftime("%d.%m.%Y %H:%M")

    def complete(self):
        self.status = "done"

    def __str__(self):
        icon = "✅" if self.status == "done" else "⬜"
        return f"{icon} [{self.id}] {self.title} — {self.status}"

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title!r}, status={self.status})"

    def to_dict(self) -> dict:
        return {
            "id":          self.id,
            "title":       self.title,
            "description": self.description,
            "status":      self.status,
            "created_at":  self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        task             = cls(data["title"], data.get("description", ""))
        task.id          = data["id"]
        task.status      = data["status"]
        task.created_at  = data["created_at"]
        return task

class TaskManager:
    def __init__(self):
        try:
            with open("tasklist.json", "r") as jsonfile:
                data = json.load(jsonfile)
                self.tasks = {key: Task.from_dict(value) for key, value in data.items()}
        except FileNotFoundError:
           self.tasks = {}
    def _save(self):
        with open("tasklist.json", "w") as jsonfile:
            json.dump({key: value.to_dict() for key, value in self.tasks.items()}, jsonfile)
    def add(self):
        title = input("Название: ")
        description = input("Описание: ")
        task = Task(title, description)
        self.tasks[task.id] = task
        self._save()
    def delete(self, id):
        try: 
            del self.tasks[id]
            self._save()
        except KeyError:
            print(f"Задача с id {id} не найдена")
    def complete(self, id):
        try: 
            task = self.tasks[id]
            task.complete()
            self._save()
        except KeyError:
            print(f"Задача с id {id} не найдена")
    def get_all(self, status = ""):
        if status != "":
            for i in self.tasks:
                task = self.tasks[i]
                if task.status == status : print(task, "\n")
        else:
            for i in self.tasks:
                print(self.tasks[i])
    def search(self, substr):
        for i in self.tasks:
            task = self.tasks[i]
            if substr in task.title or substr in task.description:
                print(task)
if __name__ == "__main__":
    taskmanager = TaskManager()
    while True:
        print("Выберите Действие: \n1 - Добавить задачу, \n2 - Удалить задачу, \n3 - Завершить задачу, \n4 - Вывести все задачи, \n5 - Найти задачу, \nесли напишите что угодно кроме 12345 программа завершится")
        try: 
            opt = int(input())
            if opt == 1:
                taskmanager.add()
            elif opt == 2:
                print("Укажите айди задачи: ")
                id = str(input())
                taskmanager.delete(id)
            elif opt == 3:
                print("Укажите айди задачи: ")
                id = str(input())
                taskmanager.complete(id)
            elif opt == 4:
                print("Если хотите вывести только готовые задачи напишите done если хотите только задачи в процессе напишите todo если все задачи не пишите ничего: ")
                status = str(input())
                taskmanager.get_all(status)
            elif opt == 5:
                print("Напишите часть описания или имени задачи")
                substr = str(input())
                taskmanager.search(substr)
            else: break
        except ValueError:
            print("Это не целочисленное число, умник")

        
