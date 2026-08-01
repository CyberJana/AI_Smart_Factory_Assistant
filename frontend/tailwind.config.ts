import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      boxShadow: {
        glow: "0 18px 60px rgba(23, 229, 190, 0.12)",
      },
      colors: {
        surface: "#111b2e",
        canvas: "#080d19",
        accent: "#17e5be",
      },
    },
  },
  plugins: [],
};

export default config;
