def dbcred():
    lines = [line.rstrip() for line in open('discord-wigobot/credentials.txt')]
    return (lines[1].split('::')[1])

def bot_token():
    lines = [line.rstrip() for line in open('discord-wigobot/credentials.txt')]
    return (lines[0].split('::')[1])