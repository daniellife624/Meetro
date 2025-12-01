from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ───────────────────────────────
# In-Memory Database
# ───────────────────────────────
matches = []
match_id_counter = 1


class Match(BaseModel):
    id: int
    sender_id: str
    receiver_id: str
    status: str  # Pending / Confirmed / Rejected


class CreateMatchRequest(BaseModel):
    sender_id: str
    receiver_id: str


class UpdateStatusRequest(BaseModel):
    status: str  # Confirmed / Rejected


# ───────────────────────────────
# Create Match (Receiver accepts invitation)
# ───────────────────────────────
@app.post("/match", response_model=Match)
def create_match(data: CreateMatchRequest):
    global match_id_counter
    new_match = Match(
        id=match_id_counter,
        sender_id=data.sender_id,
        receiver_id=data.receiver_id,
        status="Pending",
    )
    match_id_counter += 1
    matches.append(new_match)
    return new_match


# ───────────────────────────────
# Query history by receiver
# ───────────────────────────────
@app.get("/match/{receiver_id}")
def list_matches(receiver_id: str):
    pending = [
        m for m in matches if m.receiver_id == receiver_id and m.status == "Pending"
    ]
    confirmed = [
        m for m in matches if m.receiver_id == receiver_id and m.status == "Confirmed"
    ]
    return {"pending": pending, "confirmed": confirmed}


# ───────────────────────────────
# Update match status
# ───────────────────────────────
@app.patch("/match/{match_id}", response_model=Match)
def update_match(match_id: int, data: UpdateStatusRequest):
    for m in matches:
        if m.id == match_id:
            m.status = data.status
            return m
    return {"error": "Match not found"}
