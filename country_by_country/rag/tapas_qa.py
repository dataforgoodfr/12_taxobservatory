# MIT License
#
# Copyright (c) 2024 dataforgood
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# External imports
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoModelForTableQuestionAnswering,
    AutoTokenizer,
    pipeline,
)

import pandas as pd


class TapasQA:
    def __init__(self, model_name, questions):
        print(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.pipe = pipeline(
            "table-question-answering", model=model, tokenizr=tokenizer
        )
        self.questions = questions

    def __call__(self, table: pd.DataFrame):
        table = table.astype(str)
        table.columns = table.columns.astype(str)
        print(table)
        print(self.questions)
        for query in self.questions:
            results = self.pipe(table=table, query=query)
            print(results)
            # encoding = self.tokenizer(
            #     table=table,
            #     query=query,
            #     return_tensors="pt",
            #     max_length=512,
            #     truncation=True,
            # )
            # # print(encoding)
            # outputs = self.model.generate(**encoding)
            # decoded_output = self.tokenizer.batch_decode(
            #     outputs, skip_special_tokens=True
            # )
            # print(f"{query} : {decoded_output}")

            # inputs = self.tokenizer(
            #     table=table,
            #     queries=[question],
            #     padding="max_length",
            #     return_tensors="pt",
            # )

            # # Forward pass
            # outputs = self.model(**inputs)

            # # Decoding the outputs
            # (
            #     predicted_answer_coordinates,
            #     predicted_aggregation_indices,
            # ) = self.tokenizer.convert_logits_to_predictions(
            #     inputs, outputs.logits.detach(), outputs.logits_aggregation.detach()
            # )

            # id2aggregation = {0: "NONE", 1: "SUM", 2: "AVERAGE", 3: "COUNT"}
            # aggregation_predictions_string = [
            #     id2aggregation[x] for x in predicted_aggregation_indices
            # ]
            # answers = []

            # for coordinates in predicted_answer_coordinates:
            #     if len(coordinates) == 1:
            #         # only a single cell:
            #         answers.append(table.iat[coordinates[0]])
            #     else:
            #         # multiple cells
            #         cell_values = []
            #         for coordinate in coordinates:
            #             cell_values.append(table.iat[coordinate])
            #         answers.append(", ".join(cell_values))

            # for query, answer, predicted_agg in zip(
            #     [question], answers, aggregation_predictions_string
            # ):
            #     print(query)
            #     if predicted_agg == "NONE":
            #         print("Predicted answer: " + answer)
            #     else:
            #         print("Predicted answer: " + predicted_agg + " > " + answer)
