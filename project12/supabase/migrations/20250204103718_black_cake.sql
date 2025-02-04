/*
  # Initial Schema Setup for Lead Management System

  1. New Tables
    - `leads`
      - Basic lead information
      - Contact details
      - Status tracking
    - `communications`
      - Track all communications (calls, messages, WhatsApp)
      - Link to leads
    - `call_logs`
      - Detailed call records
      - Call metrics
    - `messages`
      - SMS and WhatsApp messages
      - Message status tracking

  2. Security
    - Enable RLS on all tables
    - Add policies for authenticated users
*/

-- Create leads table
CREATE TABLE IF NOT EXISTS leads (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  first_name text NOT NULL,
  last_name text,
  email text,
  phone text,
  company text,
  source text NOT NULL,
  status text NOT NULL DEFAULT 'new',
  score integer DEFAULT 0,
  last_contact timestamptz,
  notes text,
  assigned_to uuid REFERENCES auth.users(id)
);

-- Create communications table
CREATE TABLE IF NOT EXISTS communications (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at timestamptz DEFAULT now(),
  lead_id uuid REFERENCES leads(id) ON DELETE CASCADE,
  type text NOT NULL, -- 'call', 'sms', 'whatsapp'
  direction text NOT NULL, -- 'inbound', 'outbound'
  status text NOT NULL,
  duration integer, -- for calls
  content text,
  twilio_sid text -- Twilio's unique identifier
);

-- Create call_logs table
CREATE TABLE IF NOT EXISTS call_logs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at timestamptz DEFAULT now(),
  communication_id uuid REFERENCES communications(id) ON DELETE CASCADE,
  lead_id uuid REFERENCES leads(id) ON DELETE CASCADE,
  duration integer,
  recording_url text,
  call_status text NOT NULL,
  price decimal(10,2),
  transcript text
);

-- Create messages table
CREATE TABLE IF NOT EXISTS messages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at timestamptz DEFAULT now(),
  communication_id uuid REFERENCES communications(id) ON DELETE CASCADE,
  lead_id uuid REFERENCES leads(id) ON DELETE CASCADE,
  body text NOT NULL,
  status text NOT NULL,
  media_url text[],
  twilio_sid text
);

-- Enable RLS
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE communications ENABLE ROW LEVEL SECURITY;
ALTER TABLE call_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view assigned leads"
  ON leads FOR SELECT
  TO authenticated
  USING (assigned_to = auth.uid() OR auth.uid() IN (
    SELECT id FROM auth.users WHERE role = 'admin'
  ));

CREATE POLICY "Users can insert leads"
  ON leads FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Users can update assigned leads"
  ON leads FOR UPDATE
  TO authenticated
  USING (assigned_to = auth.uid() OR auth.uid() IN (
    SELECT id FROM auth.users WHERE role = 'admin'
  ));

-- Communications policies
CREATE POLICY "Users can view related communications"
  ON communications FOR SELECT
  TO authenticated
  USING (
    lead_id IN (
      SELECT id FROM leads WHERE assigned_to = auth.uid()
    ) OR auth.uid() IN (
      SELECT id FROM auth.users WHERE role = 'admin'
    )
  );

CREATE POLICY "Users can insert communications"
  ON communications FOR INSERT
  TO authenticated
  WITH CHECK (true);

-- Similar policies for call_logs and messages
CREATE POLICY "Users can view related call_logs"
  ON call_logs FOR SELECT
  TO authenticated
  USING (
    lead_id IN (
      SELECT id FROM leads WHERE assigned_to = auth.uid()
    ) OR auth.uid() IN (
      SELECT id FROM auth.users WHERE role = 'admin'
    )
  );

CREATE POLICY "Users can view related messages"
  ON messages FOR SELECT
  TO authenticated
  USING (
    lead_id IN (
      SELECT id FROM leads WHERE assigned_to = auth.uid()
    ) OR auth.uid() IN (
      SELECT id FROM auth.users WHERE role = 'admin'
    )
  );

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_leads_assigned_to ON leads(assigned_to);
CREATE INDEX IF NOT EXISTS idx_communications_lead_id ON communications(lead_id);
CREATE INDEX IF NOT EXISTS idx_call_logs_lead_id ON call_logs(lead_id);
CREATE INDEX IF NOT EXISTS idx_messages_lead_id ON messages(lead_id);