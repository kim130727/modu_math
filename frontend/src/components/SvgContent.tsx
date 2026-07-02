interface SvgContentProps {
  svg: string;
}

export function SvgContent(props: SvgContentProps) {
  return <div class="svg-content" innerHTML={props.svg} />;
}

