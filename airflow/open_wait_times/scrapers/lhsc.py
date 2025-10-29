from .base import BaseScraper
from httpx import get
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


class LHSC(BaseScraper):
    def scrape(self) -> None:
        response = get(self.url)
        response.raise_for_status()
        s3 = S3Hook(aws_conn_id="garage_s3")
        s3.load_string(
            string_data=response.text,
            key=f"{self.name}/{self.dept}/{self._id}_scraper_v{self.version}_{self.ts}.html",
            bucket_name="open-wait-times",
        )

    def parse(self) -> None:
        pass

    def save(self) -> None:
        pass
