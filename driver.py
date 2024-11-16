import discord
from discord.ext import commands

import os
import dotenv

import manage_db as db
import profile_commands
import reserv_commands

# listen on a port for render lmao
import socket
import asyncio

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to an address and port
server_address = ('localhost', 10000)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

print('Server listening on {}:{}'.format(*server_address))

def get_token():
    dotenv.load_dotenv()
    return os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f' {bot.user} has logged on !')

    await bot.load_extension('profile_commands')
    await bot.load_extension('reserv_commands')

    await bot.tree.sync()

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Connection from {addr}")
    
    # Example: Echo server logic
    while True:
        data = await reader.read(100)
        if not data:
            break
        message = data.decode()
        print(f"Received: {message}")
        writer.write(data)
        await writer.drain()

    print(f"Connection closed from {addr}")
    writer.close()
    await writer.wait_closed()

# Function to start the server
async def start_server():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 8000)
    addr = server.sockets[0].getsockname()
    print(f"Listening on {addr}")

    async with server:
        await server.serve_forever()

async def main():
    bot_task = bot.start(get_token())
    server_task = start_server()

    # Run both tasks concurrently
    await asyncio.gather(bot_task, server_task)

if __name__ == "__main__":
    asyncio.run(main())
    db.close_connection()