import path from "node:path";

const projectRoot = path.resolve(process.cwd());

/** @type {import('next').NextConfig} */
const nextConfig = {
  turbopack: {
    root: projectRoot,
    resolveAlias: {
      tailwindcss: path.join(projectRoot, "node_modules", "tailwindcss"),
      postcss: path.join(projectRoot, "node_modules", "postcss"),
      autoprefixer: path.join(projectRoot, "node_modules", "autoprefixer"),
    },
  },
};

export default nextConfig;
