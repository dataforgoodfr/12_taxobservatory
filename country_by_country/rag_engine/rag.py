import pandas as pd
from operator import itemgetter

from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts.prompt import PromptTemplate
from langchain.schema import format_document

from country_by_country.utils import pass_values, flatten_dict


DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")


def _combine_documents(docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, sep="\n\n"):
    doc_strings = [
        f"Doc {i+1}: " + format_document(doc, document_prompt)
        for i, doc in enumerate(docs)
    ]
    return sep.join(doc_strings)


def make_rag_chain(retriever, llm):
    template = """
    You are an economical expert, with 20 years experience analyzing corporate financial reports.
    You will answer the question based on the following table extracted from a financial report:
    ```
    {context}
    ```

    Guidelines:
    - Given a question you will be given extracted parts of a financial report for a company that should be relevant to answer the question.
    - If they are not relevant don't include the passages in your answer.
    - Keep as many facts and figures in your final answer
    - Stay as sharp as possible, don't include contextual information, focus on the answer
    - Give the smallest answer possible, don't make it longer than necessary
    - Focus on specifically answering the question not related questions
    - If you don't know the answer, just say that you don't know. Don't try to make up an answer.
    - Use bullet point lists if relevant in your answer.
    - When you use information from a passage, mention where it came from by using [Doc i] at the end of the sentence. i stands for the number of the document.
    - Do not use the sentence 'Doc i says ...' to say where information came from.
    - If the same thing is said in more than one document, you can mention all of them like this: [Doc i, Doc j, Doc k]
    - Instead of providing bullet-point summaries for each passage, compile your summaries into well-structured paragraphs. This approach emphasizes the crucial elements in the explanation.
    - When addressing a 'how' question, concentrate on the methods and procedures employed, rather than the outcomes.
    - You do not need to use every passage. Only use the ones that help answer the question.
    - If the documents do not have the information needed to answer the question, just say you do not have enough information.

    Question: {question}
    Answer:
    """

    # Construct the prompt
    prompt = ChatPromptTemplate.from_template(template)

    # ------- CHAIN 1
    # Retrieved documents
    retrieved_documents = {
        "docs": itemgetter("question") | retriever,
        "question": itemgetter("question"),
    } | RunnablePassthrough()

    # ------- CHAIN 2
    # Construct inputs for the llm
    input_documents = {
        "context": lambda x: _combine_documents(x["docs"]),
        "question": itemgetter("question"),
    }

    # Generate the answer
    answer = {
        "answer": input_documents | prompt | llm | StrOutputParser(),
        "docs": itemgetter("docs"),
        "question": itemgetter("question"),
    }

    # ------- FINAL CHAIN
    # Build the final chain
    chain = retrieved_documents | answer

    return chain

class Extraction:
    def __init__(self, retriever, llm, k=1, max_threads=5):
        self.llm = llm
        self.k = k
        self.max_threads = max_threads
        self.retriever = retriever
        self.rag_chain = (
            {
                "rag": make_rag_chain(self.retriever, self.llm),
            }
            | RunnablePassthrough()
            | flatten_dict
        )
        
    def ask(self, question):
        result = self.rag_chain.invoke({"question": question})
        return result

    def run(self, questions):
        all_answers = []
        validated_questions = []
        remaining_questions = [x for x in questions if x not in validated_questions]

        for question in remaining_questions:
            try:
                answer = self.ask(question)
                all_answers.append(answer)
                validated_questions.append(question)
            except Exception as e:
                print(e)
        # Format the answers to a dataframe
        all_answers_df = []
        for answer in all_answers:
            # answer = answer[0]
            answer_dict = {
                "question": answer["question"],
                "answer": answer["answer"],
            }
            for i, x in enumerate(answer["docs"]):
                # answer_dict[f"Doc {i+1}"] = os.path.basename(x.metadata["source"])
                answer_dict[f"Doc {i+1} page"] = x.metadata["page"]
                answer_dict[f"Doc {i+1} relevant content"] = x.page_content
            all_answers_df.append(answer_dict)
        all_answers_df = pd.DataFrame(all_answers_df)

        # Merge questions and answers
        # final_df = esrs_df.drop_duplicates(subset="question").merge(
        #     all_answers_df.drop_duplicates(subset="question"), on="question"
        # )

        return all_answers_df
