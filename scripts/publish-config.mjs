/** Shared rules for which repo files are published to Vercel. */
export const EXCLUDE_DIRS = new Set([
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
  ".cursor",
]);

export const EXCLUDE_FILES = new Set([
  "CLAUDE.md",
  "index.html",
  "auth-prototype.html",
]);

export function shouldSkipDir(name) {
  return EXCLUDE_DIRS.has(name) || name.startsWith(".");
}

export function shouldPublish(relPosix) {
  if (!relPosix || relPosix.includes("..")) return false;
  if (EXCLUDE_FILES.has(relPosix)) return false;
  const ext = relPosix.split(".").pop()?.toLowerCase();
  if (ext !== "md" && ext !== "html") return false;

  const parts = relPosix.split("/");
  if (parts.length > 1) {
    for (let i = 0; i < parts.length - 1; i += 1) {
      if (shouldSkipDir(parts[i])) return false;
    }
  }
  return true;
}
