import { cpSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const source = fileURLToPath(new URL('../../../../apps/mobile/build/web/', import.meta.url));
const destination = fileURLToPath(new URL('../static/editor_next/flutter_editor/', import.meta.url));
mkdirSync(destination, { recursive: true });
cpSync(source, destination, { recursive: true });
console.log(`Flutter editor copied to ${destination}`);
