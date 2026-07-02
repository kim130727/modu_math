interface SvgContentProps {
  svg: string;
}

export function sanitizeSvgForDisplay(svg: string): string {
  return svg
    .replace(/^\s*<\?xml[^>]*>\s*/i, "")
    .replace(/(<text\b[^>]*>)([^<]*?)\/text>/gi, "$1$2</text>");
}

function svgFrameDocument(svg: string): string {
  return `<!doctype html><html><head><style>html,body{margin:0;width:100%;height:100%;overflow:hidden}svg{display:block;width:100%;height:100%}</style></head><body>${sanitizeSvgForDisplay(svg)}</body></html>`;
}

export function SvgContent(props: SvgContentProps) {
  return (
    <div class="svg-content">
      <iframe class="svg-frame" srcdoc={svgFrameDocument(props.svg)} title="Problem SVG preview" />
    </div>
  );
}
