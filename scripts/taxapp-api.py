import asyncio
import httpx
import json
import typer
import uuid

app = typer.Typer()

user_id = "58d222e1-89b9-4eec-9"
conversation_id = "bb646e04-23c4-45ae-b"
role = "user"
content = ("My client is single, currently employed by Company A as well as consulting "
           "contract for Company C. Bought X amount of stocks at Company D at price Y and "
           "sold such Company C stock the same year for Z price. X dollars where collected "
           "through saving accounts interest. Company stock F distributed X dollars in dividends. "
           "Client is shareholder of a s-corporation and c-corporation that had a net income and "
           "distributed dividends. Client owns a few properties that are currently rented through "
           "a property manager. Some of the propertities had an amortization and depreciation. "
           "One of the properties is under a mortgage with around 5% interest rate. Earlier this "
           "year one of the properties suffered damages from a natural disaster and had to do repairs, "
           "purchase new furnitures and appliances. What forms and urls of those forms do i need to "
           "file for my client?")

request_data = {
    "user_id": user_id,
    "conversation_id": conversation_id,
    "content": content,
    "role": role
}

async def make_request(client, url, data):
    response = await client.post(url, json=request_data)
    return data, response.json()

async def save_to_file(request_response_pair):
    print('request_response_pair', request_response_pair)
    filename = f"{uuid.uuid4()}.txt"
    with open(filename, 'w') as file:
        content = {
            "request": request_response_pair[0],
            "response": request_response_pair[1]
        }
        file.write(json.dumps(content, indent=4))

@app.command()
def run_requests(url: str, num_requests: int):
    asyncio.run(main(url, num_requests))

async def main(url, num_requests):
    async with httpx.AsyncClient() as client:
        tasks = []
        for i in range(num_requests):  # Making specified number of requests
            data = request_data
            task = make_request(client, url, data)
            tasks.append(task)

        request_response_pairs = await asyncio.gather(*tasks)

        for pair in request_response_pairs:
            await save_to_file(pair)

if __name__ == "__main__":
    app()
