interface SvgContentProps {
  svg: string;
}

export function sanitizeSvgForDisplay(svg: string): string {
  return svg
    .replace(/^\s*<\?xml[^>]*>\s*/i, "")
    .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, "")
    .replace(/<foreignObject\b[^>]*>[\s\S]*?<\/foreignObject>/gi, "")
    .replace(/\s+on[a-z]+\s*=\s*(['"]).*?\1/gi, "")
    .replace(/\s+(?:href|xlink:href)\s*=\s*(['"])\s*javascript:[\s\S]*?\1/gi, "")
    .replace(/(<text\b[^>]*>)([^<]*?)\/text>/gi, "$1$2</text>");
}

export function SvgContent(props: SvgContentProps) {
  return <div class="svg-content" innerHTML={sanitizeSvgForDisplay(props.svg)} />;
}
