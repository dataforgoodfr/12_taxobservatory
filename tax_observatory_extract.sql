CREATE TABLE "documents" (
  "id" serial PRIMARY KEY,
  "s3_id" varchar UNIQUE,
  "relevant_pages" integer[],
  "created_at" timestamp,
  "modified_at" timestamp
);

CREATE TABLE "table_extractors" (
  "id" serial PRIMARY KEY,
  "name" varchar UNIQUE
);

CREATE TABLE "table_extractor_params" (
  "id" serial PRIMARY KEY,
  "table_extractor_id" integer,
  "params" json,
  "params_text" text GENERATED ALWAYS AS (params::text) STORED UNIQUE
);

CREATE TABLE "llm_models" (
  "id" serial PRIMARY KEY,
  "name" varchar UNIQUE
);

CREATE TABLE "llm_model_params" (
  "id" serial PRIMARY KEY,
  "llm_model_id" integer,
  "params" json,
  "params_text" text GENERATED ALWAYS AS (params::text) STORED UNIQUE
);

CREATE TABLE "llm_extracted_data" (
  "id" serial PRIMARY KEY,
  "document_id" integer,
  "table_extractor_id" integer,
  "table_extractor_params_id" integer,
  "llm_model_id" integer,
  "llm_model_params_id" integer,
  "data" bytea
);

CREATE TABLE "corrected_data" (
  "id" serial PRIMARY KEY,
  "document_id" integer UNIQUE,
  "data" bytea
);

ALTER TABLE "table_extractor_params" ADD FOREIGN KEY ("table_extractor_id") REFERENCES "table_extractors" ("id");

ALTER TABLE "llm_model_params" ADD FOREIGN KEY ("llm_model_id") REFERENCES "llm_models" ("id");

ALTER TABLE "llm_extracted_data" ADD FOREIGN KEY ("document_id") REFERENCES "documents" ("id");

ALTER TABLE "llm_extracted_data" ADD FOREIGN KEY ("table_extractor_id") REFERENCES "table_extractors" ("id");

ALTER TABLE "llm_extracted_data" ADD FOREIGN KEY ("table_extractor_params_id") REFERENCES "table_extractor_params" ("id");

ALTER TABLE "llm_extracted_data" ADD FOREIGN KEY ("llm_model_id") REFERENCES "llm_models" ("id");

ALTER TABLE "llm_extracted_data" ADD FOREIGN KEY ("llm_model_params_id") REFERENCES "llm_model_params" ("id");

ALTER TABLE "corrected_data" ADD FOREIGN KEY ("document_id") REFERENCES "documents" ("id");
