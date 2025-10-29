import re
from .base import BaseScraper
from httpx import get
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


class LHSC(BaseScraper):
    def scrape(self, ts: str) -> dict[str, str]:
        response = get(self.url)
        response.raise_for_status()

        s3 = S3Hook(aws_conn_id="garage_s3")
        filename = f"{self.name}/{self.dept}/{self._id}_scraper_v{self.version}_{ts}.html"
        s3.load_string(
            string_data=response.text,
            key=filename,
            bucket_name="open-wait-times",
        )

        return {
            "filename": filename,
            "task_timestamp": ts,
        }

    def parse(self, data: dict[str, str]) -> dict[str, any]:
        s3 = S3Hook(aws_conn_id="garage_s3")
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

        data["wait_time"] = wait_time_match.group(1).strip() if wait_time_match else None
        data["time_updated"] = time_updated_match.group(1).strip() if time_updated_match else None

        return data

    def save(self, data: dict[str, any]) -> None:
        pass
