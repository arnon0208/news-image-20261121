// A working news-image-daily entry (Node 22, standard library only): its image
// is the entry.png beside this file, and the program copies it to
// /output/entry.png. The gate takes a whole PNG or JPEG of at most 1 MiB and
// 1024 by 1024 pixels, and the judge sees exactly the bytes copied.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const out = join(outDir, 'entry.png');
copyFileSync(new URL('./entry.png', import.meta.url), out);
// Guardrail: the gate refuses anything over 1 MiB or 1024x1024; fail loudly
// here instead of shipping a bad file.
const size = statSync(out).size;
if (size > 1048576) throw new Error(`entry.png is ${size} bytes, over the 1 MiB cap`);
console.log(`wrote ${out} (${size} bytes)`);
