import os

from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("API_KEY")


class ManusAi:
    TASK_URL = "https://api.manus.ai/v1/tasks"
    HEADERS = {
        "API_KEY": f"{API_KEY}",
        "Content-Type": "application/json"
    }
    TASK_ID = None

    def create_task(self):

        payload = {
            "agentProfile": "manus-1.5-lite",
            "prompt": "Create an Instagram caption for a fitness brand",
        }

        response = requests.post(
            self.TASK_URL, json=payload, headers=self.HEADERS)
        print(response.json())
        self.TASK_ID = response.json()["task_id"]
        return

    def get_completed_task(self, task_id):
        if task_id:
            self.TASK_ID = task_id
        if self.TASK_ID is None:
            self.create_task()
        response = requests.get(
            self.TASK_URL + f'/{self.TASK_ID}', headers=self.HEADERS)
        response.raise_for_status()
        task_data = response.json()
        status = task_data.get("status")

        if status != "completed":
            return {"status": status}
        text = None
        for msg in task_data.get("output", []):
            if msg.get("role") == "assistant" and msg.get("content"):
                for item in msg["content"]:
                    if item.get("type") == "output_text":
                        text = item["text"]
        print(text)
        return


ManusAi().get_completed_task("5V5b6tWacjhqkgKzTXU5Pa")
