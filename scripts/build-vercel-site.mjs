#!/usr/bin/env node
/**
 * Build static site for Vercel: copy all publishable .md/.html,
 * generate catalog + manifest + shareable links.
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const OUT = path.join(ROOT, "public");
const TEMPLATES = path.join(__dirname, "templates");

const EXCLUDE_DIRS = new Set([
  ".git",
  ".vscode",
  "node_modules",
  "public",
  "momcozy-app-scene-prototype",
  "momcozy-carousel",
  "momcozy-cozy-outing-mobile",
  "promo-cards",
  "recommendations",
  "scripts",
]);

const EXCLUDE_FILES = new Set([
  "CLAUDE.md",
  "index.html",
  "auth-prototype.html",
]);

const CATEGORY_LABELS = {
  "Skill production": "Skill / 方法论",
  docs: "产品文档",
  html: "报告与页面",
  DTC: "DTC 战略",
  "commercialization planning": "商业化规划",
  "Competitive product research": "竞品调研",
  "全球市场母婴付费订阅调研": "订阅调研",
  ".": "根目录文档",
};

function rmrf(dir) {
  if (!fs.existsSync(dir)) return;
  fs.rmSync(dir, { recursive: true, force: true });
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function shouldSkipDir(name) {
  return EXCLUDE_DIRS.has(name) || name.startsWith(".");
}

function shouldPublish(relPosix) {
  if (EXCLUDE_FILES.has(relPosix)) return false;
  const ext = path.extname(relPosix).toLowerCase();
  if (ext !== ".md" && ext !== ".html") return false;
  return true;
}

function walk(dir, files = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name.startsWith(".") && entry.name !== ".") continue;
    const abs = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (shouldSkipDir(entry.name)) continue;
      walk(abs, files);
      continue;
    }
    const rel = path.relative(ROOT, abs).split(path.sep).join("/");
    if (shouldPublish(rel)) files.push(rel);
  }
  return files;
}

function extractTitle(rel, content) {
  const ext = path.extname(rel).toLowerCase();
  if (ext === ".md") {
    const m = content.match(/^#\s+(.+)$/m);
    if (m) return m[1].trim();
  }
  if (ext === ".html") {
    const m = content.match(/<title[^>]*>([^<]+)<\/title>/i);
    if (m) return m[1].trim();
  }
  return path.basename(rel, ext);
}

function categoryOf(rel) {
  const parts = rel.split("/");
  if (parts.length === 1) return ".";
  return parts[0];
}

function sitePath(rel) {
  return "/" + rel.split("/").map(encodeURIComponent).join("/");
}

function readUrl(rel) {
  return `/_site/viewer.html?file=${encodeURIComponent(rel)}`;
}

function prettyReadUrl(rel) {
  return `/read/${rel.split("/").map(encodeURIComponent).join("/")}`;
}

function getBaseUrl() {
  if (process.env.VERCEL_PROJECT_PRODUCTION_URL) {
    return `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}`;
  }
  if (process.env.VERCEL_URL) {
    return `https://${process.env.VERCEL_URL}`;
  }
  return "";
}

function copyPublishable(files) {
  for (const rel of files) {
    const src = path.join(ROOT, rel);
    const dest = path.join(OUT, rel);
    ensureDir(path.dirname(dest));
    fs.copyFileSync(src, dest);
  }
}

function buildCatalogHtml(groups, baseUrl) {
  const sections = Object.entries(groups)
    .sort(([a], [b]) => a.localeCompare(b, "zh-CN"))
    .map(([cat, items]) => {
      const label = CATEGORY_LABELS[cat] || cat;
      const cards = items
        .map((doc) => {
          const full = baseUrl ? `${baseUrl}${doc.url}` : doc.url;
          const badge = doc.type === "md" ? "MD" : "HTML";
          return `<a class="card" href="${doc.url}">
  <div class="meta"><span class="badge">${badge}</span><span class="path">${doc.path}</span></div>
  <h2>${escapeHtml(doc.title)}</h2>
  <p class="link">${escapeHtml(full)}</p>
</a>`;
        })
        .join("\n");
      return `<section>
  <h2 class="section-title">${escapeHtml(label)}</h2>
  <div class="cards">${cards}</div>
</section>`;
    })
    .join("\n");

  const template = fs.readFileSync(path.join(TEMPLATES, "catalog.html"), "utf8");
  const generatedAt = new Date().toISOString();
  const count = Object.values(groups).reduce((n, arr) => n + arr.length, 0);
  return template
    .replace("{{SECTIONS}}", sections)
    .replace("{{GENERATED_AT}}", generatedAt)
    .replace("{{DOC_COUNT}}", String(count))
    .replace("{{BASE_URL}}", baseUrl || "(部署后自动填充)");
}

function escapeHtml(s) {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function writeLinksMarkdown(docs, baseUrl, outFile) {
  const lines = [
    "# Vercel 文档链接",
    "",
    baseUrl
      ? `站点根地址：**${baseUrl}**`
      : "站点根地址：部署后在 Vercel 控制台查看 Production URL",
    "",
    `生成时间：${new Date().toISOString()}`,
    "",
    "| 标题 | 类型 | 访问链接 |",
    "| --- | --- | --- |",
  ];
  for (const doc of docs) {
    const url = baseUrl ? `${baseUrl}${doc.url}` : doc.url;
    lines.push(`| ${doc.title.replace(/\|/g, "\\|")} | ${doc.type.toUpperCase()} | ${url} |`);
  }
  lines.push("");
  fs.writeFileSync(outFile, lines.join("\n"), "utf8");
}

function main() {
  rmrf(OUT);
  ensureDir(OUT);

  const files = walk(ROOT).sort((a, b) => a.localeCompare(b, "zh-CN"));
  copyPublishable(files);

  const baseUrl = getBaseUrl();
  const docs = files.map((rel) => {
    const content = fs.readFileSync(path.join(ROOT, rel), "utf8");
    const ext = path.extname(rel).toLowerCase();
    const type = ext === ".md" ? "md" : "html";
    return {
      title: extractTitle(rel, content),
      path: rel,
      type,
      category: categoryOf(rel),
      url: type === "md" ? readUrl(rel) : sitePath(rel),
      prettyUrl: type === "md" ? prettyReadUrl(rel) : sitePath(rel),
    };
  });

  const groups = {};
  for (const doc of docs) {
    if (!groups[doc.category]) groups[doc.category] = [];
    groups[doc.category].push(doc);
  }

  ensureDir(path.join(OUT, "_site"));
  fs.copyFileSync(path.join(TEMPLATES, "viewer.html"), path.join(OUT, "_site", "viewer.html"));

  const manifest = {
    generatedAt: new Date().toISOString(),
    baseUrl: baseUrl || null,
    documentCount: docs.length,
    documents: docs.map(({ title, path: p, type, category, url, prettyUrl }) => ({
      title,
      path: p,
      type,
      category,
      url,
      prettyUrl,
      absoluteUrl: baseUrl ? `${baseUrl}${url}` : null,
      absolutePrettyUrl: baseUrl ? `${baseUrl}${prettyUrl}` : null,
    })),
  };

  fs.writeFileSync(
    path.join(OUT, "_site", "manifest.json"),
    JSON.stringify(manifest, null, 2),
    "utf8"
  );

  fs.writeFileSync(
    path.join(OUT, "_site", "index.html"),
    buildCatalogHtml(groups, baseUrl),
    "utf8"
  );

  writeLinksMarkdown(docs, baseUrl, path.join(OUT, "_site", "LINKS.md"));

  // Also write into docs/ for local reference after deploy (optional artifact in build output only)
  console.log(`Built ${docs.length} documents → public/`);
  console.log(`Catalog: ${baseUrl ? baseUrl + "/" : "/"}_site/`);
  if (baseUrl) {
    console.log(`Example MD: ${baseUrl}${docs.find((d) => d.type === "md")?.url || ""}`);
    console.log(`Example HTML: ${baseUrl}${docs.find((d) => d.type === "html")?.url || ""}`);
  }
}

main();
