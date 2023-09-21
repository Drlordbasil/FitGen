import requests 
from bs4 import BeautifulSoup 
import random 

class WorkoutPlanner:
    def __init__(self):
        self.exercises = []
    
    def get_user_input(self):
        fitness_goals = input("Enter your fitness goals (separated by commas): ").split(",")
        fitness_level = input("Enter your current fitness level: ")
        workout_duration = input("Enter your preferred workout duration (minutes): ")
        available_equipment = input("Enter the available equipment (separated by commas): ").split(",")
        
        return fitness_goals, fitness_level, workout_duration, available_equipment
    
    def scrape_exercise_data(self):
        url = "https://www.examplefitnesswebsite.com/exercises"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        
        exercise_elements = soup.find_all("div", class_="exercise")
        
        for exercise_element in exercise_elements:
            name = exercise_element.find("h3").text
            description = exercise_element.find("p").text
            muscle_groups = exercise_element.find("span", class_="muscle-groups").text.split(",")
            difficulty_level = exercise_element.find("span", class_="difficulty-level").text
            equipment = exercise_element.find("span", class_="equipment").text.split(",")
            
            exercise = {
                "name": name,
                "description": description,
                "muscle_groups": muscle_groups,
                "difficulty_level": difficulty_level,
                "equipment": equipment
            }
            
            self.exercises.append(exercise)
    
    def filter_exercises(self, fitness_goals, fitness_level, available_equipment):
        filtered_exercises = []
        
        for exercise in self.exercises:
            if all(goal.lower() in exercise["name"].lower() for goal in fitness_goals) \
                    and exercise["difficulty_level"].lower() == fitness_level.lower() \
                    and all(equipment.lower() in exercise["equipment"] for equipment in available_equipment):
                filtered_exercises.append(exercise)
        
        return filtered_exercises
    
    def generate_workout_routine(self, filtered_exercises, workout_duration):
        random.shuffle(filtered_exercises)
        total_exercises = len(filtered_exercises)
        exercise_duration = int(workout_duration / total_exercises)
        
        workout_routine = []
        
        for exercise in filtered_exercises:
            instruction = f"Exercise: {exercise['name']}\n"
            instruction += f"Muscle Groups: {', '.join(exercise['muscle_groups'])}\n"
            instruction += f"Difficulty Level: {exercise['difficulty_level']}\n"
            instruction += f"Equipment: {', '.join(exercise['equipment'])}\n"
            instruction += f"description: {exercise['description']}\n"
            instruction += f"Duration: {exercise_duration} minutes\n"
            
            workout_routine.append(instruction)
        
        return workout_routine
    
    def display_workout_routine(self, workout_routine):
        print("Workout Routine:")
        
        for instruction in workout_routine:
            print(instruction)
    
    def create_workout_plan(self):
        fitness_goals, fitness_level, workout_duration, available_equipment = self.get_user_input()
        self.scrape_exercise_data()
        filtered_exercises = self.filter_exercises(fitness_goals, fitness_level, available_equipment)
        workout_routine = self.generate_workout_routine(filtered_exercises, workout_duration)
        self.display_workout_routine(workout_routine)
        
if __name__ == "__main__":
    planner = WorkoutPlanner()
    planner.create_workout_plan()
