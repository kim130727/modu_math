function getCsrfToken() {
  const cookies = document.cookie ? document.cookie.split(";") : [];
  for (const c of cookies) {
    const [name, value] = c.trim().split("=");
    if (name === "csrftoken") return decodeURIComponent(value);
  }
  return "";
}

export async function saveSemantic(problemId, semantic) {
  const response = await fetch(`/editor/${problemId}/save/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCsrfToken(),
    },
    body: JSON.stringify({ semantic }),
  });
  return response.json();
}

