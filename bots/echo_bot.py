# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount
import aiohttp

class EchoBot(ActivityHandler):
    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")

    async def on_message_activity(self, turn_context: TurnContext):
        user_input = turn_context.activity.text

        payload = {
            "conversation_context": user_input,
            "sql_query_template": "v0",
            "offers_selection_limit": 5,
            "offers_final_limit": 5
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://arg-glider-wus2-sandbox.azurewebsites.net/api/v1/sandbox/infinite-shopping-demo/node-sql",
                    json=payload,
                ) as resp:
                    response_data = await resp.text()

            # 🗣 Send back the external API's response to the user
            await turn_context.send_activity(
                MessageFactory.text(f"🧠 API Response:\n{response_data}")
            )

        except Exception as e:
            await turn_context.send_activity(
                MessageFactory.text(f"❌ Failed to contact external API:\n{e}")
            )
