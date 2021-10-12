import logging

from aiogram import Bot, Dispatcher, executor, filters, types
from aiogram.types import ParseMode
from aiogram.utils.emoji import emojize

import config
from downlaoder import download_tweet

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(filters.Regexp(regexp=r'twitter.com\/.*\/status\/([0-9]*)'))
async def send_download_link(message: types.Message, regexp):
    """
    This handler will be called when user sends any text message
    """
    tweet_id = regexp.group(1)
    download_response = download_tweet(tweet_id)
    if download_response == "Not Found":
        await message.reply("Tweet Not Found")
    else:
        tweet_text = download_response['text']
        tweet_author_username = download_response['tweet_author_username']
        tweet_author_name = download_response['tweet_author_name']
        tweet_date = download_response['tweet_date']
        media_status = download_response['media']

        if media_status is True:
            media_urls = download_response['urls']
            if len(media_urls) != 1:
                media_group = types.MediaGroup()
                count = 0
                for item in media_urls:
                    if count == 0:
                        media_group.attach_photo(
                            photo=item['url'],
                            caption=emojize(
                                f'{tweet_text}\n\n\n:alarm_clock: {tweet_date}\n\n:link: [{tweet_author_name} '\
                                f'(@{tweet_author_username})](https://twitter.com/{tweet_author_username})'\
                                '\n\n:robot: @TwitterMediaDownloaderBot'
                            ),
                            parse_mode=ParseMode.MARKDOWN,
                        )
                    else:
                        media_group.attach_photo(
                            photo=item['url']
                        )
                    count += 1
                await message.reply_media_group(media_group, )
            else:
                media_url = download_response['urls'][0]
                media_type = media_url['type']
                if media_type == 'photo':
                    await message.reply_photo(
                        photo=media_url['url'],
                        caption=emojize(
                            f'{tweet_text}\n\n\n:alarm_clock: {tweet_date}\n\n:link: [{tweet_author_name} '\
                            f'(@{tweet_author_username})](https://twitter.com/{tweet_author_username})'\
                            '\n\n:robot: @TwitterMediaDownloaderBot'
                        ),
                        parse_mode=ParseMode.MARKDOWN,
                    )
                elif media_type == 'animated_gif':
                    await message.reply_animation(
                        animation=media_url['url'],
                        caption=emojize(
                            f'{tweet_text}\n\n\n:alarm_clock: {tweet_date}\n\n:link: [{tweet_author_name} '\
                            f'(@{tweet_author_username})](https://twitter.com/{tweet_author_username})'\
                            '\n\n:robot: @TwitterMediaDownloaderBot'
                        ),
                        parse_mode=ParseMode.MARKDOWN,
                    )
        else:
            await message.reply(
                # https://www.webfx.com/tools/emoji-cheat-sheet/#
                emojize(f'{tweet_text}\n\n\n:alarm_clock: {tweet_date}\n\n:link: [{tweet_author_name} '\
                        f'(@{tweet_author_username})](https://twitter.com/{tweet_author_username})'\
                        '\n\n:robot: @TwitterMediaDownloaderBot'),
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


"""
elif media_type == 'video':
    await message.reply_video(
        video=media_url['url'],
        caption=emojize(
            f'{tweet_text}\n\n\n:alarm_clock: {tweet_date}\n\n:link: [{tweet_author_name} '\
            f'(@{tweet_author_username})](https://twitter.com/{tweet_author_username})'\
            '\n\n:robot: @TwitterMediaDownloaderBot'
        ),
        parse_mode=ParseMode.MARKDOWN,
    )
"""
