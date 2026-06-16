# 🛑 AgentBreaker: Multi-Agent Algorithmic Loop Interceptor

An ultra-lightweight, sub-millisecond cryptographic safety shim designed to prevent cascading autonomous AI agent loops, rogue transactional cycles, and automated financial panic spirals at the network boundary.

## ⚖️ Commercial Enterprise Inquiries
This project is protected under the Business Source License 1.1 (BSL 1.1). Commercial production scale deployments handling greater than 50 concurrent autonomous agents or over $10,000 in monthly transaction volume require a commercial enterprise agreement license.

For production licensing, custom multi-cloud cloud infrastructure blueprints, or strategic procurement inquiries, contact our corporate gateway directly:
📩 mahima.saigal@gmail.com


import os
import hmac
import hashlib
import time
from typing import Dict, Tuple
from fastapi import FastAPI, Request, HTTPException, Header

app = FastAPI(title="AABC-Core-Gateway")

AABC_SECRET_KEY = b"enterprise_billion_dollar_anchor_key"

class AABCCoreProxy:
    def __init__(self):
        self.signature_velocity_ledger: Dict[str, list] = {}
        self.max_velocity_threshold = 3 

    def verify_agent_integrity(self, agent_id: str, tx_payload: str, incoming_signature: str) -> bool:
        message_bytes = f"{agent_id}:{tx_payload}".encode('utf-8')
        expected_signature = hmac.new(AABC_SECRET_KEY, message_bytes, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected_signature, incoming_signature)

    def enforce_circuit_breaker(self, payload_hash: str) -> Tuple[bool, str]:
        current_time = time.time()
        if payload_hash not in self.signature_velocity_ledger:
            self.signature_velocity_ledger[payload_hash] = []
        self.signature_velocity_ledger[payload_hash] = [
            t for t in self.signature_velocity_ledger[payload_hash] if current_time - t <= 5.0
        ]
        self.signature_velocity_ledger[payload_hash].append(current_time)
        if len(self.signature_velocity_ledger[payload_hash]) > self.max_velocity_threshold:
            return True, "CRITICAL: Systemic Multi-Agent Loop Intercepted. Token Isolated."
        return False, "CLEAR"

proxy_engine = AABCCoreProxy()

@app.post("/v1/agent/execute")
async def intercept_and_enforce(
    request: Request,
    x_agent_id: str = Header(...),
    x_agent_signature: str = Header(...)
):
    body = await request.body()
    payload_str = body.decode('utf-8')
    if not proxy_engine.verify_agent_integrity(x_agent_id, payload_str, x_agent_signature):
        raise HTTPException(status_code=401, detail="UNAUTHORIZED AGENT: Cryptographic token validation failed.")
    payload_hash = hashlib.md5(body).hexdigest()
    is_blocked, message = proxy_engine.enforce_circuit_breaker(payload_hash)
    if is_blocked:
        raise HTTPException(status_code=423, detail=message)
    return {"status": "SUCCESS", "message": "Transaction verified and routed securely."}
