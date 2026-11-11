from fastapi import FastAPI

app = FastAPI()

participants = [
    {"id" : 1, "name" : "Alex", "discipline" : "basketball"},
    {"id" : 2, "name" : "Artem", "discipline" : "chess"},
    {"id" : 3, "name" : "Bob", "discipline" : "football"},
    {"id" : 4, "name" : "Burger", "discipline" : "chess"},
    {"id" : 5, "name" : "Sandy", "discipline" : "basketball"},
    {"id" : 6, "name" : "Artur", "discipline" : "football"}
]
events = [
    {"event" : "football"},
    {"event" : "basketball"},
    {"event" : "chess"}
]

@app.get("/")
async def root():
    return "This is an official website for the future sports festival!\n"\
        "Please look at the events, that you can participate in\n"\
        "P.S: type /events"

@app.get("/events/")
async def get_events():
    return events


@app.get("/events/football/")
async def get_football():
    return [
        person for person in participants if person["discipline"] == "football"
    ]

@app.get("/events/basketball/")
async def get_basketball():
    return [
        person for person in participants if person["discipline"] == "basketball"
    ]

@app.get("/events/chess/")
async def get_chess():
    return [
        person for person in participants if person["discipline"] == "chess"
    ]

@app.post("/events/football/approval")
async def register_football(name: str):
    participants.append({
        "id" : len(participants) + 1,
        "name" : name,
        "discipline" : "football"
    })

    return {"message" : "Succes!"}

@app.post("/events/basketball/approval")
async def register_basketball(name: str):
    participants.append({
        "id" : len(participants) + 1,
        "name" : name,
        "discipline" : "basketball"
    })

    return {"message" : "Succes!"}

@app.post("/events/chess/approval")
async def register_chess(name: str):
    participants.append({
        "id" : len(participants) + 1,
        "name" : name,
        "discipline" : "chess"
    })

    return {"message" : "Succes!"}