const MATHJAX_BASE_URL = "/static/editor_next/tldraw_assets/mathjax";
const MATHJAX_FONT_BASE_URL = "/static/editor_next/tldraw_assets/mathjax-newcm";
const MATHJAX_COMPONENT_URL = `${MATHJAX_BASE_URL}/tex-svg.js`;

declare global {
  interface Window {
    MathJax?: {
      tex2svgPromise?: (latex: string, options?: Record<string, unknown>) => Promise<HTMLElement>;
      startup?: {
        promise?: Promise<void>;
      };
      loader?: Record<string, unknown>;
      tex?: Record<string, unknown>;
      svg?: Record<string, unknown>;
      options?: Record<string, unknown>;
    };
  }
}

let mathJaxLoadPromise: Promise<void> | null = null;

export async function renderLatexToSvgDataUrl(latex: string): Promise<string> {
  const normalizedLatex = latex.trim();
  if (!normalizedLatex) return "";

  await loadMathJax();
  const mathJax = window.MathJax;
  if (!mathJax?.tex2svgPromise) return fallbackSvgDataUrl(normalizedLatex);

  try {
    const container = await mathJax.tex2svgPromise(normalizedLatex, { display: false });
    const svg = container.querySelector("svg");
    if (!svg) return fallbackSvgDataUrl(normalizedLatex);
    svg.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    svg.removeAttribute("style");
    return svgToDataUrl(svg.outerHTML);
  } catch {
    return fallbackSvgDataUrl(normalizedLatex);
  }
}

function loadMathJax(): Promise<void> {
  if (window.MathJax?.tex2svgPromise) return Promise.resolve();
  if (mathJaxLoadPromise) return mathJaxLoadPromise;

  window.MathJax = {
    loader: {
      load: ["input/tex", "output/svg"],
      paths: {
        mathjax: MATHJAX_BASE_URL,
        "mathjax-newcm": MATHJAX_FONT_BASE_URL,
      },
    },
    tex: {
      packages: { "[+]": ["ams"] },
      inlineMath: [["\\(", "\\)"]],
      displayMath: [["\\[", "\\]"]],
    },
    svg: {
      fontCache: "none",
      linebreaks: { automatic: false },
    },
    options: {
      enableMenu: false,
    },
  };

  mathJaxLoadPromise = new Promise<void>((resolve, reject) => {
    const existing = document.querySelector<HTMLScriptElement>(`script[src="${MATHJAX_COMPONENT_URL}"]`);
    const script = existing ?? document.createElement("script");
    script.src = MATHJAX_COMPONENT_URL;
    script.async = true;
    script.onload = async () => {
      try {
        await (window.MathJax?.startup?.promise ?? Promise.resolve());
        resolve();
      } catch (error) {
        reject(error);
      }
    };
    script.onerror = () => reject(new Error("Could not load local MathJax bundle."));
    if (!existing) document.head.appendChild(script);
  });

  return mathJaxLoadPromise;
}

function fallbackSvgDataUrl(text: string): string {
  const escaped = escapeXml(text);
  const width = Math.max(120, text.length * 12);
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="36" viewBox="0 0 ${width} 36"><rect width="100%" height="100%" fill="white"/><text x="0" y="26" font-family="Segoe UI, Arial" font-size="24" fill="#111827">${escaped}</text></svg>`;
  return svgToDataUrl(svg);
}

function svgToDataUrl(svg: string): string {
  return `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
}

function escapeXml(value: string): string {
  return value.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
