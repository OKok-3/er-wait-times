import os
import sys
from importlib import import_module
from pendulum import datetime
from airflow.sdk import dag, task

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from registry import Registry

registry = Registry()
registry.register()

for hospital in registry.hospitals:
    dag_id = f"extract_data_{hospital['id']}"

    def create_dag(hospital_config: dict[str, any]):
        name = hospital_config["name"]
        dept = hospital_config["dept"]
        scraper_module = import_module(hospital_config["scraper_module"])
        scraper_class = getattr(scraper_module, hospital_config["scraper_class"])

        @dag(
            dag_id=f"extract_data_{hospital_config['id']}",
            dag_display_name=f"{name} {dept} Wait Times",
            tags=["Open Wait Times"],
            start_date=datetime(2025, 1, 1),
            catchup=False,
            params={**hospital_config},
        )
        def extract_data() -> None:
            scraper = scraper_class(hospital_config)

            @task
            def scrape(ts: str) -> dict[str, str]:
                data = scraper.scrape(ts)
                return data

            @task
            def parse(data: dict[str, str]) -> dict[str, any]:
                data = scraper.parse(data)
                return data

            @task
            def load_data(data: dict[str, any]) -> None:
                scraper.load_data(data)

            load_data(parse(scrape()))

        return extract_data()

    globals()[dag_id] = create_dag(hospital)
