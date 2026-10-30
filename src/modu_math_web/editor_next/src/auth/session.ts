const TOKEN_KEY = "modu_math_teacher_token_v1";

export function sessionToken(): string {
  return window.sessionStorage.getItem(TOKEN_KEY) ?? "";
}

export function storeToken(token: string): void {
  if (token) window.sessionStorage.setItem(TOKEN_KEY, token);
  else window.sessionStorage.removeItem(TOKEN_KEY);
}

export function editorAuthHeaders(): Record<string, string> {
  const token = sessionToken();
  return token ? { Authorization: `Token ${token}` } : {};
}
