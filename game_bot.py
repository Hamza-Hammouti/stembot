import discord
from discord.ext import commands

# Initialize the bot
intents = discord.Intents.all()
intents.reactions = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionary to store game options and their votes
game_options = {}

@bot.event
async def on_ready():
    print(f'Ingelogd als {bot.user.name}')

@bot.command()
async def create_poll(ctx, *games):
    """Create a poll for game options in a single message."""
    if games:
        game_options[ctx.guild.id] = list(games)

        # Create the poll message with game options
        poll_message = "Stem voor het spel dat je wilt spelen:\n"
        for index, game in enumerate(games, 1):
            poll_message += f"{index}. {game}\n"

        # Send the poll message and add reactions
        poll = await ctx.send(poll_message)
        for emoji in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣'][:len(games)]:
            await poll.add_reaction(emoji)
    else:
        await ctx.send("Kies minstens 1 optie.")

@bot.event
async def on_reaction_add(reaction, user):
    """Handle user reactions to the game poll."""
    if user.bot:
        return

    guild_id = reaction.message.guild.id
    if guild_id in game_options:
        game_list = game_options[guild_id]
        emoji_to_index = {
            '1️⃣': 0,
            '2️⃣': 1,
            '3️⃣': 2,
            '4️⃣': 3,
            '5️⃣': 4,
        }

        if reaction.emoji in emoji_to_index:
            index = emoji_to_index[reaction.emoji]
            if 0 <= index < len(game_list):
                chosen_game = game_list[index]
                await reaction.message.channel.send(f"{user.mention} heeft gestemd voor {chosen_game}.")

                # Remove the user's previous reactions
                for emoji, i in emoji_to_index.items():
                    if emoji != reaction.emoji and i < len(game_list):
                        await reaction.message.remove_reaction(emoji, user)


# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run('YOUR_BOT_TOKEN')
