from nonebot import on_command, CommandSession
import json
from datetime import datetime
import gpt_api

gpt_t = gpt_api.gpt_thread()


def readjson(filename):
    with open(filename, encoding='utf-8') as f:
        data = json.load(f)
    return data


def write2json(filename, data):
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def archive(data):
    current_time = datetime.now()
    time_format = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f'history/{time_format}.json'
    write2json(filename, data)


@on_command('ask', aliases=('ask', '/ask', '.', '。'))
async def ask(session: CommandSession):
    prompt = session.current_arg_text.strip()
    response = gpt_t.get_response(prompt)
    reply_msg = response['choices'][0]['message']['content']
    await session.send(reply_msg)


@on_command('save', aliases=('/save', 'save'))
async def save(session: CommandSession):
    archive(gpt_t.messages)
    await session.send('已保存上一轮对话了喵。')


@on_command('init', aliases=('/init', 'init'))
async def init(session: CommandSession):
    archive(gpt_t.messages)
    await session.send('已保存上一轮对话了喵')
    gpt_t.reset_log()
    await session.send('初始化了喵，现在床爪不记得任何事情。')

