from .indexer import build_and_write_index, build_index_entries, load_index_jsonl, write_index_jsonl
from .logger import append_run_log, load_run_logs
from .meta_recommender import infer_problem_id_from_image_path, recommend_input_meta, tune_meta_from_ocr_features
from .ocr import OcrBox, OcrPreprocessResult, extract_ocr_features, merge_ocr_result_into_meta
from .pipeline import build_generation_scaffold, make_run_id, persist_generated_outputs, validate_generated_python
from .prompt_builder import build_few_shot_prompt
from .retrieve import retrieve_examples, retrieve_examples_from_entries, score_entry

__all__ = [
    "build_index_entries",
    "write_index_jsonl",
    "build_and_write_index",
    "load_index_jsonl",
    "score_entry",
    "retrieve_examples_from_entries",
    "retrieve_examples",
    "build_few_shot_prompt",
    "infer_problem_id_from_image_path",
    "recommend_input_meta",
    "tune_meta_from_ocr_features",
    "OcrBox",
    "OcrPreprocessResult",
    "extract_ocr_features",
    "merge_ocr_result_into_meta",
    "make_run_id",
    "build_generation_scaffold",
    "validate_generated_python",
    "persist_generated_outputs",
    "append_run_log",
    "load_run_logs",
]
