import os
from dataclasses import dataclass
from pathlib import Path

import openai
from functools import cached_property
from typing import Union, List, Optional, Dict

from langchain_openai import ChatOpenAI
from llama_index.core import StorageContext, load_index_from_storage, ServiceContext, VectorStoreIndex, \
    SimpleDirectoryReader, Document
from llama_index.core.base.response.schema import StreamingResponse, Response
from llama_index.core.readers.base import BaseReader

from imk.imk_io import ImkIoInDir
import trafilatura


class HtmlReader(BaseReader):
    def load_data(
        self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
        """Reads HTML and uses trafilatura to extract text."""
        results = []
        with open(file, 'r') as f:
            text = trafilatura.extract(f.read())
            results.append(Document(text=text, extra_info=extra_info))

        return results


class ImkGpt:
    """
    s100.py.gpt("index_path").l("test1.md").l("test2.md").
    """
    def __init__(self, s100):
        self.s100 = s100
        openai.api_key = os.environ['OPENAI_API_KEY']

    def __call__(self, save_path) -> 'ImkGptSystem':
        dir_io = self.s100.py.io(save_path).mk()
        if dir_io.e('llama_index'):
            # https://github.com/jerryjliu/llama_index/issues/1608
            # from llama-index-0.5.7 => llama-index-0.6.21.post1
            # https://gpt-index.readthedocs.io/en/latest/guides/primer/usage_pattern.html#optional-save-the-index-for-future-use
            # index = GPTSimpleVectorIndex.load_from_disk(self.s100.py.io.s(save_path))
            storage_context = StorageContext.from_defaults(persist_dir=dir_io.s('llama_index'))
            index = load_index_from_storage(storage_context)
        else:
            index = VectorStoreIndex.from_documents([])
        return ImkGptSystem(self.s100, index, dir_io)


class ImkGptSystem:
    def __init__(self, s100, index: VectorStoreIndex, dir_io: ImkIoInDir):
        self.s100 = s100
        self.index = index
        self.dir_io = dir_io

    def l(self, path: str):
        """loads the txt and HTML files in the given directory into the index,
        ignoring any files that have already been loaded"""

        reg = self.s100.py.io(path).reg(self.dir_io.s('indexed_files.json'))
        new = reg.new()
        input_files = [e.path for e in new]
        if input_files:
            print(f'{input_files=}')
            documents = SimpleDirectoryReader(
                input_files=input_files,
                file_extractor={
                    ".html": HtmlReader(),
                }
            ).load_data()
            for d in documents:
                self.index.insert(d)

            reg.add(new)
            self.index.storage_context.persist(persist_dir=self.dir_io.s('llama_index'))

        return self

    @cached_property
    def qa(self):
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.)
        service_context = ServiceContext.from_defaults(llm=llm)
        return ImkGptQaSystem(self.s100, self.index.as_query_engine(service_context=service_context))

    @cached_property
    def chat(self):
        # https://gpt-index.readthedocs.io/en/latest/how_to/chat_engine/root.html
        # https://gpt-index.readthedocs.io/en/latest/examples/chat_engine/chat_engine_react.html
        # Use ChatGPT (“gpt-3.5-turbo”)
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.)
        service_context = ServiceContext.from_defaults(llm=llm)
        return ImkGptChatSystem(self.s100, self.index.as_chat_engine(service_context=service_context, verbose=True))


class ImkGptQaSystem:
    def __init__(self, s100, query_engine):
        self.s100 = s100
        self.query_engine = query_engine

    def __call__(self, *args, **kwargs):
        return ImkGptResponse(self.query_engine.query(*args, **kwargs))


class ImkGptChatSystem:
    def __init__(self, s100, chat_engine):
        self.s100 = s100
        self.chat_engine = chat_engine

    def __call__(self, *args, **kwargs):
        return ImkGptResponse(self.chat_engine.chat(*args, **kwargs))

    def re(self):
        self.chat_engine.reset()
        return self


@dataclass(frozen=True)
class ImkGptResponse:
    response: Union[Response, StreamingResponse]

    def __str__(self):
        return self.response.response

    def __repr__(self):
        return f'ImkGptResponse({self.response.response})'
