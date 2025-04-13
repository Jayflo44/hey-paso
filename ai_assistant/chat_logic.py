from fastapi import FastAPI, Request                                                                                                                                                                          
from fastapi.responses import FileResponse, JSONResponse                                                                                                                                                       
from fastapi.staticfiles import StaticFiles                                                                                                                                                                    
from fastapi.middleware.cors import CORSMiddleware                                                                                                                                                             
from pydantic import BaseModel                                                                                                                                                                                 
import google.generativeai as genai                                                                                                                                                                            
from dotenv import load_dotenv                                                                                                                                                                                 
import os                                                                                                                                                                                                      
                          
#import helper functions
from ai_assistant.maps import generate_maps_url
from ai_assistant.reservations import (
    generate_opentable_url,
    generate_fandango_url,
    generate_eventbrite_url
)
                                                                                                                     
load_dotenv()                                                                                                                                                                                                  
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))                                                                                                                                                           
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")       
                                                                                                                                
app = FastAPI()                                                                                                                                                                                                

#CORS
# Allow frontend JS to call backend                                                                                                                                                                            
app.add_middleware(                                                                                                                                                                                            
    CORSMiddleware,                                                                                                                                                                                            
    allow_origins=["*"],  # Or ["http://localhost:8000"] for strict                                                                                                                                            
    allow_credentials=True,                                                                                                                                                                                        allow_methods=["*"],                                                                                                                                                                                      
    allow_headers=["*"],                                                                                                                                                                                       
)                                                                                                                                                                                                                                                                                                                                                                                                                             
# Serve static files like index.html                                                                                                                                                                           
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")                                                                                                                                                                                                  
def get_index():                                                                                                                                                                                               
    return FileResponse("static/index.html")        
                                                                                                                                                                                                                                                                                                                                                                          
# Your AI API route              
#prompt input                                                                                                                                                                              
class Prompt(BaseModel):                                                                                                                                                                                       
    text: str                        
                                                                                                                                                                                                                                                                                                                                                                                             
@app.post("/generate")
async def generate_text(prompt: Prompt):
    user_input = prompt.text.lower()

    # Maps intent
    if any(keyword in user_input for keyword in ["where is", "show me", "map", "directions to"]):
        location = user_input.replace("where is", "").replace("show me", "").strip()
        map_url = generate_maps_url(location)
        return {"response": f"Here’s the map for that location: {map_url}"}

    #Reservation intent (OpenTable)
    elif any(keyword in user_input for keyword in ["reserve", "book", "reservation", "table at"]):
        if "table at" in user_input:
            restaurant = user_input.split("table at")[-1].strip()
        else:
            restaurant = user_input.replace("reserve", "").replace("book", "").strip()
        reservation_url = generate_opentable_url(restaurant)
        return {"response": f"Here's the reservation link for {restaurant}: {reservation_url}"}

    # Fandango intent (movies)
    elif any(keyword in user_input for keyword in ["movie", "showtime", "theater", "cinemark"]):
        movie = user_input.replace("find tickets for", "").replace("movie", "").replace("at", "").strip()
        movie_url = generate_fandango_url(movie)
        return {"response": f"Here’s the Fandango link: {movie_url}"}

    # Eventbrite intent (events)
    elif any(keyword in user_input for keyword in ["event", "concert", "festival", "weekend", "eventbrite"]):
        query = user_input.replace("find", "").replace("events", "").replace("event", "").strip()
        event_url = generate_eventbrite_url(query)
        return {"response": f"Here’s what’s happening in El Paso: {event_url}"}

    #Default to Gemini AI
    try:
        response = model.generate_content(prompt.text)
        return {"response": response.text}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
