class Rutinas:
    def __init__(self, nombre):
        self.nombre = nombre
        self.exercises=[]
        return self.nombre
    
    def add_excercise(self, exercise):
        self.exercises.append(exercise)

    def delete_excercise(self):
        self.exercises.remove(self.exercise)
