import asyncio
import httpx
import json
import typer
import uuid
import time
import os

app = typer.Typer()

user_id = "b688727c-790f-4992-8"
conversation_id = "b70b8eb7-ab96-4bd8-a"
role = "user"
# content = ("My client is single, currently employed by Company A as well as consulting "
#            "contract for Company C. Bought X amount of stocks at Company D at price Y and "
#            "sold such Company C stock the same year for Z price. X dollars where collected "
#            "through saving accounts interest. Company stock F distributed X dollars in dividends. "
#            "Client is shareholder of a s-corporation and c-corporation that had a net income and "
#            "distributed dividends. Client owns a few properties that are currently rented through "
#            "a property manager. Some of the propertities had an amortization and depreciation. "
#            "One of the properties is under a mortgage with around 5% interest rate. Earlier this "
#            "year one of the properties suffered damages from a natural disaster and had to do repairs, "
#            "purchase new furnitures and appliances. What forms and urls of those forms do i need to "
#            "file for my client?")
content = "who are you?"

request_data = {
    "user_id": user_id,
    "conversation_id": conversation_id,
    "content": content,
    "role": role
}
output_folder = "taxapp-api-outputs"

os.makedirs(output_folder, exist_ok=True)

async def make_request(client, url, data):
    response = await client.post(url, json=request_data)
    return data, response.json()

def save_to_file(request_response_pair):
    print('request_response_pair', request_response_pair)
    filename = f"{uuid.uuid4()}.txt"
    filepath = os.path.join(output_folder, filename)
    with open(filepath, 'w') as file:
        # content = {
        #     "request": request_response_pair[0],
        #     "response": request_response_pair[1]
        # }
        content = request_response_pair
        file.write(json.dumps(content, indent=4))

@app.command()
def run_requests(url: str, num_requests: int):
    start_time = time.time()
    asyncio.run(main(url, num_requests))
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")


async def main(url, num_requests):
    async with httpx.AsyncClient(timeout=60) as client:
        tasks = []
        for i in range(num_requests):  # Making specified number of requests
            data = request_data
            task = await make_request(client, url, data)
            tasks.append(task)
        print('\n')
        print('len(tasks)', len(tasks))
        print('\n')
        # print('tasks', tasks)
        for task in tasks:
            save_to_file(task)
        # request_response_pairs = await asyncio.gather(*tasks)
        # print('request_response_pairs', request_response_pairs)

        # for pair in request_response_pairs:
        #     await save_to_file(pair)

@app.command()
def hello(name: str, num_requests: int):
    print(f"Hello {name}")

@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")

if __name__ == "__main__":
    app()
