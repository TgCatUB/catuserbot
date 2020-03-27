import os
import time
import zipfile
from datetime import datetime
from PyPDF2 import PdfFileWriter, PdfFileReader

from pySmartDL import SmartDL
from telethon import events
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeVideo
from telethon.tl.types import DocumentAttributeFilename
from userbot.utils import admin_cmd, humanbytes, progress, time_formatter

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from userbot.uniborgConfig import Config


@borg.on(admin_cmd(pattern="watermark"))
async def _(event):
    if event.fwd_from:
        return
    mone = await event.edit("Processing ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if not os.path.isdir("./cat/watermark/"):
        os.makedirs("./cat/watermark/")
    if event.reply_to_msg_id:
        start = datetime.now()
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await borg.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                )
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
        else:
            end = datetime.now()
            ms = (end - start).seconds
            await mone.edit("Stored the pdf to `{}` in {} seconds.".format(downloaded_file_name, ms))
            watermark(
                inputpdf=downloaded_file_name,
                outputpdf='./cat/watermark/' + reply_message.file.name,
                watermarkpdf='./bin/watermark.pdf'
            )
        # filename = sorted(get_lst_of_files('./cat/watermark/' + reply_message.file.name, []))
        #filename = filename + "/"
        await event.edit("Uploading now")
        caption_rts = os.path.basename(watermark_path + reply_message.file.name)
        await borg.send_file(
            event.chat_id,
            watermark_path + reply_message.file.name,
            reply_to=event.message.id,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "trying to upload")
            )
        )

def watermark(inputpdf, outputpdf, watermarkpdf):
    watermark = PdfFileReader(watermarkpdf)
    watermarkpage = watermark.getPage(0)
    pdf = PdfFileReader(inputpdf)
    pdfwrite = PdfFileWriter()
    for page in range(pdf.getNumPages()):
        pdfpage = pdf.getPage(page)
        pdfpage.mergePage(watermarkpage)
        pdfwrite.addPage(pdfpage)
    with open(outputpdf, 'wb') as fh:
        pdfwrite.write(fh)

def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        output_lst.append(current_file_name)
    return output_lst
