from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot import get_bot
import json
from datetime import datetime
import gpt_api

public_session = gpt_api.gpt_thread()
session_list = {}

def readjson(filename):
    with open(filename, encoding='utf-8') as f:
        data = json.load(f)
    return data


def write2json(filename, data):
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def archive(data, qq_number=''):
    current_time = datetime.now()
    time_format = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    if qq_number:
        filename = f'history/{time_format}-{qq_number}.json'
    else:
        filename = f'history/{time_format}.json'
    write2json(filename, data)


@on_command('pask', aliases='pask')
async def pask(session: CommandSession):
    prompt = session.current_arg_text.strip()
    response = public_session.get_response(prompt)
    reply_msg = response['choices'][0]['message']['content']
    await session.send(f'[public]\n{reply_msg}')


@on_command('save', aliases='save')
async def save(session: CommandSession):
    user_id = session.ctx['user_id']
    qq_number = str(user_id)
    if qq_number not in session_list:
        await session.send('你还没有和床爪说过话喵')
    else:
        archive(session_list[user_id].messages, qq_number)
        await session.send('已保存上一轮对话了喵。')


@on_command('psave', aliases='psave')
async def psave(session: CommandSession):
    archive(public_session.messages)
    await session.send('[public]已保存上一轮对话了喵。')


@on_command('saveall', aliases='saveall')
async def psave(session: CommandSession):
    for qq_number in session_list:
        archive(session_list[qq_number].messages, qq_number)
        await session.send(f'已保存{qq_number}的对话.')
    archive(public_session.messages, 'public')
    await session.send('已保存公共session的对话.')


@on_command('reset', aliases='reset')
async def reset(session: CommandSession):
    user_id = session.ctx['user_id']
    qq_number = str(user_id)
    if qq_number not in session_list:
        await session.send('你还没有和床爪说过话喵')
    else:
        archive(session_list[qq_number].messages)
        await session.send('已保存上一轮对话了喵')
        session_list[qq_number].reset_log()
        await session.send('初始化了喵，现在床爪不记得任何事情。')


@on_command('preset', aliases='preset')
async def preset(session: CommandSession):
    archive(public_session.messages)
    await session.send('[public]已保存上一轮对话了喵')
    public_session.reset_log()
    await session.send('[public]初始化了喵，现在床爪不记得任何事情。')


@on_command('init', aliases='init')
async def init(session: CommandSession):
    user_id = session.ctx['user_id']
    qq_number = str(user_id)
    if qq_number not in session_list:
        session_list[qq_number] = gpt_api.gpt_thread()
    else:
        archive(session_list[user_id].messages)
        await session.send('已保存上一轮对话了喵')
    prompt = session.current_arg_text.strip()
    session_list[user_id].reset_system_content(prompt)
    await session.send(f'设定初始prompt为{prompt}')


@on_command('pinit', aliases='pinit')
async def pinit(session: CommandSession):
    archive(public_session.messages)
    await session.send('[public]已保存上一轮对话了喵')
    prompt = session.current_arg_text.strip()
    public_session.reset_system_content(prompt)
    await session.send(f'[public]设定初始prompt为{prompt}')



@on_command('who', aliases='who')
async def who(session: CommandSession):
    userID = session.ctx['user_id']
    await session.send(str(userID))


@on_natural_language(only_short_message=False)
async def default_(session: NLPSession):
    user_id = session.ctx['user_id']
    qq_number = str(user_id)
    if qq_number not in session_list:
        session_list[qq_number] = gpt_api.gpt_thread()
    prompt = session.msg_text
    response = session_list[qq_number].get_response(prompt)
    reply_msg = response['choices'][0]['message']['content']
    await session.send(reply_msg)