from vk_api import VkApi

import settings


vk_session = VkApi(token=settings.VK_ACCESS_TOKEN)
vk_app = vk_session.get_api()
