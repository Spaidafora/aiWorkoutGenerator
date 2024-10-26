#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from openai import OpenAI
from .models import WorkoutPlan
from django.contrib.auth.models import User


# API key
key = ' ='
client = OpenAI(api_key=key)


# Create your views here.
def home(request):
    return render(request, 'core/home.html')

#login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Username = {username}, Password = {password}")

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, 'Your Username or Password is Incorrect')
            return redirect('login')
        else:
            login(request, user)
            return redirect('home')
    
    return render(request, 'core/login.html')

#signup
def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')

        print(f"Username: {username}, Password: {password}")

        if password != confirmPassword:
            messages.error(request, "The password does not match!")
            return render(request, 'core/signup.html')
        
        try:
            # Create the user instance using Django's User model
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "You have successfully registered! Please Log In")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error while creating User: {str(e)}")
            return render(request, 'core/signup.html')
            
    return render(request, 'core/signup.html')

# get user input, make API call, save info, redirect to workout.html , save in history.html
def generate_workout(request):
    if request.method == 'POST':  # validate
        time = request.POST.get('time')  # capture time in string format i.e 10 minutes
        timeInt = int(time.split()[0])  # take only the first part, convert to int i.e 10
        target = request.POST.getlist('target_area')
        target_list = ", ".join(target)
        equipment = request.POST.getlist('equipment')
        equipment_list = ", ".join(equipment)  # comma-separated, remove list format []
        custom_equipment = request.POST.get('custom_equipment', '')  # Default to '' if not provided
        custom_target = request.POST.get('custom_target', '')
        completed = request.POST.get('completed', False)  # Default to False if not checked


        # ChatGPT-generated prompt
        chatGPT_generated_prompt = f"""
Generate a personalized workout plan in JSON format, based on the following user inputs:

- **Duration**: {timeInt} minutes
- **Target Areas**: {target_list}
- **Equipment**: {equipment_list}
- **Custom Equipment**: {custom_equipment or 'None'}
- **Custom Target Areas**: {custom_target or 'None'}

### Requirements:

1. **Workout Sections**:
    - Always include the following sections:
        - **Warm-up**
        - **Cool Down**
    - Adjust the warm-up and cool down durations based on the total workout time:
        - For shorter workouts (e.g., under 15 minutes), allocate minimal time (e.g., 1-2 minutes) for warm-up and cool down.
        - For longer workouts (e.g., 45-60 minutes or more), allocate more time for a thorough warm-up and cool down (e.g., 4-5 minutes each) to ensure safety and recovery.
        - Ensure that the time spent on warm-up and cool down is proportionate to the total workout time, balancing efficiency and health considerations, it shouldn't be longer than 5 minutes.
    - Automatically include sections such as **Cardio**, **Strength Training**, or **Flexibility** based on the target areas and equipment provided, ensuring the main workout time is focused on core exercises.

2. **Exercise Details**:
    - For each section, generate exercises with the following attributes:
        - **Name** of the exercise
        - **Sets** (number of sets, or 'None' for time-based exercises that don't have sets/rows like stretching, arm circles, rowing or treadmill or hiking and only focus on time)
        - **Reps** (number of repetitions, or 'None' for time-based exercises that won't have sets/rows as they only focus on time such as strentching or treadmill)
        - **Time** (duration of the exercise in minutes)
        - **Target Area** (the body part being targeted)
        - **Equipment** needed for each exercise (default to bodyweight if no equipment is provided)
    - Ensure the exercises are varied and balanced, avoiding unnecessary repetition and focusing on the diversity and the target of the user.
    - Still ensure the user is getting a good workout in, enough to get a burn or heart beating. 
    - for certain warmups or cool downs that rely on time, you don't need to include 'reps' and 'sets' i.e jumping jacks, arm circles, walking lunges. 

3. **Customization Options**:
    - Integrate custom equipment and target areas if provided by the user ({custom_equipment}, {custom_target}).
    - If no equipment or custom input is provided, default to bodyweight exercises.

4. **Focus and Balance**:
    - Distribute workout time effectively:
        - Warm-up and cool down durations should be determined based on the total workout time, ensuring both are reasonable and suitable for the intensity of the session.
        - Make sure the time allocated is reasonable for the workout i.e 50 jumping jacks should only take long, maybe 3 minutes.
        - The remaining time should focus on the core workout, with exercises relevant to the target areas and equipment, make sure to include body weight exercises. For example if they only include treadmill, still incorporate body weight workouts that fit their targets.
    - Avoid over-emphasizing warm-up or cool down unless necessary for longer sessions, while maintaining a focus on effective and challenging core exercises, providing relevent options for user.
    - Make sure {time} that the user provides is accurately represented in each 'section' and 'items' sum up correctly to {time} i.e if user provides 30 minutes, the warmup, cooldown, and workout sections SUM OF ALL should all be 30 minutes only! Example: 

5. **Correct Time**:
    - "Make sure the total workout time strictly matches the user input.
    - If a user specifies a time (e.g., 60 minutes), the sum of all sections (warm-up, cardio, strength training, and cool down) must add up to that exact duration. 
    - Adjust the number of exercises, sets, and reps accordingly to fit the total workout time without exceeding or falling short. Be precise and efficient with time allocations for each section, and remember to keep the workout balanced."
For example! 
Time: 30

Target: Core/Abs, Full Body

Equipment: Bodyweight

Workout Sections:

Warm-up

Dynamic Stretches
Time: 2 minutes
Sets: None
Reps: None
Target Area: Full Body
Equipment Needed: Bodyweight

High Knees
Time: 2 minutes
Sets: 1
Reps: 60
Target Area: Full Body
Equipment Needed: Bodyweight

Cardio

Rowing
Time: 10 minutes
Sets: None
Reps: None
Target Area: Full Body
Equipment Needed: Rowing Machine

Mountain Climbers
Time: 5 minutes
Sets: 3
Reps: 20
Target Area: Core/Abs
Equipment Needed: Bodyweight

Strength Training

Plank
Time: 3 minutes
Sets: 3
Reps: 1
Target Area: Core/Abs
Equipment Needed: Bodyweight

Burpees
Time: 5 minutes
Sets: 3
Reps: 15
Target Area: Full Body
Equipment Needed: Bodyweight

Cool Down

Standing Forward Fold
Time: 2 minutes
Sets: None
Reps: None
Target Area: Full Body
Equipment Needed: Bodyweight

Seated Toe Reach
Time: 1 minutes
Sets: None
Reps: None
Target Area: Core/Abs
Equipment Needed: Bodyweight

{timeInt} is correct and matches to 30 minutes, do the same!
Also, notice how small warmups or cool downs like stretches or small workouts are none as they dont need reps or sets and relies on time. 

Example, workout is standing or strentching, sets: None reps: None, just use time
5. **Output Format**:
    
        - Return the workout plan in **JSON** format, with each section as a key.
        """

        response = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "user",
                    "content": chatGPT_generated_prompt
                },
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "workout_schema",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "time": {"type": "integer"},
                            "target": {"type": "array", "items": {"type": "string"}},
                            "equipment": {"type": "array", "items": {"type": "string"}},
                            "sections": {
                                "type": "object",
                                "properties": {
                                    "Warm-up": {"type": "array", "items": {"type": "object", "properties": {
                                        "name": {"type": "string"},
                                        "time": {"type": "integer"},
                                        "sets": {"type": "integer"},
                                        "reps": {"type": "integer"},
                                        "target_area": {"type": "string"},
                                        "equipment_needed": {"type": "string"}
                                    }}},
                                    "Cardio": {"type": "array", "items": {"type": "object", "properties": {
                                        "name": {"type": "string"},
                                        "time": {"type": "integer"},
                                        "sets": {"type": "integer"},
                                        "reps": {"type": "integer"},
                                        "target_area": {"type": "string"},
                                        "equipment_needed": {"type": "string"}
                                    }}},
                                    "Cool Down": {"type": "array", "items": {"type": "object", "properties": {
                                        "name": {"type": "string"},
                                        "time": {"type": "integer"},
                                        "sets": {"type": "integer"},
                                        "reps": {"type": "integer"},
                                        "target_area": {"type": "string"},
                                        "equipment_needed": {"type": "string"}
                                    }}}
                                }
                            }
                        }
                    }
                }
            }
        )

        workout_plan_json = json.loads(response.choices[0].message.content) # parse using json.loads > converted to dictionary
        
        
         # Will combine given targets and equipment with custom targets and equipment, comma separated, if empty, output is None. 

        full_target_list = target_list
        full_equipment_list = equipment_list
        if custom_target:
            full_target_list = f"{target_list}, {custom_target}".strip(", ")
        
        if custom_equipment:
            full_equipment_list = f"{equipment_list}, {custom_equipment}".strip(", ")

        if not full_target_list:
           full_target_list = 'None'

        if not full_equipment_list:
            full_equipment_list = 'None'

        # temporarily store workout data in a session to use later in order to display in history or not 
        request.session['workout_data'] = workout_plan_json
        request.session['full_equipment_list'] = full_equipment_list
        request.session['full_target_list'] = full_target_list
        request.session['time'] = time

        return render(request, 'core/workout.html', {
            'workout_data': workout_plan_json,
            'full_equipment_list': full_equipment_list,
            'full_target_list': full_target_list
        })
    else:
        return JsonResponse({'error': 'POST NOT DETECTED, METHOD NOT ALLOWED'}, status=405)
    

def save_workout(request):  #save to DB only if completed 
    if request.method == 'POST':  # Retrieve the temp session data from previous view
        workout_plan_json = request.session.get('workout_data')    
        full_equipment_list = request.session.get('full_equipment_list')
        full_target_list = request.session.get('full_target_list')
        time = request.session.get('time')
        completed = request.POST.get('completed', 'False') 
        is_completed = completed == 'True'
        #save workout plan (lalo code here)
        workout_plan = WorkoutPlan.objects.create(
            user=request.user,
            duration=time,
            full_equipment_list = full_equipment_list,
            full_target_list = full_target_list,
            workout_data = workout_plan_json,
            completed = is_completed
        )
        workout_plan.save()
    
        del request.session['workout_data']
        del request.session['full_equipment_list']
        del request.session['full_target_list']
        del request.session['time']


    return redirect('home')
    

    
# display completed workouts in history.html 
def display_workout_history(request):
    workout_history = WorkoutPlan.objects.filter(user=request.user, completed=True).order_by('-created_at') #queries workoutplan mode DB, filter
    #print(workout_history) #test
    return render(request, 'core/history.html', { #queryset
        'workouts': workout_history #workout     
        }) 
