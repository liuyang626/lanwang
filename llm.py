from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import UnstructuredFileLoader
from langchain import OpenAI, VectorDBQA

import os

os.getenv('OPENAI_API_KEY')


def embedding_persist(file):
    # 创建 TextFileLoader
    loader = UnstructuredFileLoader(file)
    # 将文本转成 Document 对象
    document = loader.load()

    # 初始化 openai 的 embeddings 对象
    embeddings = OpenAIEmbeddings()

    # 持久化数据
    docsearch = Chroma.from_documents(document, embeddings, persist_directory="vector_store")
    docsearch.persist()


def vector_search(query):
    # 初始化 openai 的 embeddings 对象
    embeddings = OpenAIEmbeddings()

    # 加载数据
    docsearch = Chroma(persist_directory="vector_store", embedding_function=embeddings)

    # 创建问答对象
    qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="refine", vectorstore=docsearch,
                                    return_source_documents=True)

    # 进行问答
    return qa({"query": query})
