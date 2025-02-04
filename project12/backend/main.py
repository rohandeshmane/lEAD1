from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from supabase import create_client, Client as SupabaseClient
from datetime import datetime
import json

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase: SupabaseClient = create_client(
    os.getenv("VITE_SUPABASE_URL"),
    os.getenv("VITE_SUPABASE_ANON_KEY")
)

# Initialize Twilio client
twilio_client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    content: str
    phone_number: str
    type: str = "sms"  # sms or whatsapp

class CallRequest(BaseModel):
    phone_number: str
    lead_id: str

@app.post("/api/send-message")
async def send_message(message: Message):
    try:
        # Determine if it's WhatsApp or SMS
        from_number = (
            f"whatsapp:{os.getenv('TWILIO_WHATSAPP_NUMBER')}"
            if message.type == "whatsapp"
            else os.getenv('TWILIO_PHONE_NUMBER')
        )
        to_number = (
            f"whatsapp:{message.phone_number}"
            if message.type == "whatsapp"
            else message.phone_number
        )

        # Send message via Twilio
        twilio_message = twilio_client.messages.create(
            body=message.content,
            from_=from_number,
            to=to_number
        )

        # Store in Supabase
        communication = supabase.table('communications').insert({
            'type': message.type,
            'direction': 'outbound',
            'status': twilio_message.status,
            'twilio_sid': twilio_message.sid
        }).execute()

        return {"status": "success", "message_sid": twilio_message.sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/initiate-call")
async def initiate_call(call: CallRequest):
    try:
        # Start a call via Twilio
        twilio_call = twilio_client.calls.create(
            url=f"{os.getenv('BASE_URL')}/api/handle-call",
            to=call.phone_number,
            from_=os.getenv('TWILIO_PHONE_NUMBER')
        )

        # Store call info in Supabase
        communication = supabase.table('communications').insert({
            'type': 'call',
            'direction': 'outbound',
            'status': twilio_call.status,
            'lead_id': call.lead_id,
            'twilio_sid': twilio_call.sid
        }).execute()

        return {"status": "success", "call_sid": twilio_call.sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/handle-call")
async def handle_call():
    response = VoiceResponse()
    response.say("Hello! Thank you for your interest. How can I help you today?")
    return {"twiml": str(response)}

@app.post("/api/webhook/twilio")
async def twilio_webhook(data: dict):
    try:
        # Update communication status in Supabase
        if "MessageSid" in data:
            supabase.table('communications').update({
                'status': data['MessageStatus']
            }).eq('twilio_sid', data['MessageSid']).execute()
        elif "CallSid" in data:
            supabase.table('communications').update({
                'status': data['CallStatus'],
                'duration': data.get('CallDuration', 0)
            }).eq('twilio_sid', data['CallSid']).execute()

        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/leads")
async def get_leads():
    try:
        response = supabase.table('leads').select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/communications/{lead_id}")
async def get_communications(lead_id: str):
    try:
        response = supabase.table('communications').select("*").eq('lead_id', lead_id).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics")
async def get_analytics():
    try:
        # Get analytics data from Supabase
        leads = supabase.table('leads').select("*").execute()
        communications = supabase.table('communications').select("*").execute()
        
        # Process analytics
        total_leads = len(leads.data)
        total_communications = len(communications.data)
        
        return {
            "total_leads": total_leads,
            "total_communications": total_communications,
            "leads_by_source": {},  # Process leads by source
            "communication_stats": {}  # Process communication statistics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))