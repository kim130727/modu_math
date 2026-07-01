from __future__ import annotations

import mimetypes
import os
import base64
from pathlib import Path
from typing import Literal

Provider = Literal["openai", "google"]
Mode = Literal["api", "prompt"]

DEFAULT_OPENAI_MODEL = "gpt-5.4-mini"
DEFAULT_GOOGLE_MODEL = "gemini-2.5-flash"


def load_dotenv_if_available() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        env_path = Path(".env")
        if not env_path.exists():
            return
        for raw_line in env_path.read_text(encoding="utf-8-sig").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value
        return
    load_dotenv()


def resolve_provider(cli_provider: str | None) -> Provider:
    provider = (cli_provider or os.getenv("LLM_PROVIDER") or "").strip().lower()
    if provider in ("openai", "google"):
        return provider  # type: ignore[return-value]

    if os.getenv("CI"):
        return "openai"

    if os.isatty(0):
        try:
            choice = input("Select provider [1] OpenAI [2] Google (default: OpenAI): ").strip()
        except OSError:
            return "openai"
        if choice == "2":
            return "google"
    return "openai"


def resolve_model_name(provider: Provider, cli_model: str | None) -> str:
    if cli_model:
        return cli_model
    if provider == "google":
        return os.getenv("GOOGLE_MODEL") or DEFAULT_GOOGLE_MODEL
    return os.getenv("OPENAI_MODEL") or DEFAULT_OPENAI_MODEL


def resolve_mode(cli_mode: str | None) -> Mode:
    mode = (cli_mode or os.getenv("LLM_MODE") or "api").strip().lower()
    if mode in ("api", "prompt"):
        return mode  # type: ignore[return-value]
    return "api"


def maybe_write_prompt_bundle(
    *,
    prompt_out: Path | None,
    system_prompt: str,
    user_prompt: str,
    extra_user_texts: list[str] | None = None,
    image_path: Path | None = None,
    provider: Provider | None = None,
    model: str | None = None,
) -> None:
    if prompt_out is None:
        return
    extra_user_texts = extra_user_texts or []
    prompt_out.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    if provider:
        lines.append(f"# provider: {provider}")
    if model:
        lines.append(f"# model: {model}")
    if image_path is not None:
        lines.append(f"# image_path: {image_path}")
    lines.append("")
    lines.append("## System Prompt")
    lines.append(system_prompt)
    lines.append("")
    lines.append("## User Prompt")
    lines.append(user_prompt)
    if extra_user_texts:
        lines.append("")
        lines.append("## Extra User Texts")
        for idx, text in enumerate(extra_user_texts, start=1):
            lines.append(f"### Extra {idx}")
            lines.append(text)
    prompt_out.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def call_llm_text_with_optional_image(
    *,
    provider: Provider,
    model: str,
    system_prompt: str,
    user_prompt: str,
    image_path: Path | None = None,
    image_detail: str = "high",
    extra_user_texts: list[str] | None = None,
) -> str:
    extra_user_texts = extra_user_texts or []
    if provider == "google":
        return _call_google(
            model=model,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            image_path=image_path,
            extra_user_texts=extra_user_texts,
        )
    return _call_openai(
        model=model,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        image_path=image_path,
        image_detail=image_detail,
        extra_user_texts=extra_user_texts,
    )


def run_llm_or_load_output(
    *,
    mode: Mode,
    llm_output_file: Path | None,
    prompt_out: Path | None,
    provider: Provider,
    model: str,
    system_prompt: str,
    user_prompt: str,
    image_path: Path | None = None,
    image_detail: str = "high",
    extra_user_texts: list[str] | None = None,
) -> str | None:
    extra_user_texts = extra_user_texts or []
    maybe_write_prompt_bundle(
        prompt_out=prompt_out,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        extra_user_texts=extra_user_texts,
        image_path=image_path,
        provider=provider,
        model=model,
    )
    if mode == "prompt":
        if llm_output_file is None:
            return None
        if not llm_output_file.exists():
            return None
        return llm_output_file.read_text(encoding="utf-8-sig").strip()
    output_text = call_llm_text_with_optional_image(
        provider=provider,
        model=model,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        image_path=image_path,
        image_detail=image_detail,
        extra_user_texts=extra_user_texts,
    )
    if llm_output_file is not None:
        llm_output_file.parent.mkdir(parents=True, exist_ok=True)
        llm_output_file.write_text(output_text.rstrip() + "\n", encoding="utf-8")
    return output_text


def _call_openai(
    *,
    model: str,
    system_prompt: str,
    user_prompt: str,
    image_path: Path | None,
    image_detail: str,
    extra_user_texts: list[str],
) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is not set. Add it to your environment or .env file.")
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise ImportError("openai package is required. Install with: pip install openai") from exc

    user_content: list[dict[str, str]] = [{"type": "input_text", "text": user_prompt}]
    for text in extra_user_texts:
        user_content.append({"type": "input_text", "text": text})

    if image_path is not None:
        mime_type, _ = mimetypes.guess_type(str(image_path))
        if not mime_type:
            mime_type = "image/png"
        image_data_url = f"data:{mime_type};base64,{base64.b64encode(image_path.read_bytes()).decode('ascii')}"
        user_content.append({"type": "input_image", "image_url": image_data_url, "detail": image_detail})

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]},
            {"role": "user", "content": user_content},
        ],
    )
    output_text = getattr(response, "output_text", None)
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()
    output = getattr(response, "output", None)
    if isinstance(output, list):
        chunks: list[str] = []
        for item in output:
            content = getattr(item, "content", None)
            if not isinstance(content, list):
                continue
            for part in content:
                if getattr(part, "type", None) == "output_text":
                    text = getattr(part, "text", None)
                    if isinstance(text, str):
                        chunks.append(text)
        merged = "\n".join(chunks).strip()
        if merged:
            return merged
    raise ValueError("Could not extract text output from OpenAI response.")


def _call_google(
    *,
    model: str,
    system_prompt: str,
    user_prompt: str,
    image_path: Path | None,
    extra_user_texts: list[str],
) -> str:
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GOOGLE_API_KEY (or GEMINI_API_KEY) is not set.")
    try:
        from google import genai
        from google.genai import types
    except ImportError as exc:
        raise ImportError("google-genai package is required. Install with: pip install google-genai") from exc

    client = genai.Client(api_key=api_key)
    contents: list[object] = [user_prompt]
    contents.extend(extra_user_texts)
    if image_path is not None:
        mime_type, _ = mimetypes.guess_type(str(image_path))
        if not mime_type:
            mime_type = "image/png"
        contents.append(types.Part.from_bytes(data=image_path.read_bytes(), mime_type=mime_type))

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
    text = getattr(response, "text", None)
    if isinstance(text, str) and text.strip():
        return text.strip()
    raise ValueError("Could not extract text output from Google response.")
