import os
import hmac
import hashlib
import time
from typing import Dict, Tuple
from fastapi import FastAPI, Request, HTTPException, Header
from anthropic import Anthropic
import redis

app = FastAPI(title="AgentBreaker-Enterprise-Cluster-Gateway")

# Initialize the Live Anthropic Production Cloud Client Node
anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", "your-api-key-here"))

# Initialize the Centralized Enterprise Shared-State Database
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Cryptographic master verification key anchors
AABC_SECRET_KEY = b"enterprise_billion_dollar_anchor_key"

class ClusterCircuitBreaker:
    def __init__(self):
        self.time_window_seconds = 5.0  
        self.max_allowed_triggers = 3   

    def verify_agent_integrity(self, agent_id: str, prompt_payload: str, signature: str) -> bool:
        message_bytes = f"{agent_id}:{prompt_payload}".encode('utf-8')
        expected_signature = hmac.new(AABC_SECRET_KEY, message_bytes, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected_signature, signature)

    def enforce_distributed_breaker(self, payload_hash: str) -> Tuple[bool, str]:
        current_time = time.time()
        cutoff_time = current_time - self.time_window_seconds
        redis_key = f"agent_coherence:{payload_hash}"

        try:
            redis_client.zremrangebyscore(redis_key, 0, cutoff_time)
            redis_client.zadd(redis_key, {str(current_time): current_time})
            redis_client.expire(redis_key, 10)
            total_cluster_hits = redis_client.zcard(redis_key)

            if total_cluster_hits > self.max_allowed_triggers:
                return True, f"🛑 CRITICAL INTERCEPT: Distributed Loop Triggered. {total_cluster_hits} hits across fleet."
                
            return False, "CLEAR"
        except redis.RedisError as db_error:
            return True, f"SECURITY ERROR: Core state database unreachable: {str(db_error)}"

security_engine = ClusterCircuitBreaker()

@app.post("/v1/agent/execute")
async def execute_live_cluster_transaction(
    request: Request,
    x_agent_id: str = Header(...),
    x_agent_signature: str = Header(...)
):
    body_bytes = await request.body()
    prompt_content = body_bytes.decode('utf-8')
    
    if not security_engine.verify_agent_integrity(x_agent_id, prompt_content, x_agent_signature):
        raise HTTPException(status_code=401, detail="SECURITY FAILURE: Cryptographic signature mismatch.")
        
    payload_hash = hashlib.md5(body_bytes).hexdigest()
    is_blocked, alert_message = security_engine.enforce_distributed_breaker(payload_hash)
    
    if is_blocked:
        raise HTTPException(status_code=423, detail=alert_message)
        
    try:
        response = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt_content}]
        )
        return {
            "status": "SUCCESS",
            "agent_id": x_agent_id,
            "raw_output": response.content.text
        }
    except Exception as api_error:
        raise HTTPException(status_code=502, detail=f"Upstream Cloud Endpoint Error: {str(api_error)}")
