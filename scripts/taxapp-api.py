import asyncio
import httpx
import json
import typer
import uuid
import time
import os
from datetime import datetime

from constants import user_requests

app = typer.Typer()

async def make_request(client, url, data):
    response = await client.post(url, json=data)
    return data, response.json()

def save_to_file(request_response_pair):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output_folder = f"taxapp-api-outputs/{timestamp}"
    os.makedirs(output_folder, exist_ok=True)
    unique = str(uuid.uuid4())
    filename = f"{unique[:8]}.txt"
    filepath = os.path.join(output_folder, filename)
    with open(filepath, 'w') as file:
        content = {
            "request": request_response_pair[0],
            "response": request_response_pair[1]
        }
        file.write(json.dumps(content, indent=4))

async def main(url, num_requests):
    async with httpx.AsyncClient(timeout=60) as client:
        tasks = []
        for i in range(num_requests):
            for user_request in user_requests:  # Making specified number of requests
                data = user_request
                task = await make_request(client, url, data)
                tasks.append(task)
        for task in tasks:
            save_to_file(task)

@app.command()
def run_requests(url: str, num_requests: int):
    start_datetime = datetime.now()
    print("Start datetime:", start_datetime)
    start_time = time.time()
    asyncio.run(main(url, num_requests))
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")

@app.command()
def placeholder(name: str):
    pass

if __name__ == "__main__":
    app()
