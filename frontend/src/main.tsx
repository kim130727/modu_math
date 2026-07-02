import { render } from "solid-js/web";
import { EditorPage } from "./components/EditorPage";
import "./styles/editor-next.css";

const root = document.getElementById("editor-next-root");

if (!root) {
  throw new Error("editor-next-root not found");
}

render(() => <EditorPage />, root);

