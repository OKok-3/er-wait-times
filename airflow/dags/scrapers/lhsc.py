import re
import httpx
from datetime import datetime

from base import BaseScraper


class LHSC(BaseScraper):
    def scrape(self) -> None:
        response = httpx.get(self.url)
        response.raise_for_status()
        # TODO: change to S3
        with open(f"./{self._id}_v{self.version}.html", "w") as f:
            f.write(response.text)

    def parse(self) -> None:
        # TODO: change to S3
        with open(f"./{self._id}_v{self.version}.html", "r") as f:
            html = f.read()

        match self._id:
            case "lhsc_vh_adult_er":
                keyword = "VH"
            case "lhsc_uh_adult_er":
                keyword = "UH"
            case "lhsc_ch_er":
                keyword = "CH"
            case _:
                raise ValueError(f"Invalid ID: {self._id}")

        wait_time_re = f"<!--Start:{keyword}WaitTimeValue-->(.*?)<!--End:{keyword}WaitTimeValue-->"
        time_updated_re = f"<!--Start:{keyword}WaitTimeUpdated-->(.*?)<!--End:{keyword}WaitTimeUpdated-->"

        wait_time_raw = re.findall(wait_time_re, html, re.DOTALL)[0].strip().lower()
        time_updated_raw = re.findall(time_updated_re, html, re.DOTALL)[0].strip().lower()

        # Convert wait time to minutes
        if "hours" in wait_time_raw:
            wait_time = int(float(wait_time_raw.split(" ")[0]) * 60)
        else:
            wait_time = int(wait_time_raw.split(" ")[0])

        # Convert time updated to datetime
        time_updated = datetime.strptime(time_updated_raw, "%H:%M %p").time()

        print(wait_time, time_updated)

    def save(self) -> None:
        pass
