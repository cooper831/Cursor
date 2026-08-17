#!/usr/bin/env node
/**
 * Stage publishable .md/.html, commit, push, and redeploy Vercel.
 * Used by Cursor stop hook and manual: npm run publish:docs
 */
import { execFileSync, spawnSync } from "child_process";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { shouldPublish } from "./publish-config.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const LOG_FILE = path.join(ROOT, ".cursor/hooks/publish-docs.log");

const DRY_RUN = process.env.DOC_PUBLISH_DRY_RUN === "1";
const DISABLED = process.env.DOC_PUBLISH_DISABLE === "1";
const SKIP_DEPLOY = process.env.DOC_PUBLISH_SKIP_DEPLOY === "1";

function log(line) {
  const msg = `[${new Date().toISOString()}] ${line}`;
  console.log(msg);
  fs.mkdirSync(path.dirname(LOG_FILE), { recursive: true });
  fs.appendFileSync(LOG_FILE, msg + "\n", "utf8");
}

function run(cmd, args, opts = {}) {
  return execFileSync(cmd, args, {
    cwd: ROOT,
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
    ...opts,
  });
}

function listGitLines(args) {
  // core.quotePath=false keeps non-ASCII paths literal; otherwise git returns
  // octal-escaped names like "docs/\344\273\230....md" and extension checks fail.
  const out = run("git", ["-c", "core.quotePath=false", ...args]).trim();
  if (!out) return [];
  return out.split("\n").map((p) => p.split(path.sep).join("/"));
}

function getChangedPublishableFiles() {
  const files = new Set([
    ...listGitLines(["diff", "--name-only", "HEAD"]),
    ...listGitLines(["diff", "--cached", "--name-only"]),
    ...listGitLines(["ls-files", "--others", "--exclude-standard"]),
  ]);
  return [...files].filter(shouldPublish).sort();
}

function main() {
  if (DISABLED) {
    log("skip: DOC_PUBLISH_DISABLE=1");
    return;
  }

  if (!fs.existsSync(path.join(ROOT, ".git"))) {
    log("skip: not a git repository");
    return;
  }

  const files = getChangedPublishableFiles();
  if (files.length === 0) {
    log("skip: no publishable doc changes");
    return;
  }

  const title =
    files.length === 1
      ? `docs: publish ${path.basename(files[0])}`
      : `docs: publish ${files.length} documents to Vercel`;

  const body = files.map((f) => `- ${f}`).join("\n");
  const message = `${title}\n\n${body}`;

  log(`publish: ${files.length} file(s)`);
  for (const f of files) log(`  · ${f}`);

  if (DRY_RUN) {
    log("dry-run: would commit and push");
    return;
  }

  run("git", ["add", "--", ...files]);
  const staged = run("git", ["diff", "--cached", "--name-only"]).trim();
  if (!staged) {
    log("skip: nothing staged after git add");
    return;
  }

  run("git", ["commit", "-m", message]);

  const branch = run("git", ["rev-parse", "--abbrev-ref", "HEAD"]).trim();
  const push = spawnSync("git", ["push", "-u", "origin", "HEAD"], {
    cwd: ROOT,
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
  });
  if (push.status !== 0) {
    log(`push failed: ${push.stderr || push.stdout}`);
    process.exitCode = 1;
    return;
  }
  log(`pushed branch ${branch}`);

  if (SKIP_DEPLOY) {
    log("skip deploy: DOC_PUBLISH_SKIP_DEPLOY=1");
    return;
  }

  const deploy = spawnSync(
    "npx",
    ["--yes", "vercel", "deploy", "--prod", "--yes"],
    {
      cwd: ROOT,
      encoding: "utf8",
      stdio: ["ignore", "pipe", "pipe"],
      env: { ...process.env, FORCE_COLOR: "0" },
      timeout: 300000,
    }
  );

  const out = `${deploy.stdout || ""}\n${deploy.stderr || ""}`;
  const alias = out.match(/Aliased\s+(\S+)/)?.[1];
  const production = out.match(/Production\s+(\S+)/)?.[1];
  if (deploy.status !== 0) {
    log(`vercel deploy failed: ${out.slice(-800)}`);
    process.exitCode = 1;
    return;
  }

  log(`vercel: ${alias || production || "deploy ok"}`);
}

try {
  main();
} catch (err) {
  log(`error: ${err.message}`);
  process.exitCode = 1;
}
