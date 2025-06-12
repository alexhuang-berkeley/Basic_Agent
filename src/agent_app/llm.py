"""AWS Bedrock LLM invocation helpers."""

from __future__ import annotations

import json
import logging
from typing import Any

try:
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError
except Exception:  # pragma: no cover - boto3 may not be installed
    boto3 = None
    BotoCoreError = ClientError = Exception

logger = logging.getLogger(__name__)


def invoke_bedrock(prompt: str, model_id: str, *, max_tokens: int = 512, temperature: float = 0.1) -> str:
    """Invoke an AWS Bedrock model and return the response text.

    This function expects `boto3` to be configured with appropriate AWS
    credentials and region. Errors are logged and re-raised.
    """
    if boto3 is None:
        raise RuntimeError("boto3 is required to call Bedrock")

    client = boto3.client("bedrock-runtime")
    body = json.dumps({"prompt": prompt, "max_tokens_to_sample": max_tokens, "temperature": temperature})

    try:
        response = client.invoke_model(modelId=model_id, body=body, accept="application/json", contentType="application/json")
        result = json.loads(response["body"].read())
        return result.get("completion", "")
    except (BotoCoreError, ClientError) as exc:
        logger.error("Bedrock invocation failed: %s", exc)
        raise
