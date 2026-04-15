function getCsrfToken() {
  const cookies = document.cookie ? document.cookie.split(";") : [];
  for (const c of cookies) {
    const [name, value] = c.trim().split("=");
    if (name === "csrftoken") return decodeURIComponent(value);
  }
  return "";
}

async function postSemantic(problemId, body) {
  const response = await fetch(`/editor/${problemId}/save/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCsrfToken(),
    },
    body: JSON.stringify(body),
  });

  let payload;
  try {
    payload = await response.json();
  } catch (error) {
    return {
      ok: false,
      errors: [`서버 응답 파싱에 실패했습니다. (status=${response.status})`],
    };
  }

  if (!response.ok) {
    return {
      ok: false,
      errors: payload?.errors ?? [`요청이 실패했습니다. (status=${response.status})`],
    };
  }
  return payload;
}

export async function saveSemantic(problemId, semantic) {
  return postSemantic(problemId, { semantic });
}

export async function applySemantic(problemId, semantic) {
  return postSemantic(problemId, { semantic, dry_run: true });
}
