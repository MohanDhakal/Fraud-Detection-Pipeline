from datetime import datetime, timezone
from typing import Any
from uuid import uuid4
import json
import boto3
from botocore.exceptions import ClientError, BotoCoreError
import logging

logger = logging.getLogger(__name__)

_AWS_PROFILE = "cdc-uploader"
_AWS_REGION = "ap-southeast-2"
_S3_BUCKET = "raw-transactions-364077344368-ap-southeast-2-an"


class CloudService:
    def __init__(self):
        self.profile = _AWS_PROFILE
        self.region = _AWS_REGION
        self.bucket = _S3_BUCKET

    def setup_s3_client():
        session = boto3.Session(profile_name=_AWS_PROFILE)
        return session.client("s3", region_name=_AWS_REGION)

    def test_caller_identity(self):
        session = boto3.Session(profile_name=_AWS_PROFILE)
        available_profiles = session.available_profiles
        print(f"AvailableProfiles: {available_profiles}")

    def upload_to_s3(
        self,
        data: dict,
        table_name: str,
        client,
    ) -> dict[str, Any]:
        timestamp = datetime.now(timezone.utc)
        object_key = (
            f"transactions/{table_name}/"
            f"{timestamp.strftime('%Y/%m/%d/%H')}/"
            f"{uuid4().hex}.json"
        )
        json_data = json.dumps(data, default=str)
        if client is None:
            return {"error": "Please setup the s3 client first"}
        try:
            response = client.put_object(
                Bucket=_S3_BUCKET,
                Key=object_key,
                Body=json_data.encode("utf-8"),
                ContentType="application/json",
            )
            status_code = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
            logger.info(
                "S3 upload successful | bucket=%s | key=%s | status=%s",
                _S3_BUCKET,
                object_key,
                status_code,
            )
            return {"msg": response.get("ResponseMetadata", {})}

        except ClientError as e:
            return {"error": e}
        except BotoCoreError as e:
            return {"error": e}
        except Exception as e:
            return {"error": "Unexpected Failure while uplaoindg CDC event to aws"}
