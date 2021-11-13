from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

import subprocess
import sys
import requests
from bs4 import BeautifulSoup
import webbrowser


class LingUeeExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        if event.get_argument() != None:
            address = f'https://www.linguee.de/deutsch-englisch/search?source=auto&query={event.get_argument()}'
            request = requests.get(address)
            soup = BeautifulSoup(request.content, "html.parser")
            try:
                trans = ", ".join([i.find('a').text.strip() for i in soup.find_all('h3', {'class': 'translation_desc'})[:3]])
            except:
                trans = "Not found"
            data = {
                'name': event.get_argument(),
                'description': trans,
                'address': address}

            return RenderResultListAction([
                ExtensionResultItem(icon='images/icon.png',
                    name=data['name'],
                    description=data['description'],
                    on_enter=ExtensionCustomAction(data, keep_app_open=True))
            ])

        else:
            return RenderResultListAction([
                ExtensionResultItem(icon='images/icon.png',
                    name='Search Linguee',
                    description='Search for a word in Linguee',
                    on_enter=HideWindowAction())
            ])


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()
        return RenderResultListAction([
            ExtensionResultItem(icon='images/icon.png',
                                name=data['name'],
                                description=data['description'],
                                on_enter=webbrowser.open(data['address']))
        ])

if __name__ == '__main__':
    LingUeeExtension().run()