from discord_webhook import DiscordWebhook, DiscordEmbed
import json
from reddit import get_reddit
import os

discordUrl = os.getenv('DISCORD_URL')


webhook = DiscordWebhook(
    url=discordUrl,
    username='Rick\'s Stream Deck',
    avatar_url='https://avatars.githubusercontent.com/u/1243170?s=280&v=4'
)

def lambda_handler(event, context):
    subreddit = 'cats'
    if 'body' in event:
        subreddit = event['body'].split(' ')[0]
    title, url = get_reddit(subreddit, count=1)
    attempts = 0
    while 'gallery' in url and attempts < 10:
        attempts += 1
        title, url = get_reddit('cats', count=1)
    #else:
        #return {'statusCode': 404}

    print(title, url)
    embed = DiscordEmbed(
        title=subreddit,
        description=title,
        color="03b2f8")
    embed.set_image(url=url)
    webhook.add_embed(embed)
    webhook.execute()

    return {
        "statusCode": 200,
    }
    
if __name__ == "__main__":
     lambda_handler({}, {})
