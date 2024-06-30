import os
from telethon import events
from config import settings
from rate_limiter import rate_limited
from malware_scanner import check_for_malware

def register_handlers(client):
    @client.on(events.NewMessage(pattern='/download'))
    @rate_limited(settings.rate_limit)
    async def download_latest_file(event):
        try:
            if event.is_group:
                chat = await event.get_chat()
                messages = await client.get_messages(chat, limit=1)
                if messages:
                    message = messages[0]
                    if message.media and message.document.mime_type in ['application/pdf', 'application/epub+zip']:
                        # Download the document
                        file_path = await client.download_media(message, settings.download_path)
                        print(f'Downloaded: {file_path}')
                        
                        # Check for malware
                        if check_for_malware(file_path):
                            os.remove(file_path)
                            print(f'Malware detected and file deleted: {file_path}')
                        else:
                            print(f'File is clean: {file_path}')
                else:
                    await event.reply("No files found in the latest message.")
        except Exception as e:
            await event.reply(f"Error occurred: {e}")
            print(f"Error in download_latest_file: {e}")

    @client.on(events.NewMessage(pattern='/listfiles'))
    async def list_files(event):
        try:
            files = os.listdir(settings.download_path)
            if files:
                file_list = "\n".join(files)
                await event.reply(f"Downloaded files:\n{file_list}")
            else:
                await event.reply("No files found in the download directory.")
        except Exception as e:
            await event.reply(f"Error occurred: {e}")
            print(f"Error in list_files: {e}")

    @client.on(events.NewMessage(pattern='/checkfile'))
    async def check_file(event):
        try:
            file_name = event.message.text.split(' ', 1)[1]
            file_path = os.path.join(settings.download_path, file_name)
            if os.path.exists(file_path):
                if check_for_malware(file_path):
                    os.remove(file_path)
                    await event.reply(f'Malware detected and file deleted: {file_path}')
                else:
                    await event.reply(f'File is clean: {file_path}')
            else:
                await event.reply(f'File not found: {file_path}')
        except Exception as e:
            await event.reply(f"Error occurred: {e}")
            print(f"Error in check_file: {e}")

    print("Handlers registered.")
