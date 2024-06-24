import discord
from discord.ui import Button, View
from discord.ext import commands
from discord.utils import get
import random
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)


dashes = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']
odds = ['\u2680', '\u2682', '\u2684']
evens = ['\u2681', '\u2683', '\u2685']
colors = ['Yellow', 'Red', 'Green', 'Blue', 'Purple']
creatures = ['Wolf', 'Bear', 'Eagle', 'Frog', 'Elephant']
suits = ['of Hearts', 'of Diamonds', 'of Clubs', 'of Spades']
users = {}
old_users = []
values = {
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    'Jack': 10,
    'Queen': 10,
    'King': 10,
    'Ace': 11
}
numbers = [2, 3, 4, 6, 7, 8, 9, 10]
cool_guys = ['Jack', 'Queen', 'King', 'Ace']
sequence = [0, 1]
phrases_lose = ['К сожалению, вы проиграли.', 'Вы проиграли. Повезёт в следующий раз', 'Какая досада. Вы проиграли',
                'Удача сегодня на моей стороне.', 'Надеюсь, вы готовы расстаться со своей ставкой.',
                'Возможно, сегодня не ваш день.', 'В результате ужаснейшего невезения вы проиграли.']
phrases_win = ['Удача улыбается вам. Вы выиграли.', 'На этот раз вы выиграли.', 'Сегодня ваш день!',
               'Фортуна не на моей стороне.', 'Надеюсь, мне повезёт в следующий раз.',
               'Эта партия за вами.', 'Победа за вами.']


async def win(ctx, bet, doubledown):
    global users
    await ctx.send(phrases_win[random.randint(0, 6)])
    await asyncio.sleep(2)
    bet = int(bet)
    if doubledown:
        users[ctx.author][6] += bet * 2
        users[ctx.author][5] += bet * 2
        await ctx.send(f'Вы выиграли {int(bet) * 2} :coin:.')
    else:
        users[ctx.author][6] += bet
        users[ctx.author][5] += bet
        await ctx.send(f'Вы выиграли {int(bet)} :coin:.')
    users[ctx.author][1] += 1
    users[ctx.author][4] = int((users[ctx.author][1] / (users[ctx.author][2]
                                                        + users[ctx.author][3] + users[ctx.author][1])) * 100)


async def lose(ctx, bet, doubledown):
    global users
    await ctx.send(phrases_lose[random.randint(0, 6)])
    await asyncio.sleep(2)
    bet = int(bet)
    if doubledown:
        users[ctx.author][6] -= bet * 2
        users[ctx.author][5] -= bet * 2
        await ctx.send(f'Вы проиграли {int(bet) * 2} :coin:.')
    else:
        users[ctx.author][6] -= bet
        users[ctx.author][5] -= bet
        await ctx.send(f'Вы проиграли {int(bet)} :coin:.')
    users[ctx.author][2] += 1
    users[ctx.author][4] = int((users[ctx.author][1] / (users[ctx.author][2]
                                                        + users[ctx.author][3] + users[ctx.author][1])) * 100)


@bot.command()
async def dice(ctx):
    if ctx.author not in old_users:
        users[ctx.author] = [0, 0, 0, 0, 0, 0, 100]  # 1 - число матчей,2 - победы,
        # 3 - поражения,4 - ничьи, 5 - вр, 6 - итог, 7 - баланс
        old_users.append(ctx.author)
    await ctx.send('Сделайте ставку от 1 до 5 :coin:.')

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and \
               msg.content.lower() in ["1", "2", "3", "4", "5"]

    msg = await bot.wait_for("message", check=check)
    bet = msg.content
    await ctx.send(f"Ваша ставка принята.")
    button_odd = Button(label='Odd', style=discord.ButtonStyle.green, custom_id='button_odd')
    button_even = Button(label='Even', style=discord.ButtonStyle.red, custom_id='button_even')
    view = View()
    view.add_item(button_odd)
    view.add_item(button_even)
    await ctx.send('На что ставите?', view=view)

    async def button_odd_callback(interaction):
        result = random.choice(dashes)
        player_chose = 'Odd'
        await interaction.response.send_message('Бросок кубика')
        await asyncio.sleep(2)
        await ctx.send(result)
        if (result in odds and player_chose == 'Odd') or (result in evens and player_chose == 'Even'):
            await win(ctx, bet, False)
        else:
            await lose(ctx, bet, False)

    button_odd.callback = button_odd_callback

    async def button_even_callback(interaction):
        result = random.choice(dashes)
        player_chose = 'Even'
        await interaction.response.send_message('Бросок кубика')
        await asyncio.sleep(2)
        await ctx.send(result)
        if (result in odds and player_chose == 'Odd') or (result in evens and player_chose == 'Even'):
            await win(ctx, bet, False)
        else:
            await lose(ctx, bet, False)

    button_even.callback = button_even_callback


@bot.command()
async def blackjack(ctx):
    turn_was = False
    if ctx.author not in old_users:
        users[ctx.author] = [0, 0, 0, 0, 0, 0, 100]  # 1 - число матчей,2 - победы,
        # 3 - поражения,4 - ничьи, 5 - вр, 6 - итог, 7 - баланс
        old_users.append(ctx.author)
    await ctx.send('Сделайте ставку от 1 до 10 :coin:.')

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and \
               msg.content.lower() in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

    msg = await bot.wait_for("message", check=check)
    bet = msg.content
    await ctx.send(f"Ваша ставка принята.", delete_after=2)
    await asyncio.sleep(2)
    await ctx.send('Первый ход начинается', delete_after=2)
    await asyncio.sleep(3)

    number_player = random.choice(sequence)
    player_suit_1 = suits[random.randint(0, 3)]
    if number_player == 0:
        player_value_1 = values[random.choice(numbers)]
    else:
        player_value_1 = cool_guys[random.randint(0, 3)]

    number_player_2 = random.choice(sequence)
    player_suit_2 = suits[random.randint(0, 3)]
    if number_player_2 == 0:
        player_value_2 = values[random.choice(numbers)]
    else:
        player_value_2 = cool_guys[random.randint(0, 3)]

    await ctx.send(f"Ваша рука: {player_value_1} {player_suit_1}, {player_value_2} {player_suit_2}")

    number_dealer = random.choice(sequence)
    dealer_suit_1 = suits[random.randint(0, 3)]
    if number_dealer == 0:
        dealer_value_1 = values[random.choice(numbers)]
    else:
        dealer_value_1 = cool_guys[random.randint(0, 3)]

    number_dealer_2 = random.choice(sequence)
    dealer_suit_2 = suits[random.randint(0, 3)]
    if number_dealer_2 == 0:
        dealer_value_2 = values[random.choice(numbers)]
    else:
        dealer_value_2 = cool_guys[random.randint(0, 3)]

    await ctx.send(f"Мои карты: {dealer_value_1} {dealer_suit_1}, ???")
    await asyncio.sleep(2)
    button_stay = Button(label='Stay', style=discord.ButtonStyle.green, custom_id='button_stay')
    button_hit = Button(label='Hit', style=discord.ButtonStyle.blurple, custom_id='button_hit')
    button_dd = Button(label='Double Down', style=discord.ButtonStyle.red, custom_id='button_dd')
    button_sur = Button(label='Surrender', style=discord.ButtonStyle.secondary, custom_id='button_sur')
    view = View()
    view.add_item(button_stay)
    view.add_item(button_hit)
    view.add_item(button_dd)
    view.add_item(button_sur)
    await ctx.send('Ваш ход', view=view)

    async def button_stay_callback(interaction):
        button_dd.disabled = True
        button_stay.disabled = True
        button_hit.disabled = True
        button_sur.disabled = True
        await interaction.response.edit_message(view=view)
        await asyncio.sleep(1)
        dealer_total = values[dealer_value_1] + values[dealer_value_2]
        player_total = values[player_value_1] + values[player_value_2]
        if player_total < 16 or player_total > 21:
            await ctx.send('Вы решили не брать карту,'
                           ' когда у вас меньше 16 очков. Не лучший ход....')
            await lose(ctx, bet, False)
        else:
            if dealer_total < 16:
                await ctx.send('Кажется у меня меньше, чем 16 очков.Я доберу ещё одну карту.')
                number_dealer_3 = random.choice(sequence)
                dealer_suit_3 = suits[random.randint(0, 3)]
                if number_dealer_3 == 0:
                    dealer_value_3 = values[random.choice(numbers)]
                else:
                    dealer_value_3 = cool_guys[random.randint(0, 3)]
                await ctx.send(f"Мои карты: {dealer_value_1} {dealer_suit_1},"
                               f" {dealer_value_2} {dealer_suit_2}, {dealer_value_3} {dealer_suit_3}")
            else:
                await ctx.send(f"Мои карты: {dealer_value_1} {dealer_suit_1},"
                               f" {dealer_value_2} {dealer_suit_2}")

            if dealer_total < 16 or dealer_total > 21:
                await win(ctx, bet, False)

            elif dealer_total > player_total:
                await lose(ctx, bet, False)

            elif player_total > dealer_total:
                await win(ctx, bet, False)

            elif player_total == dealer_total:
                await ctx.send('Ничья!')
                users[ctx.author][3] += 1
                await asyncio.sleep(2)
                await ctx.send('Вы при своих.')
                users[ctx.author][4] = int((users[ctx.author][1] / (users[ctx.author][2]
                                                                    + users[ctx.author][3] + users[ctx.author][
                                                                        1])) * 100)

    button_stay.callback = button_stay_callback

    async def button_surrender_callback(interaction):
        button_dd.disabled = True
        button_stay.disabled = True
        button_hit.disabled = True
        button_sur.disabled = True
        await interaction.response.edit_message(view=view)
        await asyncio.sleep(2)
        await ctx.send('Вы решили сдаться? Я бы не стал так поступать, но дело ваше.')
        users[ctx.author][2] += 1
        users[ctx.author][6] -= int(bet)
        await asyncio.sleep(2)
        await ctx.send(f'Вы проиграли {int(bet)} :coin:.')
        await ctx.send(f'Теперь ваш баланс составляет {users[ctx.author][6]} :coin:')

    button_sur.callback = button_surrender_callback

    async def button_doubledown_callback(interaction):
        await ctx.send(f'Ставка удваивается до {int(bet) * 2} :coin:!')
        button_dd.disabled = True
        button_stay.disabled = True
        button_hit.disabled = True
        button_sur.disabled = True
        await interaction.response.edit_message(view=view)

        player_total = values[player_value_1] + values[player_value_2]
        dealer_total = values[dealer_value_1] + values[dealer_value_2]

        if dealer_total < 16:
            await ctx.send('Кажется у меня меньше, чем 16 очков.Я доберу ещё одну.')
            number_dealer_3 = random.choice(sequence)
            dealer_suit_3 = suits[random.randint(0, 3)]
            if number_dealer_3 == 0:
                dealer_value_3 = values[random.choice(numbers)]
            else:
                dealer_value_3 = cool_guys[random.randint(0, 3)]
            await asyncio.sleep(2)
            await ctx.send(f"Мои карты: {dealer_value_1} {dealer_suit_1},"
                           f" {dealer_value_2} {dealer_suit_2}, {dealer_value_3} {dealer_suit_3}")
            dealer_total = values[dealer_value_1] + values[dealer_value_2] + values[dealer_value_3]

        else:
            await ctx.send(f"Мои карты: {dealer_value_1} {dealer_suit_1},"
                           f" {dealer_value_2} {dealer_suit_2}")

        number_player_3 = random.choice(sequence)
        player_suit_3 = suits[random.randint(0, 3)]
        if number_player_3 == 0:
            player_value_3 = values[random.choice(numbers)]
        else:
            player_value_3 = cool_guys[random.randint(0, 3)]
        await asyncio.sleep(2)
        await ctx.send(f"Ваша рука: {player_value_1} {player_suit_1},"
                       f" {player_value_2} {player_suit_2}, {player_value_3} {player_suit_3}")

        player_total = values[player_value_1] + values[player_value_2] + values[player_value_3]

        if player_total < 16 or player_total > 21:
            await lose(ctx, bet, True)

        elif dealer_total < 16 or dealer_total > 21:
            await win(ctx, bet, True)

        elif dealer_total > player_total:
            await lose(ctx, bet, True)

        elif player_total > dealer_total:
            await win(ctx, bet, True)

        elif player_total == dealer_total:
            await ctx.send('Ничья!')
            await asyncio.sleep(2)
            users[ctx.author][3] += 1
            await ctx.send('Вы при своих.')
            users[ctx.author][4] = int((users[ctx.author][1] / (users[ctx.author][2]
                                                                + users[ctx.author][3] + users[ctx.author][1])) * 100)

    button_dd.callback = button_doubledown_callback

    async def button_hit_callback(interaction):
        await asyncio.sleep(1)
        button_dd.disabled = True
        button_stay.disabled = True
        button_hit.disabled = True
        button_sur.disabled = True
        await interaction.response.edit_message(view=view)
        dealer_total = values[dealer_value_1] + values[dealer_value_2]
        player_total = values[player_value_1] + values[player_value_2]
        if dealer_total < 16:
            await ctx.send('Кажется у меня меньше, чем 16 очков.Я доберу ещё одну.')
            number_dealer_3 = random.choice(sequence)
            dealer_suit_3 = suits[random.randint(0, 3)]
            if number_dealer_3 == 0:
                dealer_value_3 = values[random.choice(numbers)]
            else:
                dealer_value_3 = cool_guys[random.randint(0, 3)]
            await ctx.send(f"Мои карты: {dealer_value_1} {dealer_suit_1},"
                           f" {dealer_value_2} {dealer_suit_2}, {dealer_value_3} {dealer_suit_3}")
            dealer_total = values[dealer_value_1] + values[dealer_value_2] + values[dealer_value_3]

        else:
            await ctx.send(f"Мои карты: {dealer_value_1} {dealer_suit_1},"
                           f" {dealer_value_2} {dealer_suit_2}")

        number_player_3 = random.choice(sequence)
        player_suit_3 = suits[random.randint(0, 3)]
        if number_player_3 == 0:
            player_value_3 = values[random.choice(numbers)]
        else:
            player_value_3 = cool_guys[random.randint(0, 3)]
        await asyncio.sleep(2)
        await ctx.send(f"Ваша рука: {player_value_1} {player_suit_1},"
                       f" {player_value_2} {player_suit_2}, {player_value_3} {player_suit_3}")

        player_total = values[player_value_1] + values[player_value_2] + values[player_value_3]

        if player_total < 16 or player_total > 21:
            await lose(ctx, bet, False)

        elif dealer_total < 16 or dealer_total > 21:
            await win(ctx, bet, False)

        elif dealer_total > player_total:
            await lose(ctx, bet, False)

        elif player_total > dealer_total:
            await win(ctx, bet, False)

        elif player_total == dealer_total:
            await ctx.send('Ничья!')
            users[ctx.author][4] = int((users[ctx.author][1] / (users[ctx.author][2]
                                                                + users[ctx.author][3] + users[ctx.author][1])) * 100)
            users[ctx.author][3] += 1
            await asyncio.sleep(2)
            await ctx.send('Вы при своих.')

    button_hit.callback = button_hit_callback


@bot.command()
async def menu(ctx):
    if ctx.author not in old_users:
        users[ctx.author] = [0, 0, 0, 0, 0, 0, 100]  # 1 - число матчей,2 - победы,
        # 3 - поражения,4 - ничьи, 5 - винрейт, 6 - итог, 7 - баланс
        old_users.append(ctx.author)
    await ctx.send('/blackjack :diamonds:- блекджек \n'
                   '/dice :game_die: - бросок шестигранного кубика \n'
                   '/rem :brain: - игра на память \n'
                   '/tictactoe ❌ - крестики-нолики \n'
                   '/math :1234: - простые числовые задания \n'
                   '\n/rules :newspaper: - информация о правилах мини-игр \n'
                   '/shop :money_with_wings: - магазин \n'
                   '/balance :purse: - посмотреть баланс \n'
                   '/visual :star2: - настройка визуала \n'
                   '\n/stat :scroll: - статистика сыгранных игр \n'
                   '/menu :book: - список всех команд \n'
                   '/helpme - техподдержка')


@bot.command()
async def helpme(ctx):
    if ctx.author not in old_users:
        users[ctx.author] = [0, 0, 0, 0, 0, 0, 100]  # 1 - число матчей,2 - победы,
        # 3 - поражения,4 - ничьи, 5 - вр, 6 - итог, 7 - баланс
    button_faq = Button(label='FAQ', style=discord.ButtonStyle.url, url='https://drive.google.com/file/d/1I9CoR9g-1nSESwxxbLJa-9SXDJ3ZM8Tf/view?usp=sharing')
    view = View()
    view.add_item(button_faq)
    await ctx.send('Нажмите на кнопку, чтобы открыть файл поддержки', view=view)

@bot.command()
async def balance(ctx):
    if ctx.author not in old_users:
        users[ctx.author] = [0, 0, 0, 0, 0, 0, 100]  # 1 - число матчей,2 - победы,
        # 3 - поражения,4 - ничьи, 5 - вр, 6 - итог, 7 - баланс
        old_users.append(ctx.author)
    await ctx.send(f'Ваш баланс составляет {users[ctx.author][6]} :coin:')


@bot.command()
async def visual(ctx):
    if ctx.author not in old_users:
        users[ctx.author] = [0, 0, 0, 0, 0, 0, 100]  # 1 - число матчей,2 - победы,
        # 3 - поражения,4 - ничьи, 5 - вр, 6 - итог, 7 - баланс
        old_users.append(ctx.author)
    button_suits = Button(label='Карты', style=discord.ButtonStyle.secondary, custom_id='button_suits')
    button_dice = Button(label='Кубик', style=discord.ButtonStyle.secondary, custom_id='button_dice')
    button_guess = Button(label='Слова', style=discord.ButtonStyle.secondary, custom_id='button_guess')
    button_example = Button(label='Пример', style=discord.ButtonStyle.red, custom_id='button_example')
    view = View()
    view.add_item(button_suits)
    view.add_item(button_dice)
    view.add_item(button_guess)
    view.add_item(button_example)
    await ctx.send('Выберите что вы хотели бы изменить', view=view)

    async def button_example_callback(interaction):
        await interaction.response.send_message(f'Ace {suits[0]}, King {suits[1]},'
                                                f' Queen {suits[2]}, Jack {suits[3]}')
        await ctx.send(f'1 - {dashes[0]}, 2 - {dashes[1]}, 3 - {dashes[2]}')
        await ctx.send(f'{colors[0]} {creatures[0]}, {colors[1]} {creatures[1]}, {colors[2]} {creatures[2]}')

    button_example.callback = button_example_callback

    async def button_suits_callback(interaction):
        global suits
        if button_suits.style == discord.ButtonStyle.green:
            button_suits.style = discord.ButtonStyle.secondary
        else:
            button_suits.style = discord.ButtonStyle.green
        await interaction.response.edit_message(view=view)
        if suits == ['of Hearts', 'of Diamonds', 'of Clubs', 'of Spades']:
            suits = [':hearts:', ':diamonds:', ':clubs:', ':spades:']
        else:
            suits = ['of Hearts', 'of Diamonds', 'of Clubs', 'of Spades']

    button_suits.callback = button_suits_callback

    async def button_dice_callback(interaction):
        global dashes, odds, evens
        if button_dice.style == discord.ButtonStyle.green:
            button_dice.style = discord.ButtonStyle.secondary
        else:
            button_dice.style = discord.ButtonStyle.green
        await interaction.response.edit_message(view=view)
        if dashes == ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']:
            dashes = [':game_die: :one:', ':game_die: :two:', ':game_die: :three:',
                      ':game_die: :four:', ':game_die: :five:', ':game_die: :six:']
            odds = [':game_die: :one:', ':game_die: :three:', ':game_die: :five:']
            evens = [':game_die: :two:', ':game_die: :four:', ':game_die: :six:']
        else:
            dashes = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']
            odds = ['\u2680', '\u2682', '\u2684']
            evens = ['\u2681', '\u2683', '\u2685']

    button_dice.callback = button_dice_callback

    async def button_guess_callback(interaction):
        global colors, creatures
        if button_guess.style == discord.ButtonStyle.green:
            button_guess.style = discord.ButtonStyle.secondary
        else:
            button_guess.style = discord.ButtonStyle.green
        await interaction.response.edit_message(view=view)
        if colors == ['Yellow', 'Red', 'Green', 'Blue', 'Purple'] and \
                creatures == ['Wolf', 'Bear', 'Eagle', 'Frog', 'Elephant']:
            colors = ['🟡', '🔴', '🟢', '🔵', '🟣']
            creatures = ['🐺', '🐻', '🦅', '🐸', '🐘']
        else:
            colors = ['Yellow', 'Red', 'Green', 'Blue', 'Purple']
            creatures = ['Wolf', 'Bear', 'Eagle', 'Frog', 'Elephant']

    button_guess.callback = button_guess_callback


@bot.command()
async def stat(ctx):
    if ctx.author not in old_users:
        users[ctx.author] = [0, 0, 0, 0, 0, 0, 100]  # 1 - число матчей,2 - победы,
        # 3 - поражения,4 - ничьи, 5 - вр, 6 - итог, 7 - баланс
        old_users.append(ctx.author)
    await asyncio.sleep(2)
    await ctx.send(f'Количество сыгранных матчей: {users[ctx.author][1] + users[ctx.author][2] + users[ctx.author][3]}')
    await ctx.send(f'Побед: {users[ctx.author][1]}, Поражений: {users[ctx.author][2]}, Ничьих: {users[ctx.author][3]}')
    await ctx.send(f'Процент побед: {users[ctx.author][4]} %')
    await ctx.send(f'Итог: {users[ctx.author][5]} :coin:')


@bot.command()
async def math(ctx):
    global users, old_users
    await asyncio.sleep(1)
    if ctx.author not in old_users:
        users[ctx.author] = [0, 0, 0, 0, 0, 0, 100]  # 1 - число матчей,2 - победы,
        # 3 - поражения,4 - ничьи, 5 - вр, 6 - итог, 7 - баланс
        old_users.append(ctx.author)
    await ctx.send('В этой мини-игре нет ставок.')
    await ctx.send('За каждый правильный ответ вы получаете 1 :coin:.')
    await ctx.send('А за каждый неверный теряете столько же.')
    number_1 = random.randint(1, 100)
    number_2 = random.randint(100, 200)
    operation = random.choice(sequence)
    if operation == 0:
        bot_exercise = await ctx.send(f'{number_1} + {number_2} = ?')
        answer = number_1 + number_2
        answer = str(answer)
    else:
        bot_exercise = await ctx.send(f'{number_2} - {number_1} = ?')
        answer = number_2 - number_1
        answer = str(answer)
    await ctx.send('5', delete_after=1)
    await asyncio.sleep(2)
    await ctx.send('4', delete_after=1)
    await asyncio.sleep(2)
    await ctx.send('3', delete_after=1)
    await asyncio.sleep(2)
    await ctx.send('2', delete_after=1)
    await asyncio.sleep(2)
    await ctx.send('1', delete_after=1)
    await asyncio.sleep(2)
    await bot_exercise.delete()
    await ctx.send('Итак, ваш ответ.')

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await bot.wait_for("message", check=check)
    player_try = msg.content
    if player_try == answer:
        await asyncio.sleep(1)
        await ctx.send(phrases_win[random.randint(0, 6)])
        users[ctx.author][5] += 1
        users[ctx.author][6] += 1
        users[ctx.author][1] += 1
        users[ctx.author][4] = int((users[ctx.author][1] / (users[ctx.author][2]
                                                            + users[ctx.author][3] + users[ctx.author][1])) * 100)
    else:
        await asyncio.sleep(1)
        await ctx.send(phrases_lose[random.randint(0, 6)])
        users[ctx.author][5] -= 1
        users[ctx.author][6] -= 1
        users[ctx.author][2] += 1
        users[ctx.author][4] = int((users[ctx.author][1] / (users[ctx.author][2]
                                                            + users[ctx.author][3] + users[ctx.author][1])) * 100)


@bot.command()
async def rules(ctx):
    if ctx.author not in old_users:
        users[ctx.author] = [0, 0, 0, 0, 0, 0, 100]  # 1 - число матчей,2 - победы,
        # 3 - поражения,4 - ничьи, 5 - вр, 6 - итог, 7 - баланс
        old_users.append(ctx.author)
    button_blackjack = Button(label='Блекджек', url='https://ru.wikipedia.org/wiki/Блэкджек')
    button_dice = Button(label='Игральный куб', url='https://ru.wikipedia.org/wiki/Игральная_кость')
    button_ttt = Button(label='Крестики-нолики', url='https://ru.wikipedia.org/wiki/Крестики-нолики')
    view = View()
    view.add_item(button_blackjack)
    view.add_item(button_dice)
    view.add_item(button_ttt)
    await ctx.send('Выберите игру о которой хотите узнать побольше', view=view)


@bot.command()
async def shop(ctx):
    global users
    if ctx.author not in old_users:
        users[ctx.author] = [0, 0, 0, 0, 0, 0, 100]  # 1 - число матчей,2 - победы,
        # 3 - поражения,4 - ничьи, 5 - вр, 6 - итог, 7 - баланс
        old_users.append(ctx.author)
    view = View()
    role_weak = 'Роль 1'
    role_not_so_weak = 'Роль 2'
    role_mediocre = 'Роль 3'
    role_strong = 'Роль 4'
    role_too_strong = 'Роль 5'
    if users[ctx.author][6] < 100:
        role_1 = Button(label=role_weak, disabled=True)
    else:
        role_1 = Button(label=role_weak)
    if users[ctx.author][6] < 400:
        role_2 = Button(label=role_not_so_weak, disabled=True)
    else:
        role_2 = Button(label=role_not_so_weak)
    if users[ctx.author][6] < 600:
        role_3 = Button(label=role_mediocre, disabled=True)
    else:
        role_3 = Button(label=role_mediocre)
    if users[ctx.author][6] < 1000:
        role_4 = Button(label=role_strong, disabled=True)
    else:
        role_4 = Button(label=role_strong)
    if users[ctx.author][6] < 3000:
        role_5 = Button(label=role_too_strong, disabled=True, style=discord.ButtonStyle.red)
    else:
        role_5 = Button(label=role_too_strong, style=discord.ButtonStyle.red)
    view.add_item(role_1)
    view.add_item(role_2)
    view.add_item(role_3)
    view.add_item(role_4)
    view.add_item(role_5)
    await ctx.send('Добро пожаловать в магазин.', view=view)
    await ctx.send('Цены:')
    await ctx.send(f'{role_weak} - 100 :coin:, {role_not_so_weak} - 400 :coin:')
    await ctx.send(f'{role_mediocre} - 600 :coin:, {role_strong} - 1000 :coin:')
    await ctx.send(f'{role_too_strong} - 3000 :coin:')

    async def role_1_callback(interaction):
        if role_1.style == discord.ButtonStyle.secondary:
            role_1.style = discord.ButtonStyle.green
            role_1.label = 'Куплено'
            role_1.disabled = True
        await interaction.response.edit_message(view=view)
        role = discord.utils.get(ctx.guild.roles, name=role_weak)
        await ctx.author.add_roles(role)
        users[ctx.author][6] -= 100

    role_1.callback = role_1_callback

    async def role_2_callback(interaction):
        if role_2.style == discord.ButtonStyle.secondary:
            role_2.style = discord.ButtonStyle.green
            role_2.label = 'Куплено'
            role_2.disabled = True
        await interaction.response.edit_message(view=view)
        role = discord.utils.get(ctx.guild.roles, name=role_not_so_weak)
        await ctx.author.add_roles(role)
        users[ctx.author][6] -= 400

    role_2.callback = role_2_callback

    async def role_3_callback(interaction):
        if role_3.style == discord.ButtonStyle.secondary:
            role_3.style = discord.ButtonStyle.green
            role_3.label = 'Куплено'
            role_3.disabled = True
        await interaction.response.edit_message(view=view)
        role = discord.utils.get(ctx.guild.roles, name=role_mediocre)
        await ctx.author.add_roles(role)
        users[ctx.author][6] -= 600

    role_3.callback = role_3_callback

    async def role_4_callback(interaction):
        if role_4.style == discord.ButtonStyle.secondary:
            role_4.style = discord.ButtonStyle.green
            role_4.label = 'Куплено'
            role_4.disabled = True
        await interaction.response.edit_message(view=view)
        role = discord.utils.get(ctx.guild.roles, name=role_strong)
        await ctx.author.add_roles(role)
        users[ctx.author][6] -= 400

    role_4.callback = role_4_callback

    async def role_5_callback(interaction):
        if role_5.style == discord.ButtonStyle.red:
            role_5.style = discord.ButtonStyle.green
            role_5.label = 'Куплено'
            role_5.disabled = True
        await interaction.response.edit_message(view=view)
        role = discord.utils.get(ctx.guild.roles, name=role_too_strong)
        await ctx.author.add_roles(role)
        users[ctx.author][6] -= 1000

    role_5.callback = role_5_callback


@bot.command()
async def rem(ctx):
    global users, old_users
    await ctx.send('Сделайте ставку от 1 до 5 :coin:.')
    if ctx.author not in old_users:
        users[ctx.author] = [0, 0, 0, 0, 0, 0, 100]  # 1 - число матчей,2 - победы,
        # 3 - поражения,4 - ничьи, 5 - вр, 6 - итог, 7 - баланс.
        old_users.append(ctx.author)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and \
               msg.content.lower() in ["1", "2", "3", "4", "5"]

    msg = await bot.wait_for("message", check=check)
    bet = msg.content
    animals = ''
    view = View()
    animal_1 = colors[random.randint(0, 4)] + ' ' + random.choice(creatures)
    animal_2 = colors[random.randint(0, 4)] + ' ' + random.choice(creatures)
    animal_3 = colors[random.randint(0, 4)] + ' ' + random.choice(creatures)
    button_an_1 = Button(label=animal_1, disabled=True, style=discord.ButtonStyle.red)
    button_an_2 = Button(label=animal_2, disabled=True, style=discord.ButtonStyle.blurple)
    button_an_3 = Button(label=animal_3, disabled=True, style=discord.ButtonStyle.green)
    view.add_item(button_an_1)
    view.add_item(button_an_2)
    view.add_item(button_an_3)
    guessing = await ctx.send(animals, view=view)
    view_2 = View()
    animal_true = Button(label=animal_1 + ', ' + animal_2 + ', ' + animal_3, style=discord.ButtonStyle.blurple)
    fake = []
    for i in range(10):
        animal = random.choice(colors) + ' ' + random.choice(creatures)
        fake.append(animal)
    animal_false_1 = Button(label=animal_2 + ', ' + random.choice(fake) + ', ' + random.choice(fake),
                            style=discord.ButtonStyle.blurple)
    animal_false_2 = Button(label=random.choice(fake) + ', ' + random.choice(fake) + ', ' + random.choice(fake),
                            style=discord.ButtonStyle.blurple)
    animal_false_3 = Button(label=random.choice(fake) + ', ' + random.choice(fake) + ', ' + random.choice(fake),
                            style=discord.ButtonStyle.blurple)
    new_n3on = [animal_false_1, animal_false_2, animal_false_3]
    sequence_2 = [0, 1, 2]
    choice = random.choice(sequence_2)
    for i in range(3):
        if choice == i:
            view_2.add_item(animal_true)
        else:
            view_2.add_item(new_n3on[i])
    await ctx.send('3', delete_after=1)
    await asyncio.sleep(1)
    await ctx.send('2', delete_after=1)
    await asyncio.sleep(1)
    await ctx.send('1', delete_after=1)
    await asyncio.sleep(1)
    await guessing.delete()
    bot_word = await ctx.send('Итак, ваш ответ', view=view_2)

    async def button_true_callback(interaction):
        view_2.clear_items()
        await interaction.response.edit_message(view=view_2)
        await win(ctx, bet, False)

    animal_true.callback = button_true_callback

    async def button_false_callback(interaction):
        view_2.clear_items()
        await interaction.response.edit_message(view=view_2)
        await lose(ctx, bet, False)

    async def button_false_2_callback(interaction):
        view_2.clear_items()
        await interaction.response.edit_message(view=view_2)
        await lose(ctx, bet, False)

    async def button_false_3_callback(interaction):
        view_2.clear_items()
        await interaction.response.edit_message(view=view_2)
        await lose(ctx, bet, False)

    animal_false_1.callback = button_false_callback
    animal_false_2.callback = button_false_2_callback
    animal_false_3.callback = button_false_3_callback


@bot.command()
async def tictactoe2(ctx):
    global users, old_users
    await ctx.send('Сделайте ставку от 1 до 10 :coin:.')
    if ctx.author not in old_users:
        users[ctx.author] = [0, 0, 0, 0, 0, 0, 100]  # 1 - число матчей,2 - победы,
        # 3 - поражения,4 - ничьи, 5 - вр, 6 - итог, 7 - баланс.
        old_users.append(ctx.author)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and \
               msg.content.lower() in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

    msg = await bot.wait_for("message", check=check)
    bet = msg.content
    view = View()
    buttons = []
    for i in range(9):
        if i < 3:
            button = Button(label=' ', style=discord.ButtonStyle.blurple, row=1)
        elif 3 <= i < 6:
            button = Button(label=' ', style=discord.ButtonStyle.blurple, row=2)
        else:
            button = Button(label=' ', style=discord.ButtonStyle.blurple, row=3)
        view.add_item(button)
        buttons.append(button)
    await ctx.send('Ваш ход', view=view)
    possible_turns = []
    situation = ['', '', '',
                 '', '', '',
                 '', '', '']

    async def bot_turn():
        available_turns = False
        player_win = False
        bot_win = False
        for i in situation:
            if i == '':
                available_turns = True
        if (situation[0] == '❌' and situation[1] == '❌' and situation[2] == '❌') or \
                (situation[3] == '❌' and situation[4] == '❌' and situation[5] == '❌') or \
                (situation[6] == '❌' and situation[7] == '❌' and situation[8] == '❌') or \
                (situation[0] == '❌' and situation[3] == '❌' and situation[6] == '❌') or \
                (situation[1] == '❌' and situation[4] == '❌' and situation[7] == '❌') or \
                (situation[2] == '❌' and situation[5] == '❌' and situation[8] == '❌') or \
                (situation[0] == '❌' and situation[4] == '❌' and situation[8] == '❌'):
            player_win = True
        if (situation[0] == '⭕' and situation[1] == '⭕' and situation[2] == '⭕') or \
                (situation[3] == '⭕' and situation[4] == '⭕' and situation[5] == '⭕') or \
                (situation[6] == '⭕' and situation[7] == '⭕' and situation[8] == '⭕') or \
                (situation[0] == '⭕' and situation[3] == '⭕' and situation[6] == '⭕') or \
                (situation[1] == '⭕' and situation[4] == '⭕' and situation[7] == '⭕') or \
                (situation[2] == '⭕' and situation[5] == '⭕' and situation[8] == '⭕') or \
                (situation[0] == '⭕' and situation[4] == '⭕' and situation[8] == '⭕'):
            bot_win = True

        if available_turns:
            dada = True
            while dada:
                turn = random.randint(0, 8)
                element = situation[turn]
                if element == '':
                    dada = False
            situation[turn] = '⭕'
            buttons[turn].disabled = True
            buttons[turn].label = '⭕'
            buttons[turn].style = discord.ButtonStyle.secondary
        if player_win:
            for i in range(9):
                buttons[i].disabled = True
            await win(ctx, bet, False)
        elif bot_win:
            for i in range(9):
                buttons[i].disabled = True
            await lose(ctx, bet, False)
        available_turns = False

    async def button_1_callback(interaction):
        situation[0] = '❌'
        buttons[0].label = '❌'
        buttons[0].style = discord.ButtonStyle.green
        buttons[0].disabled = True
        await bot_turn()
        await interaction.response.edit_message(view=view)

    buttons[0].callback = button_1_callback

    async def button_2_callback(interaction):
        situation[1] = '❌'
        buttons[1].label = '❌'
        buttons[1].style = discord.ButtonStyle.green
        buttons[1].disabled = True
        await bot_turn()
        await interaction.response.edit_message(view=view)

    buttons[1].callback = button_2_callback

    async def button_3_callback(interaction):
        situation[2] = '❌'
        buttons[2].label = '❌'
        buttons[2].style = discord.ButtonStyle.green
        buttons[2].disabled = True
        await bot_turn()
        await interaction.response.edit_message(view=view)

    buttons[2].callback = button_3_callback

    async def button_4_callback(interaction):
        situation[3] = '❌'
        buttons[3].label = '❌'
        buttons[3].style = discord.ButtonStyle.green
        buttons[3].disabled = True
        await bot_turn()
        await interaction.response.edit_message(view=view)

    buttons[3].callback = button_4_callback

    async def button_5_callback(interaction):
        situation[4] = '❌'
        buttons[4].label = '❌'
        buttons[4].style = discord.ButtonStyle.green
        buttons[4].disabled = True
        await bot_turn()
        await interaction.response.edit_message(view=view)

    buttons[4].callback = button_5_callback

    async def button_6_callback(interaction):
        situation[5] = '❌'
        buttons[5].label = '❌'
        buttons[5].style = discord.ButtonStyle.green
        buttons[5].disabled = True
        await bot_turn()
        await interaction.response.edit_message(view=view)

    buttons[5].callback = button_6_callback

    async def button_7_callback(interaction):
        situation[6] = '❌'
        buttons[6].label = '❌'
        buttons[6].style = discord.ButtonStyle.green
        buttons[6].disabled = True
        await bot_turn()
        await interaction.response.edit_message(view=view)

    buttons[6].callback = button_7_callback

    async def button_8_callback(interaction):
        situation[7] = '❌'
        buttons[7].label = '❌'
        buttons[7].style = discord.ButtonStyle.green
        buttons[7].disabled = True
        await bot_turn()
        await interaction.response.edit_message(view=view)

    buttons[7].callback = button_8_callback

    async def button_9_callback(interaction):
        situation[8] = '❌'
        buttons[8].label = '❌'
        buttons[8].style = discord.ButtonStyle.green
        buttons[8].disabled = True
        await bot_turn()
        await interaction.response.edit_message(view=view)

    buttons[8].callback = button_9_callback



token_2 = ""
bot.run(token_2)