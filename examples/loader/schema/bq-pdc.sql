CREATE TABLE `customermod-genai-sa.kalschi_products.product_info`
(
  business_keys ARRAY<STRUCT<value STRING, name STRING>>,
  image_embedding ARRAY<FLOAT64>,
  text_embedding ARRAY<FLOAT64>,
  categories ARRAY<STRUCT<children ARRAY<STRUCT<children ARRAY<STRUCT<children ARRAY<STRUCT<children ARRAY<STRING>, name STRING, id STRING>>, name STRING, id STRING>>, name STRING, id STRING>>, name STRING, id STRING>>,
  base_price STRUCT<rounding_rule STRUCT<trim_insignificant_digits BOOL, relevant_decimal INT64>, value STRUCT<decimal INT64, whole INT64>, code STRING>,
  headers ARRAY<STRUCT<attribute_values ARRAY<STRING>, images ARRAY<STRUCT<url STRING, origin_url STRING>>, nlp_description STRING, locale STRING, long_description STRING, short_description STRING, brand STRING, name STRING>>
);