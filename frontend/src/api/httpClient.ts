import type { ApiErrorCategory } from "../types/api";

export class EditorApiError extends Error {
  readonly status: number;
  readonly payload: unknown;
  readonly category: ApiErrorCategory;

  constructor(message: string, status: number, payload: unknown, category: ApiErrorCategory) {
    super(message);
    this.name = "EditorApiError";
    this.status = status;
    this.payload = payload;
    this.category = category;
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function payloadMessage(payload: unknown): string | null {
  if (!isRecord(payload)) return null;
  const error = payload.error;
  if (typeof error === "string" && error.trim()) return error;
  const message = payload.message;
  if (typeof message === "string" && message.trim()) return message;
  return null;
}

export function classifyApiError(message: string, status: number): ApiErrorCategory {
  if (status === 0 || /network|fetch/i.test(message)) return "NETWORK_ERROR";
  if (/patch|slot|layout-patch/i.test(message)) return "DSL_PATCH_ERROR";
  if (/parse|syntax|invalid DSL/i.test(message)) return "DSL_PARSE_ERROR";
  if (/schema|validation/i.test(message)) return "SCHEMA_ERROR";
  if (/build|stderr|compiler/i.test(message) || status >= 500) return "BUILD_ERROR";
  return "UNKNOWN_ERROR";
}

export async function requestJson<T>(url: string, init: RequestInit = {}): Promise<T> {
  let response: Response;
  let payload: unknown;
  try {
    response = await fetch(url, {
      ...init,
      headers: {
        Accept: "application/json",
        ...(init.headers ?? {}),
      },
    });
    payload = await response.json();
  } catch (error) {
    const message = `Network request failed: ${String(error)}`;
    throw new EditorApiError(message, 0, null, "NETWORK_ERROR");
  }

  const okFlag = isRecord(payload) ? payload.ok : undefined;
  if (!response.ok || okFlag === false) {
    const message = payloadMessage(payload) ?? `HTTP ${response.status}`;
    throw new EditorApiError(message, response.status, payload, classifyApiError(message, response.status));
  }
  return payload as T;
}

