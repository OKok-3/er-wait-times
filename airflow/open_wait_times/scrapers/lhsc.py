import re
import pandas as pd
from .base import BaseScraper
from pendulum import parse
from httpx import get
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook


class LHSC(BaseScraper):
    def scrape(self, ts: str) -> dict[str, str]:
        response = get(self.url)
        response.raise_for_status()

        s3 = S3Hook(aws_conn_id="garage-s3")
        filename = f"{self.name}/{self.dept}/{self._id}_scraper_v{self.version}_{ts}.html"
        s3.load_string(
            string_data=response.text,
            key=filename,
            bucket_name="open-wait-times",
        )

        return {
            "filename": filename,
            "fetch_ts": ts,
        }

    def parse(self, data: dict[str, str]) -> dict[str, any]:
        s3 = S3Hook(aws_conn_id="garage-s3")
        html = str(s3.read_key(key=data["filename"], bucket_name="open-wait-times"))

        hospital_identifier = self._id.split("_")[1].upper()
        wait_time_re = (
            f"<!--Start:{hospital_identifier}WaitTimeValue-->(.*?)<!--End:{hospital_identifier}WaitTimeValue-->"
        )
        time_updated_re = (
            f"<!--Start:{hospital_identifier}WaitTimeUpdated-->(.*?)<!--End:{hospital_identifier}WaitTimeUpdated-->"
        )

        wait_time_match = re.search(wait_time_re, html)
        time_updated_match = re.search(time_updated_re, html)

        data["wait_duration"] = wait_time_match.group(1).strip() if wait_time_match else None
        data["update_ts"] = time_updated_match.group(1).strip() if time_updated_match else None

        return data

    def save(self, data: dict[str, any]) -> None:
        pg = PostgresHook(postgres_conn_id="owt-pg")

        # We won't do None/Null checks and will rely on pipeline failing to catch this
        hospital_id = self._id
        fetch_ts = parse(data["fetch_ts"], strict=False)
        update_ts = parse(data["update_ts"], strict=False, tz="America/Toronto")

        wait_duration = pd.to_timedelta(data["wait_duration"].lower().strip())
        patient_arrival_time = update_ts.subtract(minutes=int(wait_duration.total_seconds() / 60))
        patient_departure_time = update_ts
        extra_info = None

        # TODO: Conflict will be dealt with by the to-be-implemented file hash checking step
        pg.insert_rows(
            table="owt.er_wait_times",
            rows=[
                (
                    hospital_id,
                    fetch_ts,
                    update_ts,
                    wait_duration,
                    patient_arrival_time,
                    patient_departure_time,
                    extra_info,
                )
            ],
            target_fields=[
                "hospital_id",
                "fetch_ts",
                "update_ts",
                "wait_duration",
                "patient_arrival_time",
                "patient_departure_time",
                "extra_info",
            ],
        )
