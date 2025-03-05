class Student:
    def __init__(self, name, AC, submit):
        self.name = name
        self.AC = AC
        self.submit = submit

    def output(self):
        print(self.name, self.AC, self.submit)


n = int(input())
student_arr = []
while(n > 0):
    n -= 1
    name = input()
    AC, submit = map(int, input().split())
    student = Student(name, AC, submit)
    
    student_arr.append(student)
    

student_arr.sort(key=lambda x: (-x.AC, x.submit, x.name))

for i in student_arr:
    i.output()

    

