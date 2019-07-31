# SCP-079-REGEX - Manage the regex patterns
# Copyright (C) 2019 SCP-079 <https://scp-079.org>
#
# This file is part of SCP-079-REGEX.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import re

from pyrogram import Client, Message

from .. import glovar
from .etc import code, get_forward_name, get_text, t2s, thread, user_mention
from .telegram import send_message
from .words import similar

# Enable logging
logger = logging.getLogger(__name__)


def name_test(client: Client, message: Message) -> bool:
    # Test user's or channel's name
    try:
        name_text = get_forward_name(message)
        if name_text:
            cid = message.chat.id
            aid = message.from_user.id
            mid = message.message_id
            text = ""
            text += f"管理员：{user_mention(aid)}\n\n"
            text += f"来源名称：{code(name_text)}\n\n"
            result = ""
            # Can add more test to the "for in" list
            for word_type in ["ad", "con", "iml", "nm", "wb"]:
                if glovar.compiled[word_type].search(name_text):
                    w_list = [w for w in eval(f"glovar.{word_type}_words") if similar("test", w, name_text)]
                    result += "\t" * 4 + f"{glovar.names[word_type]}：" + "\\-" * 16 + "\n\n"
                    for w in w_list:
                        result += "\t" * 8 + f"{code(w)}\n\n"

            if result:
                text += result
            else:
                text = ""

            thread(send_message, (client, cid, text, mid))
            return True
    except Exception as e:
        logger.warning(f"Name test error: {e}", exc_info=True)

    return False


def sticker_test(client: Client, message: Message) -> bool:
    # Test sticker set name
    try:
        if message.sticker and message.sticker.set_name:
            cid = message.chat.id
            aid = message.from_user.id
            mid = message.message_id
            result = ""
            result += f"管理员：{user_mention(aid)}\n\n"
            text = message.sticker.set_name
            text = t2s(text)
            result += f"贴纸名称：{code(text)}\n\n"
            # Can add more test to the "for in" list
            for word_type in ["sti"]:
                if glovar.compiled[word_type].search(text):
                    w_list = [w for w in eval(f"glovar.{word_type}_words") if similar("test", w, text)]
                    result += "\t" * 4 + f"{glovar.names[word_type]}：" + "\\-" * 16 + "\n\n"
                    for w in w_list:
                        result += "\t" * 8 + f"{code(w)}\n\n"

            thread(send_message, (client, cid, result, mid))
            return True
    except Exception as e:
        logger.warning(f"Sticker test error: {e}", exc_info=True)

    return False


def text_test(client: Client, message: Message) -> bool:
    # Test message text or caption
    try:
        message_text = get_text(message)
        except_pattern = ("^版本：|"
                          "^#(bug|done|fixed|todo)|"
                          "^{|"
                          "^消息结构：")
        if message_text and not re.search(except_pattern, message_text, re.I | re.M | re.S):
            cid = message.chat.id
            if re.search("^管理员：[0-9]", message_text):
                aid = int(message_text.split("\n")[0].split("：")[1])
            else:
                aid = message.from_user.id

            mid = message.message_id
            result = ""
            for word_type in glovar.names:
                if glovar.compiled[word_type].search(message_text):
                    w_list = [w for w in eval(f"glovar.{word_type}_words") if similar("test", w, message_text)]
                    result += f"{glovar.names[word_type]}：" + "—" * 16 + "\n\n"
                    for w in w_list:
                        result += "\t" * 4 + f"{code(w)}\n\n"

            if result:
                result = (f"管理员：{user_mention(aid)}\n\n"
                          f"{result}")
                thread(send_message, (client, cid, result, mid))

            return True
    except Exception as e:
        logger.warning(f"Text test error: {e}", exc_info=True)

    return False
