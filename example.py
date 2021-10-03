from translator import DocumentTranslator 
from handler import ContextHandler
from handler import InstanceHandler

if __name__ == '__main__':
    with open('example_document.json', mode='r', encoding='utf8') as file:
        serialized_document = file.read()
        translator = DocumentTranslator(ContextHandler, InstanceHandler)
        translator.translate(serialized_document)